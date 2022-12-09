import pygame as pg
from pprint import pprint
from Objects.Tanks_objects import Walls
from Objects import config
import copy


class Level1:
	def __init__(self, game):
		self.size = config.SIZE_BOARD_FOR_TANKS
		self.vis_board = [['0' for x in range(self.size[0])] for y in range(self.size[1])]
		self.vis_board = [
			['b', '0', '0', '0', '0', 'b', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'b'],
			['0', '0', 'br', '0', '0', 'b', '0', '0', 'b', 'b', 'b', 'b', 'b', 'b', '0', '0'],
			['0', '0', 'bl', '0', '0', 'b', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
			['0', '0', 'bu', 'bd', 'bu', 'b', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
			['0', '0', '0', '0', '0', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', '0', '0', '0'],
			['0', '0', '0', '0', '0', 'b', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
			['0', '0', '0', '0', 'b', 'b', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
			['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
			['b', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
		]
		# for i in self.board:
		# 	print(i)
		self.board = copy.deepcopy(self.vis_board)

		for y in range(len(self.vis_board)):
			for x in range(len(self.vis_board[0])):
				if self.vis_board[y][x] != '0':
					if 'b' in self.vis_board[y][x]:
						self.board[y][x] = Walls.Brick(game, (x, y), type_=self.vis_board[y][x])

		# for i in self.board:
		# 	print(i)



if __name__ == '__main__':
	pg.init()
	screen = pg.display.set_mode((config.WIDTH, config.WIDTH))
	group = pg.sprite.Group()
	l1 = Level1(screen)
	for y in range(len(l1.board)):
			for x in range(len(l1.board[0])):
				if l1.board[y][x] != '!':
					group.add(l1.board[y][x])
	while 1:
		group.draw(screen)
		group.update()
		pg.display.update()
