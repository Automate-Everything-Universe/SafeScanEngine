import os
import subprocess
from pathlib import Path

import pytest

TEST_FOLDER = Path(__file__).parents[0]
MAIN = Path(__file__).parents[1] / "src/main.py"


@pytest.fixture
def file() -> Path:
    return TEST_FOLDER / "logo/logo.png"


@pytest.fixture
def input_path() -> Path:
    return TEST_FOLDER / "logo/"


@pytest.fixture
def expected_pillow() -> Path:
    return TEST_FOLDER / "logo/logo_converted_pillow.png"


@pytest.fixture
def expected_pillow_cropped() -> Path:
    return TEST_FOLDER / "logo/logo_converted_pillow_cropped.png"


@pytest.fixture
def expected_pillow_resized() -> Path:
    return TEST_FOLDER / "logo/logo_converted_pillow_resized.png"


# expected_pillow_c_and_r
@pytest.fixture
def expected_pillow_r_and_c() -> Path:
    return TEST_FOLDER / "logo/logo_converted_pillow_resized_cropped.png"


def test_cli_pillow(file, expected_pillow):
    command = ["python", str(MAIN), "--file", str(file), "--method", "pillow"]

    result = subprocess.run(command, capture_output=True, check=True, timeout=180, cwd=TEST_FOLDER)

    assert result.returncode == 0, f"Script failed with errors: {result.stderr}"

    assert expected_pillow.exists(), "Processed image file does not exist"

    # Clean up
    os.remove(expected_pillow)


def test_cli_pillow_cropped(file, expected_pillow_cropped):
    command = ["python", str(MAIN), "--file", str(file), "--method", "pillow", "--crop", "auto"]

    result = subprocess.run(command, capture_output=True, check=True, timeout=180, cwd=TEST_FOLDER)

    assert result.returncode == 0, f"Script failed with errors: {result.stderr}"

    assert expected_pillow_cropped.exists(), "Processed image file does not exist"

    # Clean up
    os.remove(expected_pillow_cropped)


def test_cli_pillow_resized(file, expected_pillow_resized):
    command = ["python", str(MAIN), "--file", str(file), "--method", "pillow", "--resize", "256"]

    result = subprocess.run(command, capture_output=True, check=True, timeout=180, cwd=TEST_FOLDER)

    assert result.returncode == 0, f"Script failed with errors: {result.stderr}"

    assert expected_pillow_resized.exists(), "Processed image file does not exist"

    # Clean up
    os.remove(expected_pillow_resized)


def test_cli_pillow_cropped_and_resized(file, expected_pillow_r_and_c):
    command = ["python", str(MAIN), "--file", str(file), "--method", "pillow", "--crop", "auto", "--resize", "256"]

    result = subprocess.run(command, capture_output=True, check=True, timeout=180, cwd=TEST_FOLDER)

    assert result.returncode == 0, f"Script failed with errors: {result.stderr}"

    assert expected_pillow_r_and_c.exists(), "Processed image file does not exist"

    # Clean up
    os.remove(expected_pillow_r_and_c)


def test_cli_folder_rembg_cropped_and_resized(input_path, expected_pillow_r_and_c):
    command = ["python", str(MAIN), "--folder", str(input_path), "--method", "pillow", "--crop", "auto", "--resize",
               "256"]

    result = subprocess.run(command, capture_output=True, check=True, timeout=180, cwd=TEST_FOLDER)

    assert result.returncode == 0, f"Script failed with errors: {result.stderr}"

    assert expected_pillow_r_and_c.exists(), "Processed image file does not exist"

    # Clean up
    os.remove(expected_pillow_r_and_c)
