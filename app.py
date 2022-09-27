import sys
from pathlib import Path

from mission import Mission
from commandline_data_service import CommandlineDataService
from file_data_service import FileDataService
from exceptions import FileFormatError, CollisionException


def app(filepath: Path) -> None:
    if filepath:
        mission = Mission(FileDataService(filepath))
    else:
        mission = Mission(CommandlineDataService.get_user_input())

    for rover in mission.get_rovers():
        rover.get_navigator().execute_instructions()
        print(f'Rover{rover.id_}: {rover.get_navigator()}')


if __name__ == '__main__':
    path = None
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        try:
            path = Path(__file__).with_name(filename)
        except ValueError as e:
            sys.exit(e)
    try:
        app(path)
    except (ValueError, FileFormatError, CollisionException) as e:
        print(e)
