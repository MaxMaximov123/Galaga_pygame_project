import pygame as pg
from pprint import pprint
from Objects.Tanks_objects import Walls
from Objects import config
import copy


walls = {
	'b0': Walls.Brick0,
	'b1': Walls.Brick1,
	'b2': Walls.Brick2,
	'b3': Walls.Brick3,
	'b4': Walls.Brick4
}


class Level1:
	def __init__(self, screen):
		self.size = config.SIZE_BOARD_FOR_TANKS
		self.vis_board = [['0' for x in range(self.size[0])] for y in range(self.size[1])]
		self.vis_board = [
			['b0', '0', '0', '0', '0', 'b1', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'b0'],
			['0', '0', '0', '0', '0', 'b1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
			['0', '0', '0', '0', '0', 'b1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
			['0', '0', '0', '0', '0', 'b1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
			['0', '0', '0', '0', '0', 'b0', 'b0', 'b0', 'b0', 'b0', 'b4', 'b4', 'b2', '0', '0', '0'],
			['0', '0', '0', '0', '0', 'b3', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
			['0', '0', '0', '0', 'b3', 'b3', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
			['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
			['b0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
		]
		# for i in self.board:
		# 	print(i)
		self.board = copy.deepcopy(self.vis_board)

		for y in range(len(self.vis_board)):
			for x in range(len(self.vis_board[0])):
				if self.vis_board[y][x] != '0':
					self.board[y][x] = walls[self.vis_board[y][x]](screen, (x, y))

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
