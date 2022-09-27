from navigator import Navigator


class Rover:
    """Represents rover with id and navigator"""

    def __init__(self, id_: int, navigator: Navigator) -> None:
        self.id_ = id_
        self.navigator = navigator

    def get_navigator(self) -> Navigator:
        return self.navigator
