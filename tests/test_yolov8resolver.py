import pytest
from pathlib import Path

from src.baby_safe_scan import YoloV8Resolver

TEST_FOLDER = Path(__file__).parents[0]


@pytest.fixture
def img_1() -> Path:
    return TEST_FOLDER / "pic/electrical_outlet.png"


@pytest.fixture
def img_2() -> Path:
    return TEST_FOLDER / "pic/electrical_outlet_with_kid.jpg"


@pytest.fixture
def img_no_danger() -> Path:
    return TEST_FOLDER / "pic/empty_living_room.jpeg"

@pytest.fixture
def input_path() -> Path:
    return TEST_FOLDER / "pic/"


def test_yolovresolver(img_1, img_2, img_no_danger):
    electrical_outlet_resolver = YoloV8Resolver(images=[img_1, img_no_danger, img_2])
    results = electrical_outlet_resolver.return_detections()
    assert len(results) >= 1, "No result was extracted"