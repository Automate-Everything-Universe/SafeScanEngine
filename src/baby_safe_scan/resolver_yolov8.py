"""
Resolver which uses YoloV8 Model.

"""
from pathlib import Path
from typing import List, Any, Union

from PIL.Image import Image
from ultralytics import YOLO

from .folder_utils import convert_image, resize_image
from .resolver import Resolver


class ModelInitializer:
    _model_path = Path(__file__).parents[2] / "models/electrical_outlet_labelstudio.pt"

    @classmethod
    def initialize_model(cls):
        return YOLO(cls._model_path)


class ImageProcessor:
    @staticmethod
    def convert_image(img: Union[Path, Image]) -> Image:
        pil_image = convert_image(file=img)
        if pil_image.width > 640:
            pil_image = resize_image(img=pil_image, width=640)
        return pil_image


class YoloV8Resolver(Resolver):
    """
    YoloV8 Resolver
    """

    def __init__(self, images: List[Any]):
        self.images = images
        self.model = ModelInitializer.initialize_model()

    def process_images(self):
        results = []
        try:
            for image in self.images:
                pil_image = ImageProcessor.convert_image(img=image)
                result = self.run_model(img=pil_image)
                results.append(result)
            return results
        except Exception as e:
            print(f"Error processing image: {e}")

    def run_model(self, img):
        return self.model(source=img, show=True, conf=0.6, save=True, iou=0.4)
