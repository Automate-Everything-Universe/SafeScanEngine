"""
Resolver which uses YoloV8 Model.

"""
import json

from typing import List, Dict, Any, Union

import numpy as np
import torch

from ultralytics import YOLO

from ultralytics.engine.results import Results, Boxes

from .image_processor import ImageProcessor
from .model_initializer import YoloV8ModelInitializer
from .model_initializer import ELECTRICAL_OUTLET_MODEL
from .resolver import Resolver


class YoloResultSerializer:
    def __init__(self, detections: Dict[str, Any], labeled_image: str):
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


class YoloV8Resolver:
    """
    YoloV8 Resolver
    """

    def __init__(self, images: List[Any]):
        self.images = ImageProcessor.convert_images_to_pillow(images)
        self.model_intializer = YoloV8ModelInitializer(
            model_type=YOLO, model_path=ELECTRICAL_OUTLET_MODEL
        )
        self.model = self.model_intializer.model
        self.detections = self.model(
            source=self.images, show=False, conf=0.6, save=False, iou=0.4
        )

    def create_json_object(self):
        try:
            processed_detections = []
            for detection in self.detections:
                if YoloV8Resolver.detections_is_available(detection=detection):
                    labeled_image = ImageProcessor.extract_labeled_image(
                        detections=detection
                    )
                    detections_to_process = self.extract_detections_for_serializer(
                        detections=detection
                    )
                    image_as_string = ImageProcessor.convert_image_to_base64(
                        img=labeled_image
                    )
                    serializer = YoloResultSerializer(
                        detections=detections_to_process, labeled_image=image_as_string
                    )
                    json_data = serializer.to_json()
                    processed_detections.append(json_data)
                    return processed_detections
                else:
                    continue
        except Exception as e:
            print(f"Error processing image: {e}")

    @staticmethod
    def detections_is_available(detection: Results) -> bool:
        if not detection.boxes.shape[0]:
            return False
        return True

    @staticmethod
    def extract_detections_for_serializer(detections: Results) -> object:
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
