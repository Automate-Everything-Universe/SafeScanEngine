"""
Module which handles the Image creation

"""
from abc import ABC
from abc import abstractmethod
from pathlib import Path
from typing import Union

from PIL import Image


class ImageCreator(ABC):
    """
    Interface for creating
    """

    def __init__(self, file: Union[Path, str]):
        self.file = file

    @abstractmethod
    def convert_image(self):
        """
        Abstract method for sizer objects.
        """


class CreatePillowImage(ImageCreator):
    """
    Converts a picture to a Pillow image object
    """

    def __init__(self, file: Union[Path, str]):
        super().__init__(file)

    def convert_image(self) -> Image:
        """
        Converts a file path to a Pillow image
        :param file: Path to a file
        :return: Pillow Image object
        """
        try:
            file_is_valid = self.validate_image(self.file)
            if file_is_valid:
                return Image.open(self.file)
        except FileNotFoundError as exc:
            raise FileNotFoundError(f"The file {self.file} was not found") from exc
        except PermissionError as exc:
            raise PermissionError(f"Permission denied for file {self.file}") from exc
        except OSError as exc:
            raise OSError(f"An error occurred while opening the file {self.file}: {exc}") from exc
        except Exception as exc:
            raise Exception(f"An unexpected error occurred: {exc}") from exc

    @staticmethod
    def validate_image(file: Path) -> bool:
        if not file.exists():
            raise FileNotFoundError(f"The file {file} does not exist")
        if not isinstance(file, (str, Path)):
            raise ValueError("File path must be str or Path object")
        return True
