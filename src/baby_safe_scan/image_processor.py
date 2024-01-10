from pathlib import Path
from typing import List, Union, Dict

import numpy as np
from PIL import Image
from PIL.Image import Image as PilImage
from ultralytics.engine.results import Results

from .encoders import Base64Encoder
from .folder_utils import convert_image


class ImageProcessor:
    @staticmethod
    def convert_images_to_pillow(images: List[Union[Path, str]]) -> List[PilImage]:
        processed_images = []
        for image in images:
            pil_image = convert_image(file=image)
            processed_images.append(pil_image)
        return processed_images

    @staticmethod
    def encode_image_base64(img: Union[Image.Image, np.ndarray]) -> Dict[str, str]:
        if not isinstance(img, (np.ndarray, Image.Image)):
            raise ValueError(f"Wrong data type used for base64 image encoding: {type(img)}")
        elif isinstance(img, np.ndarray):
            img = Image.fromarray(img, "RGB")
            encoded_image = Base64Encoder.encode_image_to_base64(img=img)
        else:
            encoded_image = Base64Encoder.encode_image_to_base64(img=img)
        return {"encoded_image": encoded_image}

    @staticmethod
    def extract_labeled_image(detections: Results) -> PilImage:
        try:
            return detections[0].plot()
        except Exception as exc:
            print(f"Could not extract labeled image: {exc}")
