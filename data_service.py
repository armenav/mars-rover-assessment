from abc import ABC, abstractmethod
from typing import Dict


class DataService(ABC):
    """ An abstract dataservice class that requires get_rovers and get_plateau methods """

    def __init__(self):
        pass

    @abstractmethod
    def get_plateau(self):
        pass

    @abstractmethod
    def get_rovers(self):
        pass

    @staticmethod
    def parse_plateau_data(plateau_data_raw: str) -> Dict:
        plateau_data = plateau_data_raw.strip().split()
        try:
            x = int(plateau_data[0])
            y = int(plateau_data[1])
        except ValueError:
            raise ValueError('Plateau size should be defined with 2 integers')
        return {'x': x, 'y': y}

    @staticmethod
    def parse_position_data(position_data_raw: str) -> Dict:
        position_data = position_data_raw.strip().split()
        try:
            x = int(position_data[0])
            y = int(position_data[1])
            c = position_data[2]
        except ValueError:
            raise ValueError('Landing coordinates should be defined with 2 integers and a compass direction')
        return {'x': x, 'y': y, 'c': c}
