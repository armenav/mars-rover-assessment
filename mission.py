from typing import List

from data_service import DataService
from plateau import Plateau
from rover import Rover
from exceptions import CollisionException


class Mission:
    """ Represents the Mission with Plateau and Rovers """

    def __init__(self, data_service: DataService) -> None:
        self.source = data_service
        self.plateau: Plateau = data_service.get_plateau()
        self.rovers: List[Rover] = data_service.get_rovers()
        self.validate_mission()

    def validate_mission(self) -> 'Mission':
        """
        Validate that rovers are going to land in different locations
        :return:
        """
        for rover in self.rovers:
            position = rover.get_navigator().get_position()
            if self.plateau.get_item_id_by_coords(position['x'], position['y']) != 0:
                raise CollisionException('You are trying to land 2 rovers at the same location, aborting the mission!')
            else:
                self.plateau.set_item_location(rover.id_, position['x'], position['y'])
        return self

    def get_rovers(self) -> List:
        return self.rovers
