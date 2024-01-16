"""
Resolver which uses YoloV8 Model.

"""
import json
from typing import Any
from typing import Dict
from typing import List

import numpy as np
import torch
from ultralytics import YOLO
from ultralytics.engine.results import Results

from .image_processor import ImageProcessor
from .model_initializer import MODEL
from .model_initializer import YoloV8ModelInitializer
from .resolver import Resolver


class YoloV8Resolver(Resolver):
    """
    YoloV8 Resolver
    """

    def __init__(self, images: List[Any]):
        self.images = ImageProcessor.convert_images_to_pillow(images)
        self.model_intializer = YoloV8ModelInitializer(
            model_type=YOLO, model_path=MODEL
        )
        self.model = self.model_intializer.model
        self.detections = self.model(source=self.images, show=False, conf=0.7, save=False, iou=0.4)

    def return_detections(self):
        try:
            processed_detections = []
            for detection in self.detections:
                if not YoloV8Resolver.is_danger_found(detection=detection):
                    danger_found = {"danger_found": False}
                    processed_detections.append(danger_found)
                else:
                    danger_found = {"danger_found": True}
                    labeled_image = ImageProcessor.extract_labeled_image(detections=detection)
                    detections_to_process = self.extract_detections_metadata(detections=detection)
                    encoded_image = ImageProcessor.encode_image_base64(img=labeled_image)
                    detections_to_return = {
                        **detections_to_process,
                        **encoded_image,
                        **danger_found,
                    }
                    processed_detections.append(detections_to_return)
            return processed_detections
        except Exception as e:
            print(f"Error processing image: {e}")

    @staticmethod
    def is_danger_found(detection: Results) -> bool:
        """
        If no Yolo detections boxes were found, return false
        """
        if not detection.boxes.shape[0]:
            return False
        return True

    @staticmethod
    def extract_detections_metadata(detections: Results) -> Dict[str, str]:
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
            elif isinstance(obj, tuple):
                return list(obj)
            elif isinstance(obj, dict):
                return obj
            else:
                print(f"fObject type not handled: {type(obj)}")
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

    @staticmethod
    def gather_detections(**kwargs) -> Dict:
        return {k: v for k, v in kwargs}
