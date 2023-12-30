import base64
import io
from pathlib import Path

from PIL.Image import Image


class Base64Encoder:
    """
    Class to handle encoding from image to ASCI string.
    """
    @staticmethod
    def encode_image_to_base64(image_path: Path) -> str:
        """
        Encodes an image to a Base64 string.

        Args:
        - image_path (Path): The path to the image file to be encoded.

        Returns:
        - str: The Base64 encoded string representation of the image.
        """
        # Open the image file and convert it to binary data
        with Image.open(image_path) as image:
            buffered = io.BytesIO()
            image.save(buffered, format=image.format)
            encoded_image = base64.b64encode(buffered.getvalue())

            return encoded_image.decode('utf-8')
