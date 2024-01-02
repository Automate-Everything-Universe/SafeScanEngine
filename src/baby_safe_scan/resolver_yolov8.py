"""
Resolver which uses YoloV8 Model.

"""
import json
from pathlib import Path
from typing import List, Dict, Any, Union

import numpy as np
import torch
import ultralytics
from PIL import Image
from ultralytics import YOLO
from ultralytics.engine.results import Results, Boxes

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
    def convert_image_to_pillow(img: Image) -> Image:
        pil_image = convert_image(file=img)
        if pil_image.width > 640:
            pil_image = resize_image(img=pil_image, width=640)
        return pil_image

    @staticmethod
    def convert_image_to_base64(img: Union[Image.Image, np.ndarray]) -> str:
        """
        Encodes a Pillow Image or a Numpy array into an ASCII string
        """
        if isinstance(img, np.ndarray):
            img = Image.fromarray(img, "RGB")
        encoded_image = Base64Encoder.encode_image_to_base64(img=img)
        return encoded_image


class YoloResultSerializer:
    def __init__(self, detections: List[Dict[str, Any]], labeled_image: str):
        self.detections = detections
        self.labeled_image = labeled_image

    def to_json(self) -> str:
        """
        Converts the YOLO model results to a JSON-serializable format.

        Returns:
        - str: A JSON string representing the model results.
        """
        data = {
            "detections": self.detections,
            "labeled_image": f"data:image/jpeg;base64,{self.labeled_image}",
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
                pil_image = ImageProcessor.convert_image_to_pillow(img=image)
                detections = self.run_model(img=pil_image)
                image_with_detection = self.extract_labeled_image(detections=detections)
                detections_to_process = self.extract_detections_for_serializer(
                    detections=detections[0]
                )
                image_as_string = ImageProcessor.convert_image_to_base64(
                    img=image_with_detection
                )
                serializer = YoloResultSerializer(detections=detections_to_process, labeled_image=image_as_string)
                json_data = serializer.to_json()
                processed_data.append(json_data)
            return processed_data
        except Exception as e:
            print(f"Error processing image: {e}")

    def run_model(self, img):
        return self.model(source=img, show=False, conf=0.6, save=False, iou=0.4)

    @staticmethod
    def extract_labeled_image(detections):
        try:
            return detections[0].plot()
        except Exception as exc:
            print(f"Could not extract labeled image: {exc}")

    @staticmethod
    def extract_detections_for_serializer(detections: Results):
        try:
            return {
                "boxes": {
                    "xywh": YoloV8Resolver.make_object_json_serializable(
                        getattr(detections.boxes, "xywh", None)
                    ),
                    "xywhn": YoloV8Resolver.make_object_json_serializable(
                        getattr(detections.boxes, "xywhn", None)
                    ),
                    "xyxy": YoloV8Resolver.make_object_json_serializable(
                        getattr(detections.boxes, "xyxy", None)
                    ),
                    "xyxyn": YoloV8Resolver.make_object_json_serializable(
                        getattr(detections.boxes, "xyxyn", None)
                    ),
                },
                "original_shape": YoloV8Resolver.make_object_json_serializable(
                    getattr(detections, "orig_shape", None)
                ),
                "original_image": YoloV8Resolver.make_object_json_serializable(
                    getattr(detections, "orig_img", None)
                ),
                "names": YoloV8Resolver.make_object_json_serializable(
                    getattr(detections, "names", None)
                ),
            }
        except AttributeError as exc:
            print(f"Could not extract detections: {exc}")
            return {}

    @staticmethod
    def make_object_json_serializable(obj: Any):
        try:
            if not YoloV8Resolver.is_object_json_serializable(obj):
                if isinstance(obj, (torch.Tensor, np.ndarray)):
                    return obj.tolist()
            return obj
        except TypeError as exc:
            raise TypeError(f"Object is not JSON serializable: {obj}") from exc

    @staticmethod
    def is_object_json_serializable(obj: Any):
        try:
            json.dumps(obj)
            return True
        except TypeError as exc:
            print("Not JSON serializable:", exc)
            return False
