import unittest
from navigator import Navigator
from plateau import Plateau
from rover import Rover
from exceptions import CollisionException


class TestNavigator(unittest.TestCase):

    def setUp(self) -> None:
        rover1_id = 1
        self.plateau = Plateau(6, 6)
        self.plateau.set_item_location(rover1_id, 3, 3)

        self.navigator1 = Navigator(self.plateau, {'x': 3, 'y': 3, 'c': 'N'}, rover1_id)
        self.navigator1.set_instructions('MMM')
        self.rover1 = Rover(rover1_id, self.navigator1)

    def tearDown(self) -> None:
        pass

    def test_validate_instructions(self):
        with self.assertRaises(ValueError):
            self.navigator1.validate_instructions('K')
        self.assertTrue(self.navigator1.validate_instructions('RLM'))

    def test_validate_position(self):
        with self.assertRaises(ValueError):
            self.navigator1.validate_position({'x': 3, 'y': 3, 'c': 'K'})
        self.assertTrue(self.navigator1.validate_position({'x': 3, 'y': 3, 'c': 'N'}))

    def test_execute_instructions(self):
        self.navigator1.set_instructions('MMM')
        self.plateau.set_item_location(1, 3, 3)
        self.assertEqual(self.navigator1.execute_instructions().get_position(), {'x': 3, 'y': 6, 'c': 'N'})

    def test_get_next_position(self):
        self.navigator1.set_position({'x': 2, 'y': 2, 'c': 'E'})
        self.assertEqual(self.navigator1.get_next_position(), (3, 2))

    def test_validate_plateau_inbound(self):
        with self.assertRaises(ValueError):
            self.navigator1.validate_plateau_inbound(7, 6)

        self.assertTrue(self.navigator1.validate_plateau_inbound(4, 6))

    def test_validate_collision_avoidance(self):

        with self.assertRaises(CollisionException):
            self.navigator1.validate_collision_avoidance(3, 3)

    def test_move(self):
        self.plateau.set_item_location(1, 2, 2)
        self.navigator1.set_position({'x': 2, 'y': 2, 'c': 'E'})
        self.assertEqual(self.navigator1.move(2, 3).get_position(), {'x': 2, 'y': 3, 'c': 'E'})

    def test_turn_left(self):
        self.navigator1.position = {'x': 3, 'y': 3, 'c': 'N'}
        self.navigator1.turn_left()
        self.assertEqual(self.navigator1.position['c'], 'W')
        self.navigator1.turn_left()
        self.assertEqual(self.navigator1.position['c'], 'S')
        self.navigator1.turn_left()
        self.assertEqual(self.navigator1.position['c'], 'E')
        self.navigator1.turn_left()
        self.assertEqual(self.navigator1.position['c'], 'N')

    def test_turn_right(self):
        self.navigator1.position = {'x': 3, 'y': 3, 'c': 'N'}
        self.navigator1.turn_right()
        self.assertEqual(self.navigator1.position['c'], 'E')
        self.navigator1.turn_right()
        self.assertEqual(self.navigator1.position['c'], 'S')
        self.navigator1.turn_right()
        self.assertEqual(self.navigator1.position['c'], 'W')
        self.navigator1.turn_right()
        self.assertEqual(self.navigator1.position['c'], 'N')


if __name__ == '__main__':
    unittest.main()
