from pathlib import Path

from ultralytics import YOLO

ELECTRIC_OUTLET_LABEL_STUD = Path(__file__).parents[1] / "models/electrical_outlet_labelstudio.pt"


def initialize_model():
    return YOLO(ELECTRIC_OUTLET_LABEL_STUD)


if __name__ == "__main__":
    initialize_model()
