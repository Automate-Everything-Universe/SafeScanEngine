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
def expected_rembg() -> Path:
    return TEST_FOLDER / "logo/logo_converted_rembg.png"


@pytest.fixture
def expected_rembg_cropped() -> Path:
    return TEST_FOLDER / "logo/logo_converted_rembg_cropped.png"


@pytest.fixture
def expected_rembg_resized() -> Path:
    return TEST_FOLDER / "logo/logo_converted_rembg_resized.png"


# expected_rembg_c_and_r
@pytest.fixture
def expected_rembg_r_and_c() -> Path:
    return TEST_FOLDER / "logo/logo_converted_rembg_resized_cropped.png"


def test_cli_rembg(file, expected_rembg):
    command = ["python", str(MAIN), "--file", str(file), "--method", "rembg"]

    result = subprocess.run(command, capture_output=True, check=True, timeout=180, cwd=TEST_FOLDER)

    assert result.returncode == 0, f"Script failed with errors: {result.stderr}"

    assert expected_rembg.exists(), "Processed image file does not exist"

    # Clean up
    os.remove(expected_rembg)


def test_cli_rembg_cropped(file, expected_rembg_cropped):
    command = ["python", str(MAIN), "--file", str(file), "--method", "rembg", "--crop", "auto"]

    result = subprocess.run(command, capture_output=True, check=True, timeout=180, cwd=TEST_FOLDER)

    assert result.returncode == 0, f"Script failed with errors: {result.stderr}"

    assert expected_rembg_cropped.exists(), "Processed image file does not exist"

    # Clean up
    os.remove(expected_rembg_cropped)


def test_cli_rembg_resized(file, expected_rembg_resized):
    command = ["python", str(MAIN), "--file", str(file), "--method", "rembg", "--resize", "256"]

    result = subprocess.run(command, capture_output=True, check=True, timeout=180, cwd=TEST_FOLDER)

    assert result.returncode == 0, f"Script failed with errors: {result.stderr}"

    assert expected_rembg_resized.exists(), "Processed image file does not exist"

    # Clean up
    os.remove(expected_rembg_resized)


def test_cli_rembg_cropped_and_resized(file, expected_rembg_r_and_c):
    command = ["python", str(MAIN), "--file", str(file), "--method", "rembg", "--crop", "auto", "--resize", "256"]

    result = subprocess.run(command, capture_output=True, check=True, timeout=180, cwd=TEST_FOLDER)

    assert result.returncode == 0, f"Script failed with errors: {result.stderr}"

    assert expected_rembg_r_and_c.exists(), "Processed image file does not exist"

    # Clean up
    os.remove(expected_rembg_r_and_c)


def test_cli_folder_rembg_cropped_and_resized(input_path, expected_rembg_r_and_c):
    command = ["python", str(MAIN), "--folder", str(input_path), "--method", "rembg", "--crop", "auto", "--resize",
               "256"]

    result = subprocess.run(command, capture_output=True, check=True, timeout=180, cwd=TEST_FOLDER)

    assert result.returncode == 0, f"Script failed with errors: {result.stderr}"

    assert expected_rembg_r_and_c.exists(), "Processed image file does not exist"

    # Clean up
    os.remove(expected_rembg_r_and_c)
