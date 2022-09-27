from typing import List
from pathlib import Path

from data_service import DataService
from plateau import Plateau
from rover import Rover
from navigator import Navigator
from exceptions import FileFormatError


class FileDataService(DataService):
    """ Represents the data service which reads mission data from a file and populates plateau and rovers"""

    def __init__(self, filepath: Path) -> None:
        super().__init__()
        self.plateau = None
        self.rovers = []
        self.read_file(filepath)

    def get_plateau(self) -> Plateau:
        return self.plateau

    def get_rovers(self) -> List:
        return self.rovers

    def read_file(self, filepath: Path) -> None:
        """
        Read the file with the given filepath.
        :param filepath:
        :return:
        """
        try:
            with filepath.open('r') as f:
                first_line = next(f)
                plateau_data_raw = FileDataService.parse_plateau_line(first_line)
                plateau_dict = DataService.parse_plateau_data(plateau_data_raw)
                self.plateau = Plateau(plateau_dict['x'], plateau_dict['y'])
                rover_id = 1
                for line in f:
                    position_raw = FileDataService.parse_position_line(rover_id, line.strip())
                    position = DataService.parse_position_data(position_raw)
                    navigator = Navigator(self.plateau, position, rover_id)
                    nextline = next(f)
                    navigator.set_instructions(FileDataService.parse_instructions_line(rover_id, nextline.strip()))
                    self.rovers.append(Rover(rover_id, navigator))
                    rover_id += 1
        except FileNotFoundError as e:
            print(e)

    @staticmethod
    def parse_plateau_line(plateau_line: str) -> str:
        """
        parse plateau line and make sure it has the correct label
        :param plateau_line:
        :return:
        """
        plateau_arr = plateau_line.strip().split(':')
        if plateau_arr[0] != 'Plateau':
            raise FileFormatError
        return plateau_arr[1]

    @staticmethod
    def parse_position_line(id_: int, position_line: str) -> str:
        """
        parse position line and make sure it has the correct label
        :param id_:
        :param position_line:
        :return:
        """
        position_arr = position_line.split(':')
        if position_arr[0] != f'Rover{id_} Landing':
            raise FileFormatError
        return position_arr[1]

    @staticmethod
    def parse_instructions_line(id_, instructions_raw: str) -> str:
        """
        parse instructions line and make sure it has the correct label
        :param id_:
        :param instructions_raw:
        :return:
        """
        instr_arr = instructions_raw.strip().split(':')
        if instr_arr[0] != f'Rover{id_} Instructions':
            raise FileFormatError
        return instr_arr[1].strip()
