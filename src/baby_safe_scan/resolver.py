"""
Module for Resolver interface
"""

from abc import ABC
from abc import abstractmethod


class Resolver(ABC):
    @abstractmethod
    def create_json_object(self):
        pass
