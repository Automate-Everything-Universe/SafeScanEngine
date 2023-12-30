"""
Resolver which uses YoloV8 Model.

"""
import json
from pathlib import Path
from typing import List, Dict, Any, Union

from PIL.Image import Image
from ultralytics import YOLO

from .encoders import Base64Encoder
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


class YoloResultSerializer:
    def __init__(self, detections: List[Dict[str, Any]], labeled_image: bytes):
        self.detections = detections
        self.labeled_image = labeled_image

    def to_json(self) -> str:
        """
        Converts the YOLO model results to a JSON-serializable format.

        Returns:
        - str: A JSON string representing the model results.
        """
        encoded_image = Base64Encoder.encode_image_to_base64(self.labeled_image)
        data = {
            "detections": self.detections,
            "labeled_image": f"data:image/jpeg;base64,{encoded_image}"
        }
        return json.dumps(data)


class YoloV8Resolver(Resolver):
    """
    YoloV8 Resolver
    """

    def __init__(self, images: List[Any]):
        self.images = images
        self.model = ModelInitializer.initialize_model()

    def process_images(self):
        processed_data = []
        try:
            for image in self.images:
                pil_image = ImageProcessor.convert_image(img=image)
                detections, labeled_image = self.run_model(img=pil_image)
                serializer = YoloResultSerializer(detections, labeled_image)
                json_data = serializer.to_json()
                processed_data.append(json_data)
                processed_data.append(result_yolo)
            return processed_data
        except Exception as e:
            print(f"Error processing image: {e}")

    def run_model(self, img):
        return self.model(source=img, show=True, conf=0.6, save=True, iou=0.4)
