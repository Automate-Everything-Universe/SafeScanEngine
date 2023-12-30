import pytest
from pathlib import Path

from src.baby_safe_scan import YoloV8Resolver

TEST_FOLDER = Path(__file__).parents[0]


@pytest.fixture
def file() -> Path:
    return TEST_FOLDER / "pic/electrical_outlet.png"


@pytest.fixture
def input_path() -> Path:
    return TEST_FOLDER / "pic/"


@pytest.fixture
def expected_yollo() -> Path:
    return TEST_FOLDER / "pic/logo_converted_pillow.png"  # todo: add path with expected result


def test_yolovresolver(file):
    electrical_outlet_resolver = YoloV8Resolver(images=[file])
    results = electrical_outlet_resolver.process_images()
    print("")

    # Check if processed image was created
    # assert expected_pillow.exists(), "Processed image file does not exist"

    # Clean up
    # os.remove(expected_pillow)
    # shutil.rmtree()
