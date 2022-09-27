from typing import Dict
from plateau import Plateau
from exceptions import CollisionException


class Navigator:
    """
    Represents rover navigator with Plateau information, current position and rover_id
    """

    INSTRUCTIONS = 'LRM'
    DIRECTIONS = 'NESW'

    def __init__(self, plateau: Plateau, position: Dict, rover_id: int) -> None:
        self.plateau = plateau
        self.validate_position(position)
        self.position = position
        self.rover_id = rover_id
        self.instructions = ''

    def get_position(self) -> Dict:
        return self.position

    def set_position(self, position: Dict) -> None:
        self.position = position

    def set_instructions(self, instructions: str) -> None:
        self.validate_instructions(instructions)
        self.instructions = instructions

    def validate_instructions(self, instructions: str) -> bool:
        if not all(ch in Navigator.INSTRUCTIONS for ch in instructions):
            raise ValueError(f'Instruction Not Allowed for Rover: {self.rover_id}')
        return True

    def validate_position(self, position: dict) -> bool:
        if not self.validate_plateau_inbound(position['x'], position['y']) or position['c'] not in Navigator.DIRECTIONS:
            raise ValueError(f'Incorrect position for Rover {self.rover_id}')
        return True

    def execute_instructions(self):
        for i in self.instructions:
            if i == 'M':
                next_x, next_y = self.get_next_position()
                self.validate_plateau_inbound(next_x, next_y)
                self.validate_collision_avoidance(next_x, next_y)
                self.move(next_x, next_y)
            elif i == 'L':
                self.turn_left()
            elif i == 'R':
                self.turn_right()

        return self

    def get_next_position(self):
        x = self.position['x']
        y = self.position['y']
        if self.position['c'] == 'N':
            y += 1
        elif self.position['c'] == 'S':
            y -= 1
        elif self.position['c'] == 'W':
            x -= 1
        elif self.position['c'] == 'E':
            x += 1
        return x, y

    def validate_plateau_inbound(self, x: int, y: int) -> bool:
        if x < 0 or y < 0 or x > self.plateau.x or y > self.plateau.y:
            raise ValueError('Coordinates out of the plateau!')
        return True

    def validate_collision_avoidance(self, next_x: int, next_y: int) -> bool:
        if self.plateau.get_obstacles()[next_x][next_y] != 0:
            raise CollisionException(f'Rover can not move to {next_x}, {next_y} as there is an obstacle')
        return True

    def move(self, next_x: int, next_y: int) -> 'Navigator':
        self.plateau.move_item_location(self.rover_id, self.position['x'], self.position['y'], next_x, next_y)
        self.position['x'] = next_x
        self.position['y'] = next_y
        return self

    def turn_left(self):
        d = Navigator.DIRECTIONS
        new_index = d.find(self.position['c']) - 1 if d.find(self.position['c']) - 1 >= 0 else len(d) - 1
        self.position['c'] = d[new_index]

    def turn_right(self):
        d = Navigator.DIRECTIONS
        new_index = d.find(self.position['c']) + 1 if d.find(self.position['c']) + 1 < len(d) else 0
        self.position['c'] = d[new_index]

    def __str__(self):
        return f"{self.position['x']} {self.position['y']} {self.position['c']}"
