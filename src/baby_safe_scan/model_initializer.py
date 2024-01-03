"""
Module for different models
"""

from pathlib import Path

from ultralytics import YOLO

ELECTRICAL_OUTLET = (
    Path(__file__).parents[2] / "models/electrical_outlet_labelstudio.pt"
)


class ModelInitializer:
    def __init__(self, model):
        self.model = model

    def initialize_model(self):
        return YOLO(self.model)
