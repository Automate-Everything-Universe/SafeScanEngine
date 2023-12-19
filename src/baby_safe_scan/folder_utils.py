"""
Module to handle file operations
"""
import os
from pathlib import Path
from typing import List
from typing import Tuple
from typing import Union

from PIL.Image import Image

from .image_creator import CreatePillowImage


def find_files(path: Path, extension: Union[str, Tuple, None]) -> List[Path]:
    """
    Finds and returns files with certain extension
    :param path:
    :param extension:
    :return: list of images
    """
    path_is_valid = validate_path(path=path)
    if not path_is_valid:
        raise ValueError("Folder path is not valid")
    elif extension:
        pics = [pic for pic in path.iterdir() if pic.suffix.lower() in extension]
        if not pics:
            raise FileNotFoundError(f"No picture was found with {extension} in folder {path}")
        return pics
    pics = [pic for pic in path.iterdir()]
    if not pics:
        raise FileNotFoundError(f"No picture was found in folder {path}")
    return pics


def validate_path(path: Path) -> bool:
    """
    Validates path, returns False if path is not valid.
    :param path:
    :return: bool
    """
    if not any((path.exists(), path.is_dir())):
        return False
    return True


def load_image(picture: Path) -> Union[Image, None]:
    try:
        if not picture.exists():
            raise ValueError('The picture could not be found!')
        if not os.access(picture, os.R_OK):
            raise PermissionError(f"Permission denied for file {picture} !")
        if picture:
            image_creator = CreatePillowImage(file=picture)
            image_obj = image_creator.convert_image()
            return image_obj
    except PermissionError as exc:
        raise PermissionError(f"Permission error: {exc}") from exc
    except OSError as exc:
        raise OSError(f"Error opening image: {exc}") from exc
