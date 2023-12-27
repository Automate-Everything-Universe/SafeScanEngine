import os
from pathlib import Path

import pytest
from src.resolver.folder_utils import load_image


TEST_FOLDER = Path(__file__).parents[0]


@pytest.fixture
def file() -> Path:
    return TEST_FOLDER / "pic/replace_pic.png"


@pytest.fixture
def input_path() -> Path:
    return TEST_FOLDER / "pic/"


@pytest.fixture
def expected_yollo() -> Path:
    return TEST_FOLDER / "pic/logo_converted_pillow.png"


def test_transparent_pillow(file, expected_pillow):
    image_object = load_image(picture=file)
    # Check if processed image was created
    assert expected_pillow.exists(), "Processed image file does not exist"

    # Open the processed image and check for transparency
    assert image_object.mode == 'RGBA', "Image is not in RGBA mode"
    corner_pixel = image_object.getpixel((0, 0))
    assert corner_pixel[3] == 0, "Background is not transparent"

    # Clean up
    os.remove(expected_pillow)