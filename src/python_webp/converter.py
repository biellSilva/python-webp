from concurrent.futures import ThreadPoolExecutor
from glob import glob
from pathlib import Path

from PIL import Image
from PIL.Image import Image as ImageType
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)

from python_webp._logging import get_logger
from python_webp._settings import Settings
from python_webp.exceptions import PyWebpInputError, PyWebpInputSizeError

_logger = get_logger(__name__)


class Converter:
    def __init__(
        self,
        *,
        input: Path,
        output: Path,
        files_format: list[str] | None,
        quality: int,
        alpha_quality: int,
        lossless: bool,
        method: int,
        exact: bool,
        keep_directory: bool,
        recursive: bool,
        use_threads: bool,
        threads: int | None,
        unlink: bool,
        ignore_existing: bool,
        resize: str | None,
        keep_aspect_ratio: bool,
        min_width: int | None,
        min_height: int | None,
        max_width: int | None,
        max_height: int | None,
    ) -> None:
        self.input = input
        self.output = output

        self.files_format = files_format or Settings.DEFAULT_FILES_FORMAT
        self.quality = quality
        self.alpha_quality = alpha_quality
        self.lossless = lossless
        self.method = method
        self.exact = exact

        self.keep_directory = keep_directory
        self.recursive = recursive
        self.use_threads = use_threads
        self.threads = threads

        self.unlink = unlink
        self.ignore_existing = ignore_existing

        self.resize = resize
        self.keep_aspect_ratio = keep_aspect_ratio

        self.min_width = min_width
        self.min_height = min_height
        self.max_width = max_width
        self.max_height = max_height

        self._files: list[Path] = []

        self._width: int
        self._height: int

        self._validate_input_path()
        self._parse_files_format()
        self._parse_sizes()

        _logger.debug(self)

    def __repr__(self) -> str:
        vars_ = ", ".join(
            f"{k}={v}" for k, v in self.__dict__.items() if not k.startswith("_")
        )
        return f"{self.__class__.__name__}({vars_})"

    def _validate_input_path(self) -> None:
        if not self.input.exists():
            raise PyWebpInputError(self.input)

    def _parse_files_format(self) -> None:
        formats_: list[str] = []

        for format_ in self.files_format:
            formats_.extend(string_.strip() for string_ in format_.split(","))

        self.files_format = formats_

    def _parse_sizes(self) -> None:
        if self.resize:
            try:
                width, height = map(int, self.resize.split("x"))
                self._width = width
                self._height = height
            except ValueError:
                raise PyWebpInputSizeError(self.resize) from None

    def _search_images(self, progress: Progress) -> None:
        for format_ in self.files_format:
            pattern = f"**/*.{format_}" if self.recursive else f"*.{format_}"
            files = list(
                glob(
                    str(self.input / pattern),
                    recursive=self.recursive,
                )
            )

            _logger.debug(f"Found {len(files)} {format_} files")

            self._files.extend([Path(file) for file in files])
            progress.update(self.task, total=len(self._files), refresh=True)

        _logger.debug(f"Found {len(self._files)} image files")

    def _iter_files(self, progress: Progress) -> None:
        _logger.debug("Starting conversion")
        progress.update(self.task, description="Converting", start=True)

        if self.use_threads:
            _logger.debug("Using threads")
            with ThreadPoolExecutor(max_workers=self.threads) as executor:
                for file in self._files:
                    executor.submit(self._convert_image, file, progress)

                executor.shutdown(wait=True)
        else:
            for file in self._files:
                self._convert_image(path=file, progress=progress)

    def _resize(self, img: ImageType) -> ImageType:
        if not self.resize:
            return img

        if self.keep_aspect_ratio:
            img.thumbnail((self._width, self._height))
        else:
            img = img.resize((self._width, self._height))

        return img

    def _skip_size(self, img: ImageType) -> bool:
        if self.min_width and img.width < self.min_width:
            return True

        elif self.min_height and img.height < self.min_height:
            return True

        elif self.max_width and img.width > self.max_width:
            return True

        elif self.max_height and img.height > self.max_height:
            return True
        return False

    def _convert_image(self, path: Path, progress: Progress) -> None:
        output_path = self.output / path.relative_to(self.input)

        if not self.keep_directory:
            output_path = self.output / path.name

        output_path.parent.mkdir(parents=True, exist_ok=True)

        output_path = output_path.with_suffix(".webp")

        if output_path.exists() and self.ignore_existing:
            _logger.debug(f'Skipping "{output_path}" due to existing file')
            progress.advance(self.task)
            return

        with Image.open(path) as img:
            if self._skip_size(img):
                _logger.debug(f'Skipping "{path}" due to min/max size requirements')
                progress.advance(self.task)
                return

            img = self._resize(img)

            img.save(
                output_path,
                "WEBP",
                quality=self.quality,
                alpha_quality=self.alpha_quality,
                lossless=self.lossless,
                method=self.method,
                exact=self.exact,
            )

        if self.unlink:
            path.unlink()
            _logger.debug(f"Unlinked {path}")

        _logger.debug(f"=> {output_path}")
        progress.advance(self.task)

    def run(self) -> None:
        with Progress(
            SpinnerColumn(),
            BarColumn(),
            TimeElapsedColumn(),
            TextColumn(
                "{task.description:<10} ({task.completed}/{task.total})", style="black"
            ),
        ) as progress:
            self.task = progress.add_task(description="Searching files", total=0)
            self._search_images(progress=progress)
            self._iter_files(progress=progress)
        _logger.debug("Task completed")
