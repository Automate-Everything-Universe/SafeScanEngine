import base64
import io
from pathlib import Path
from typing import Union

from PIL.Image import Image


class Base64Encoder:
    """
    Class to handle encoding from image to ASCI string.
    """

    @staticmethod
    def encode_image_to_base64(img: Image) -> str:
        # Open the image file and convert it to binary data
        buffered = io.BytesIO()
        img.save(buffered, format="png")
        encoded_image = base64.b64encode(buffered.getvalue())
        return encoded_image.decode("utf-8")

