import logging
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from PIL import Image
from PIL.Image import Image as ImageType

from ._arg_parser import get_argparser

AVALIABLE_FORMATS: set[str] = set([".jpg", ".jpeg", ".png"])


def _setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    logger = logging.getLogger("pywebp")

    return logger


_logger = _setup_logging()


class Core:
    def __init__(
        self,
        input: str,
        output: str,
        quality: int,
        size: str | None,
        verbose: bool,
        optimize: bool,
        recursive: bool,
        keep_directory: bool,
        unlink: bool,
        threads: int | None,
        no_threads: bool,
    ):
        self.input = input
        self.output = output
        self.quality = quality
        self.size = self.__size_to_tuple(size)
        self.verbose = verbose
        self.optimize = optimize
        self.recursive = recursive
        self.keep_directory = keep_directory
        self.unlink = unlink
        self.threads = threads
        self.no_threads = no_threads

    def __str__(self) -> str:
        return f"""{self.__class__.__name__}({
            ", ".join(f'{k}={v}' for k, v in self.__dict__.items())
            })"""

    def __log(
        self, message: str, is_error: bool = False, err: Exception | None = None
    ) -> None:
        if is_error:
            _logger.error(message, exc_info=err)
            return

        if self.verbose:
            _logger.info(message)

    def __size_to_tuple(self, size: str | None) -> tuple[int, int] | None:
        if size:
            X, Y = size.split("x", 1)
            assert X.isdigit() and isinstance(
                X, int
            ), "Size must be in the format of '640x480'"
            assert Y.isdigit() and isinstance(
                Y, int
            ), "Size must be in the format of '640x480'"
            return X, Y
        return None

    def __size_to_string(self, size: tuple[int, int] | None) -> str | None:
        if size:
            return "x".join(map(str, size))
        return None

    def __get_output_path(self, path: Path) -> Path:
        path_ = Path(self.output)

        if self.keep_directory:
            parents = [parent.name for parent in path.parents]
            parents.reverse()
            path_ = Path(self.output, *parents)

        path_.mkdir(parents=True, exist_ok=True)
        return path_

    def resize_image(self, image: ImageType) -> ImageType:
        if self.size:
            self.__log(f"Resizing image to {self.__size_to_string(self.size)}")
            return image.resize(size=self.size)
        return image

    def open_image(self, path: Path) -> ImageType:
        self.__log(f"Opening image {str(path)}")
        return Image.open(path)

    def convert_to_webp(self, image: ImageType, path: Path) -> None:
        output_path = Path(
            str(self.__get_output_path(path)), path.name.split(".")[0] + ".webp"
        )

        self.__log(f"Saving image to {str(output_path)}")

        image.save(
            str(output_path),
            "WEBP",
            quality=self.quality,
            optimize=self.optimize,
        )

    def convert_image(self, path: Path) -> None:
        image = self.open_image(path)
        image = self.resize_image(image)
        self.convert_to_webp(image, path)
        if self.unlink:
            self.__log(f"Unlinking {str(path)}")
            path.unlink(missing_ok=True)

    def process_images(self, path: Path | None = None):
        path = path or Path(self.input)

        assert path.exists(), f"Path {path} does not exist"

        if path.is_file():
            self.convert_image(path)
            return

        for file in Path(path).iterdir():
            if file.is_dir() and self.recursive:
                self.process_images(file)

            if (
                file.is_file()
                and file.suffix != ".webp"
                and file.suffix in AVALIABLE_FORMATS
            ):
                if not self.no_threads:
                    with ThreadPoolExecutor(max_workers=self.threads) as executor:
                        executor.submit(self.convert_image, file)
                else:
                    self.convert_image(file)


def main():
    Core(**get_argparser().__dict__).process_images()
