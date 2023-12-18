import os
from pathlib import Path

import pytest
from src.logo_bg_vanisher import AutoCropper
from src.logo_bg_vanisher import ManualCropper
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
def expected_crop() -> Path:
    return TEST_FOLDER / "logo/logo_cropped.png"


def test_auto_cropper(file, expected_crop):
    image_object = load_image(picture=file)

    width = image_object.width
    height = image_object.height

    auto_cropper = AutoCropper(img=image_object)
    image_object = auto_cropper.crop_image()

    image_saver = SavePic(img=image_object)
    image_saver.save_image(suffix="_cropped")

    # Check if processed image was created
    assert expected_crop.exists(), "Processed image file does not exist"

    new_image_width = image_object.width
    new_image_height = image_object.height
    assert new_image_width <= width, "Image width was not cropped"
    assert new_image_height <= height, "Image height was not cropped"

    # Clean up
    os.remove(expected_crop)


def test_manual_cropper(file, expected_crop):
    image_object = load_image(picture=file)
    width = image_object.width
    height = image_object.height

    crop_dimensions = (0, 0, 512, 512)

    manual_cropper = ManualCropper(img=image_object, dimensions=crop_dimensions)
    image_object = manual_cropper.crop_image()

    image_saver = SavePic(img=image_object)
    image_saver.save_image(suffix="_cropped")

    # Check if processed image was created
    assert expected_crop.exists(), "Processed image file does not exist"

    new_image_width = crop_dimensions[1]
    new_image_height = crop_dimensions[3]
    assert new_image_width <= width, "Image width was not cropped"
    assert new_image_height <= height, "Image height was not cropped"

    # Clean up
    os.remove(expected_crop)
