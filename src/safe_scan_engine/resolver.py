"""
Module for Resolver interface
"""

from abc import ABC
from abc import abstractmethod


class Resolver(ABC):
    @abstractmethod
    def return_detections(self):
        pass
