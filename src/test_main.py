import pygame
from pygame.locals import *
import unittest
import sys
from main import Game
from unittest.mock import patch
from io import StringIO
from hypothesis import given, strategies as st
from dataclasses import dataclass

@dataclass
class Data:
	x_value: st.SearchStrategy[int]

data = Data(x_value=st.integers(min_value=0, max_value=570)) #x values

class TestMain(unittest.TestCase):
	"""Unittests for Game class in main.py
	"""
	def setUp(self) -> None:
		"""Set up
		"""
		self.game = Game()
		
	def test_rockTotal(self) -> None:
		self.assertEqual(self.game.inventory.rockTotal,0)

	@given(x=st.integers(), y=st.integers())
	def test_player(self, x, y):
		"""Using hypothesis, assert starting player coords
		"""
		x = 100
		y = 100
		self.assertEqual(self.game.player.x, x)
		self.assertEqual(self.game.player.y, y)

	@given(st.data())
	def test_x(self, test_data: st.DataObject):
		"""Using hypothesis, assert x value is int
		"""
		random_int = test_data.draw(data.x_value)
		self.game.player.x = random_int
		assert isinstance(self.game.player.x, int)