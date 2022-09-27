from exceptions import CollisionException


class Plateau:
    """ Represents Plateau with max x, y size"""

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.validate_plateau_size()

        # plateau max size should be inclusive as rovers can be located on 0 and on max size hence + 1
        self.obstacles = [[0] * (self.x + 1) for i in range(self.y + 1)]

    def set_item_location(self, rover_id: int, x: int, y: int) -> None:
        self.obstacles[x][y] = rover_id

    def get_obstacles(self):
        return self.obstacles

    def get_item_id_by_coords(self, x: int, y: int) -> int:
        return self.obstacles[x][y]

    def move_item_location(self, rover_id: int, x: int, y: int, next_x: int, next_y: int) -> None:
        if self.obstacles[x][y] != rover_id:
            raise CollisionException(f"Rover{rover_id} location busy with item {self.obstacles[x][y]}")
        self.obstacles[x][y] = 0
        self.obstacles[next_x][next_y] = rover_id

    def validate_plateau_size(self) -> None:
        if self.x < 0 or self.y < 0:
            raise ValueError('Wrong Plateau Size')
