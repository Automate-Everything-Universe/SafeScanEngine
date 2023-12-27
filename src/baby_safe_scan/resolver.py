"""
Module for Resolver interface
"""

from abc import ABC, abstractmethod
from typing import List


class Resolver(ABC):
    __slots__ = ['images']

    @abstractmethod
    def process_images(self):
        pass
