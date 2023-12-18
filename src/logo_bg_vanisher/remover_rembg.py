"""
Module which handles background removal from pics using Rembgr
"""
import rembg
from PIL import Image

from .background_remover import BackgroundRemovalStrategy
from .utils_validation import is_string_valid


class RembgBackgroundRemoval(BackgroundRemovalStrategy):
    def __init__(self, img, suffix: str = "_rembg_converted"):
        super().__init__(img)
        self.filename = img.filename
        self.suffix = is_string_valid(text=suffix)

    def remove_background(self) -> Image:
        if self.image is None or not hasattr(self.image, 'convert'):
            raise ValueError("Invalid image object provided")

        img = self.image.convert("RGBA")
        processed_img = rembg.remove(img)
        processed_img.filename = self.filename
        return processed_img
