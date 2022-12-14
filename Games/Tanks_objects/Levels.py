import copy
import csv

import pygame as pg

from Games import config
from Games.Tanks_objects import Walls


class Level:
	def __init__(self, game, path):
		self.size = config.SIZE_BOARD_FOR_TANKS
		self.vis_board1 = [['0' for x in range(self.size[0])] for y in range(self.size[1])]


		with open(path, encoding="utf8") as csvfile:
			self.vis_board1 = list(csv.reader(csvfile, delimiter='\t', quotechar='"'))

		self.vis_board = []
		for y in range(self.size[1]):
			row = []
			for x in range(self.size[0]):
				if y >= len(self.vis_board1) or x >= len(self.vis_board1[0]):
					row.append('0')
				else:
					row.append(self.vis_board1[y][x])
			self.vis_board.append(row)
		self.board = copy.deepcopy(self.vis_board)

		for y in range(len(self.vis_board)):
			for x in range(len(self.vis_board[0])):
				if self.vis_board[y][x] != '0':
					if 'b' in self.vis_board[y][x]:
						self.board[y][x] = Walls.Brick(game, (x, y), type_=self.vis_board[y][x])
					if 'i' in self.vis_board[y][x]:
						self.board[y][x] = Walls.Iron(game, (x, y), type_=self.vis_board[y][x])
					if 'xz' in self.vis_board[y][x]:
						self.board[y][x] = Walls.IronXZ(game, (x, y), type_=self.vis_board[y][x])
					if 'w' in self.vis_board[y][x]:
						self.board[y][x] = Walls.Water(game, (x, y), type_=self.vis_board[y][x])
					if 'sh' in self.vis_board[y][x]:
						self.board[y][x] = Walls.Bush(game, (x, y), type_=self.vis_board[y][x])


if __name__ == '__main__':
	pg.init()
	screen = pg.display.set_mode((config.WIDTH, config.WIDTH))
	group = pg.sprite.Group()
	l1 = Level(screen, 'data/levels/level0.csv')
	for y in range(len(l1.board)):
		for x in range(len(l1.board[0])):
			if l1.board[y][x] != '!':
				group.add(l1.board[y][x])
	while 1:
		group.draw(screen)
		group.update()
		pg.display.update()
