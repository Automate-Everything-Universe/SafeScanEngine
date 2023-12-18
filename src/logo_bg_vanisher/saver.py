"""
Module which handles saving the picture
"""
from pathlib import Path

from PIL import Image


class SavePic:
    """
    Class to save the Pillow image object
    """

    def __init__(self, img: Image):
        self.image = img

    def save_image(self, suffix: str = "converted") -> None:
        """
        Saves the image
        :param suffix: Suffix for converted images
        :return: None
        """
        try:
            filename = Path(self.image.filename)
            output_path = filename.parent / f"{filename.stem}{suffix}.png"
            self.image.save(output_path, "PNG")
        except OSError as exc:
            raise OSError(f"Error saving image: {exc}") from exc
        except ValueError as exc:
            raise ValueError(f"Invalid image: {exc}") from exc
