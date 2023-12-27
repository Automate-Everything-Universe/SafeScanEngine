"""
Yolov8 resolver
"""
from pathlib import Path
from typing import List

from PIL.Image import Image

from .resolver import Resolver
from src.main import (
    convert_image,
    resize_image
)
from src.yolov8_custom import initialize_model


class Yolov8Resolver(Resolver):
    def __init__(self, images: List[Path, ...]):
        self.images = images

    def process_images(self):
        self.define_entries()

    def define_entries(self):
        for image in self.images:
            pil_image = convert_image(file=image)
            if pil_image.height > 640:
                pil_image = resize_image(img=pil_image, width=640)
            self.run_yolov8(img=pil_image)

    @staticmethod
    def run_yolov8(img: Image) -> None:
        model = initialize_model()
        model(source=img, show=True, conf=0.2, save=True, iou=0.4)
