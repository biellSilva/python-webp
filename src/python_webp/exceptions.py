from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


class PyWebpError(Exception):
    """Base class for exceptions in this module."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class PyWebpInputError(PyWebpError):
    """Exception raised for errors in the input.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, path: "str | Path") -> None:
        self.path = path
        super().__init__(f'Input directory "{path}" does not exist')


class PyWebpInputSizeError(PyWebpError):
    """Exception raised for errors in the input size.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, size: str) -> None:
        self.size = size
        super().__init__(f"Invalid size format: {size}, expected format: 640x800")
