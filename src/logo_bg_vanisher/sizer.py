"""
Module which handles the sizing
"""
from abc import ABC
from abc import abstractmethod
from typing import Union

from PIL import Image

from .utils_validation import are_numbers_valid


class Sizer(ABC):
    """
    Interface for sizer objects
    """

    def __init__(self, img: Image):
        self.image = img

    @abstractmethod
    def set_size(self) -> Image:
        """
        Abstract method for sizer objects.
        :return: Pillow image
        """


class AspectRatioSizer(Sizer):
    """
    Changes the picture size while keeping the aspect ratio.
    """

    def __init__(self, img: Image, width: int):
        super().__init__(img)
        self.filename = img.filename
        self.width = are_numbers_valid(width)

    def set_size(self) -> Image:
        if not self.width:
            raise ValueError("No width provided. The width must be an integer")
        else:
            new_height = self._calculate_height(img=self.image)
            resized_img = self.image.resize(size=(self.width, new_height))
            resized_img.filename = self.filename
            return resized_img

    def _calculate_height(self, img: Image):
        """
        Calcules for the user given width the new height in order to keep the original aspect ratio.
        :param img: Pillow Image object
        :return: New calculated height
        """
        w_percent = (self.width / float(img.size[0]))
        new_height = int(float(img.size[1]) * float(w_percent))
        return new_height


class ManualSizer(Sizer):
    """
    Changes the picture size from user width and height
    """

    def __init__(self, img: Image, width: int, height: int):
        super().__init__(img)
        self.filename = img.filename
        self.width, self.height = are_numbers_valid(width, height)

    def set_size(self) -> Image:
        if not all((self.width, self.height)):
            raise ValueError("Width and height must be provided in integer form (width, height)")
        else:
            resized_img = self.image.resize(size=(self.width, self.height))
            resized_img.filename = self.filename
            return resized_img
