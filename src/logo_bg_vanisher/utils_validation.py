"""
Module to handle user validation
"""
from typing import Tuple, Union


def is_string_valid(text: str) -> str:
    """
    Validates if text is string
    :param text:
    :return: str
    """
    if not isinstance(text, str):
        raise ValueError("Input must be string!")
    return text


def are_numbers_valid(*args) -> Union[Tuple[int, ...], int]:
    """
    Validates that all provided arguments are integers.

    :param args: A variable number of arguments.
    :return: Tuple of the provided integers.
    :raises ValueError: If no arguments are provided or if any argument is not an integer.
    """
    if not args:
        raise ValueError("No arguments provided!")

    items = []
    try:
        if len(args) == 1:
            return int(args[0])
        for item in args:
            item = int(item)
            items.append(item)
        return tuple(items)
    except ValueError as exc :
        raise ValueError("Argument needs to be an integer") from exc
