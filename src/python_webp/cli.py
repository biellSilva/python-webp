from pathlib import Path
from typing import Annotated, Union

import typer

from python_webp.__version__ import get_version
from python_webp._logging import get_logger, setup_logging

setup_logging()

_logger = get_logger(__name__)

app = typer.Typer(rich_markup_mode="rich")

_LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


def _version_callback(value: bool | None) -> None:
    if value:
        _logger.info(f"Python WebP CLI version {get_version()}")
        raise typer.Exit()


def _set_log_level(value: str) -> None:
    get_logger("pywebp").setLevel(value.upper())


@app.callback()
def callback(
    version: Annotated[
        Union[bool, None],
        typer.Option(
            "--version",
            help="Show the version of the Python WebP CLI",
            callback=_version_callback,
        ),
    ] = None,
    log_level: Annotated[
        str,
        typer.Option(
            "--log-level",
            help=f"Set the log level, must be one of: {', '.join(_LOG_LEVELS)}",
            case_sensitive=False,
            show_default=True,
            callback=_set_log_level,
        ),
    ] = "WARNING",
) -> None:
    """
    Python WebP CLI

    A CLI to convert images to WebP format.
    """


@app.command()
def convert(
    input: Annotated[Path, typer.Argument(help="Input directory")] = Path("."),
    output: Annotated[Path, typer.Argument(help="Output directory")] = Path("."),
    *,
    resize: Annotated[
        str | None,
        typer.Option(help="Resize image to the given size. e.g 640x800"),
    ] = None,
    min_width: Annotated[
        int | None,
        typer.Option(help="Skips images that are smaller then the given size."),
    ] = None,
    min_height: Annotated[
        int | None,
        typer.Option(help="Skips images that are smaller then the given size."),
    ] = None,
    max_width: Annotated[
        int | None,
        typer.Option(help="Skips images that are bigger then the given size."),
    ] = None,
    max_height: Annotated[
        int | None,
        typer.Option(help="Skips images that are bigger then the given size."),
    ] = None,
    keep_aspect_ratio: Annotated[
        bool, typer.Option(help="Keep the original aspect ratio while resizing")
    ] = True,
    files_format: Annotated[
        list[str] | None,
        typer.Option(help="Input files format. e.g png,jpg,jpeg"),
    ] = None,
    quality: Annotated[
        int,
        typer.Option(
            help=(
                "Integer, 0-100. For lossy, 0 gives the smallest size and "
                "100 the largest. For lossless, this parameter is the amount of effort put into "
                "the compression: 0 is the fastest, but gives larger files compared to the slowest, "
                "but best, 100."
            )
        ),
    ] = 80,
    alpha_quality: Annotated[
        int,
        typer.Option(
            help=(
                "Integer, 0-100. For lossy compression only. "
                "0 gives the smallest size and 100 is lossless."
            )
        ),
    ] = 100,
    lossless: Annotated[bool, typer.Option(help="Enable lossless compression")] = False,
    method: Annotated[
        int,
        typer.Option(help="Quality/speed trade-off (0=fast, 6=slower-better)."),
    ] = 4,
    exact: Annotated[
        bool,
        typer.Option(
            help=(
                "If true, preserve the transparent RGB values. Otherwise, "
                "discard invisible RGB values for better compression."
            )
        ),
    ] = False,
    keep_directory: Annotated[
        bool, typer.Option(help="Keep the directory structure of the input")
    ] = True,
    recursive: Annotated[
        bool, typer.Option(help="Convert images in subdirectories")
    ] = False,
    use_threads: Annotated[bool, typer.Option(help="Use multiple threads")] = False,
    threads: Annotated[
        int | None,
        typer.Option(
            help="Number of threads to use. None = Max possible (4 * N of cores, limited to 32)"
        ),
    ] = None,
    unlink: Annotated[bool, typer.Option(help="Unlink/delete the input files")] = False,
    ignore_existing: Annotated[bool, typer.Option(help="Ignore existing files")] = True,
) -> None:
    """
    Convert an image to WebP format.
    """
    from python_webp.converter import Converter

    Converter(
        input=input,
        output=output,
        files_format=files_format,
        quality=quality,
        alpha_quality=alpha_quality,
        lossless=lossless,
        method=method,
        exact=exact,
        keep_directory=keep_directory,
        recursive=recursive,
        use_threads=use_threads,
        threads=threads,
        unlink=unlink,
        ignore_existing=ignore_existing,
        resize=resize,
        keep_aspect_ratio=keep_aspect_ratio,
        min_width=min_width,
        min_height=min_height,
        max_width=max_width,
        max_height=max_height,
    ).run()


def main() -> None:
    app()
