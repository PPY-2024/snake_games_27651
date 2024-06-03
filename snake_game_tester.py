import sys
import os
import unittest
from pygame.math import Vector2

current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.append(src_dir)

from src.main import FRUIT, SNAKE, MAIN

class TestSnake(unittest.TestCase):
    def setUp(self):
        self.snake = SNAKE()

    def test_snake_initialization(self):
        self.assertEqual(len(self.snake.body), 3)
        self.assertEqual(self.snake.direction, Vector2(0, 0))

    def test_snake_movement(self):
        initial_head_position = self.snake.body[0].copy()
        self.snake.direction = Vector2(1, 0)
        self.snake.move_snake()
        self.assertEqual(self.snake.body[0], initial_head_position + Vector2(1, 0))

    def test_snake_growth(self):
        initial_length = len(self.snake.body)
        self.snake.add_block()
        self.assertEqual(len(self.snake.body), initial_length + 1)

    def test_snake_reset(self):
        self.snake.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.snake.direction = Vector2(1, 0)
        self.snake.reset()
        self.assertEqual(len(self.snake.body), 3)
        self.assertEqual(self.snake.direction, Vector2(0, 0))

class TestFruit(unittest.TestCase):
    def setUp(self):
        self.fruit = FRUIT()

    def test_fruit_initialization(self):
        self.assertIsNotNone(self.fruit.pos)

    def test_fruit_randomize(self):
        initial_position = self.fruit.pos.copy()
        self.fruit.randomize()
        self.assertNotEqual(self.fruit.pos, initial_position)

class TestMain(unittest.TestCase):
    def setUp(self):
        self.main_game = MAIN()

    def test_collision_detection_fruit(self):
        initial_length = len(self.main_game.snake.body)
        self.main_game.fruit.pos = self.main_game.snake.body[0]
        self.main_game.check_collision()
        self.assertEqual(len(self.main_game.snake.body), initial_length + 1)

    def test_collision_detection_self(self):
        self.main_game.snake.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10), Vector2(3, 11)]
        self.assertTrue(self.main_game.check_fail())

    def test_collision_detection_wall(self):
        self.main_game.snake.body[0] = Vector2(-1, 10)
        self.assertTrue(self.main_game.check_fail())

    def test_update(self):
        initial_snake_position = self.main_game.snake.body[0].copy()
        self.main_game.update()
        self.assertNotEqual(self.main_game.snake.body[0], initial_snake_position)


if __name__ == '__main__':
    unittest.main()
