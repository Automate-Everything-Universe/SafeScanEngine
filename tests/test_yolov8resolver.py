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
def input_path() -> Path:
    return TEST_FOLDER / "pic/"


def test_yolovresolver(img_1, img_2):
    electrical_outlet_resolver = YoloV8Resolver(images=[img_1, img_2])
    results = electrical_outlet_resolver.create_json_object()
    assert len(results) >= 1, "No result was extracted"