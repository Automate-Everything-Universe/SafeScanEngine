from typing import List, Union

import numpy as np
from PIL import Image
from PIL.Image import Image as PilImage
from ultralytics.engine.results import Results

from .encoders import Base64Encoder
from .folder_utils import convert_image, resize_image


class ImageProcessor:
    @staticmethod
    def convert_images_to_pillow(images: List[PilImage]) -> List[PilImage]:
        processed_images = []
        for image in images:
            pil_image = convert_image(file=image)
            if pil_image.width > 640:
                pil_image = resize_image(img=pil_image, width=640)
                processed_images.append(pil_image)
            else:
                processed_images.append(pil_image)

        return processed_images

    @staticmethod
    def convert_image_to_base64(img: Union[Image.Image, np.ndarray]) -> str:
        """
        Encodes a Pillow Image or a Numpy array into an ASCII string
        """
        if isinstance(img, np.ndarray):
            img = Image.fromarray(img, "RGB")
        encoded_image = Base64Encoder.encode_image_to_base64(img=img)
        return encoded_image

    @staticmethod
    def extract_labeled_image(detections: Results) -> PilImage:
        try:
            return detections[0].plot()
        except Exception as exc:
            print(f"Could not extract labeled image: {exc}")
