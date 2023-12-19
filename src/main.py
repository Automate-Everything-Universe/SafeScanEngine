"""
Main entry for CLI
"""
import argparse
from pathlib import Path


def parse_arguments():
    """
    Parses user arguments
    :return:
    """
    parser = argparse.ArgumentParser(
        prog='LogoBgVanisher',
        description='Can do the following image processing operations:\n'
                    '- Makes image background transparent (method: pillow)\n'
                    '- Removes image background (method: rembg)\n'
                    '- Resizes image\n'
                    '- Crops image\n'
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", help="File absolute path")
    group.add_argument("--folder", help="Folder absolute path")

    parser.add_argument("--method", choices=["pillow", "rembg"], required=True, help="Background removal method")
    parser.add_argument("--resize", help="Resize the image. Format: 'width,height' or 'width' for aspect ratio")
    parser.add_argument("--crop", help="Crop the image. Use 'auto' for autocrop or 'width,height' for manual crop")
    parser.add_argument('--verbose', action='store_true', help="Debug mode")
    return parser.parse_args()


def _process_image(pic: Path, user_args: argparse.Namespace) -> None:
    image_object = load_image(picture=pic)
    suffix = ""
    # Background removal
    if user_args.method == "pillow":
        remover = PillowBackgroundRemoval(img=image_object)
        image_object = remover.remove_background()
        suffix = suffix + "_converted_pillow"
    elif user_args.method == "rembg":
        remover = RembgBackgroundRemoval(img=image_object)
        image_object = remover.remove_background()
        suffix = suffix + "_converted_rembg"

    # Resize
    if user_args.resize:
        if ',' in user_args.resize:
            width, height = user_args.resize.split(',')
            scaler = ManualSizer(img=image_object, width=width, height=height)
            scaler.width = width
            scaler.height = height
            image_object = scaler.set_size()
            suffix = suffix + "_resized"
        else:
            width = user_args.resize
            scaler = AspectRatioSizer(img=image_object, width=width)
            image_object = scaler.set_size()
            suffix = suffix + "_resized"

    # Crop
    if user_args.crop:
        if ',' in user_args.crop:
            cropper = ManualCropper(img=image_object)
            cropper.dimensions = tuple(map(int, user_args.crop.split(',')))
            image_object = cropper.crop_image()
            suffix = suffix + "_cropped"
        elif user_args.crop.lower() == 'auto':
            cropper = AutoCropper(img=image_object)
            image_object = cropper.crop_image()
            suffix = suffix + "_cropped"

    image_saver = SavePic(img=image_object)
    image_saver.save_image(suffix=suffix)


def main() -> int:
    """
    Main entry for the CLI
    :return: None
    """
    try:
        args = parse_arguments()
        file = Path(args.file) if args.file else None
        folder = Path(args.folder) if args.folder else None

        if args.verbose:
            print("Done!")
            return 0
    except ValueError as exc:
        print(f"Invalid value provided: {exc}")
        return 1
    except FileNotFoundError as exc:
        print(f"The file was not found: {exc}")
        return 1
    except PermissionError as exc:
        print(f"Permission denied for file: {exc}")
        return 1
    except OSError as exc:
        print(f"An error occurred while opening the file: {exc}")
        return 1
    except Exception as exc:
        print(f"An unexpected error occurred: {exc}")
        return 1


if __name__ == "__main__":
    main()
