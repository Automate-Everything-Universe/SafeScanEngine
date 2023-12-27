"""
Module for Resolver interface
"""

from abc import ABC, abstractmethod


class Resolver(ABC):
    __slots__ = ['images']

    @abstractmethod
    def process_images(self):
        pass
