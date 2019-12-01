from abc import ABC, abstractmethod


class DataWrapper(ABC):
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return self.data

    @staticmethod
    @abstractmethod
    def factory(data): pass
