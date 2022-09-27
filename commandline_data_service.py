import sys
from typing import List

from data_service import DataService
from plateau import Plateau
from rover import Rover
from navigator import Navigator


class CommandlineDataService(DataService):
    """ Service for reading data from the command line """

    def __init__(self, plateau: Plateau) -> None:
        super().__init__()
        self.rovers: List[Rover] = []
        self.plateau = plateau

    def add_rover(self, rover: Rover) -> None:
        self.rovers.append(rover)

    def get_plateau(self) -> Plateau:
        return self.plateau

    def get_rovers(self) -> List:
        return self.rovers

    @classmethod
    def get_user_input(cls):
        """
        Read User Input
        :return:
        """
        print('Please input plateau and rover information. When done type "done". Type "exit" to exit.')
        plateau_raw = input('Plateau:')

        if plateau_raw == 'exit':
            sys.exit('Good bye!')

        plateau_dict = DataService.parse_plateau_data(plateau_raw)
        plateau = Plateau(plateau_dict['x'], plateau_dict['y'])

        input_data_source = cls(plateau)
        i = 1
        while True:

            position_raw = input(f'Rover{i} Landing:').strip()
            if not CommandlineDataService.process_user_actions(position_raw):
                break

            instructions_raw = input(f'Rover{i} Instructions:').strip()
            if not CommandlineDataService.process_user_actions(position_raw):
                break

            position = DataService.parse_position_data(position_raw)

            navigator = Navigator(plateau, position, i)
            navigator.set_instructions(instructions_raw.strip())
            rover = Rover(i, navigator)
            input_data_source.add_rover(rover)
            i += 1
        return input_data_source

    @staticmethod
    def process_user_actions(raw_input: str):
        """
        Process user commands to submit or to exit the app
        :param raw_input:
        :return:
        """
        if raw_input == 'exit':
            sys.exit('Good Bye! Mission Aborted')
        elif raw_input == 'done':
            return False
        return True
