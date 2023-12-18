import os
from pathlib import Path

import pytest
from src.logo_bg_vanisher import AspectRatioSizer
from src.logo_bg_vanisher import ManualSizer
from src.logo_bg_vanisher.folder_utils import load_image
from src.logo_bg_vanisher import SavePic

TEST_FOLDER = Path(__file__).parents[0]


@pytest.fixture
def file() -> Path:
    return TEST_FOLDER / "logo/logo.png"


@pytest.fixture
def input_path() -> Path:
    return TEST_FOLDER / "logo/"


@pytest.fixture
def expected_resize() -> Path:
    return TEST_FOLDER / "logo/logo_resized.png"


def test_autoscaler_resize(file, expected_resize):
    image_object = load_image(picture=file)
    width = int(image_object.width / 2)  # half the size

    scaler_aspect_ratio = AspectRatioSizer(img=image_object, width=width)

    scaler_aspect_ratio.width = width
    image_object = scaler_aspect_ratio.set_size()

    image_saver = SavePic(img=image_object)
    image_saver.save_image(suffix="_resized")

    # Check if processed image was created
    assert expected_resize.exists(), "Processed image file does not exist"

    new_image_width = image_object.width
    assert new_image_width == width, "Image was not scaled"

    # Clean up
    os.remove(expected_resize)


def test_manualscaler_resize(file, expected_resize):
    image_object = load_image(picture=file)
    width, height = 256, 256

    scaler_aspect_ratio = ManualSizer(img=image_object, width=width, height=height)
    image_object = scaler_aspect_ratio.set_size()

    image_saver = SavePic(img=image_object)
    image_saver.save_image(suffix="_resized")

    # Check if processed image was created
    assert expected_resize.exists(), "Processed image file does not exist"

    new_image_width = image_object.width
    new_image_height = image_object.height
    assert new_image_width == width, "Image width was not resized"
    assert new_image_height == height, "Image height was not resized"

    # Clean up
    os.remove(expected_resize)
