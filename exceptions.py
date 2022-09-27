class FileFormatError(Exception):
    """ Custom exception for wrong formatted file """

    def __init__(self, message: str = 'File format is not correct, refer to the documentation!') -> None:
        super().__init__(message)


class CollisionException(Exception):
    """ Custom exception for collision of objects on the plateau """

    def __init__(self, message: str = 'There is another object at that location') -> None:
        super().__init__(message)


