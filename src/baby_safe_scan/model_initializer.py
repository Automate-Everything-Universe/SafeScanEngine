"""
Module for different models
"""
from abc import ABC, abstractproperty, abstractmethod
from pathlib import Path
from typing import Any, Type

from ultralytics import YOLO

ELECTRICAL_OUTLET_MODEL = (
    Path(__file__).parents[2] / "models/electrical_outlet_labelstudio.pt"
)


class ModelInitializer(ABC):
    def __init__(self, model_type: Any, model_path: Path):
        self.model_type = model_type
        self.model_path = model_path

    @abstractmethod
    def model(self):
        """
        Returns the initialized model
        """


class YoloV8ModelInitializer(ModelInitializer):
    def __init__(self, model_type: Type[YOLO], model_path: Path):
        super().__init__(model_type, model_path)
        self._model = None

    @property
    def model(self):
        if self._model is None:
            self._model = self.model_type(self.model_path)
        return self._model
