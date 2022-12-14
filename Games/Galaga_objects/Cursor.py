import pygame as pg
from Games import config


class Cursor:
	def __init__(self, screen):
		self.size = 15
		self.screen = screen
		self.pos = None
		self.color = pg.Color('white')

	def update_pos(self, pos):
		self.pos = pos
		self.draw()


	def draw(self):
		pg.draw.polygon(self.screen, self.color, (
			self.pos,
			(self.pos[0] - (self.size ** 2 - (self.size // 2) ** 2) ** 0.5, self.pos[1] - self.size // 2),
			(self.pos[0] - (self.size ** 2 - (self.size // 2) ** 2) ** 0.5, self.pos[1] + self.size // 2)
		))