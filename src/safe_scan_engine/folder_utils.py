"""
Module to handle file operations
"""
from pathlib import Path
from typing import List
from typing import Tuple
from typing import Union

from PIL import Image
from PIL.Image import Image as PilImage
from pillow_heif import register_heif_opener


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


def convert_image(file: Union[str, Path]) -> PilImage:
    try:
        if not isinstance(file, (str, Path)):
            raise ValueError("Expected image to be Path object")
        if isinstance(file, str):
            file = Path(file)
        if file.suffix == ".HEIC":
            # https://stackoverflow.com/questions/54395735/how-to-work-with-heic-image-file-types-in-python
            register_heif_opener()
            return Image.open(file)
        return Image.open(file)

    except FileNotFoundError as exc:
        raise FileNotFoundError(f"File not found {file}") from exc
    except PermissionError as exc:
        raise PermissionError(f"Permission denied {file}") from exc
    except OSError as exc:
        raise OSError(f"Error occurred while opening file {file}") from exc
    except Exception as exc:
        raise Exception("Unexpected error occurred when opening the image") from exc
