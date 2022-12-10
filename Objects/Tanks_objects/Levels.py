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
			['0', '0', '0', '0', '0', 'b', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'b'],
			['0', '0', 'br', '0', '0', 'b', '0', '0', 'b', 'b', 'b', 'b', 'b', 'b', '0', '0'],
			['0', '0', 'bl', '0', '0', 'b', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
			['0', '0', 'bu', 'bd', 'bu', 'b', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
			['0', '0', 'il', '0', '0', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', '0', '0', '0'],
			['0', '0', 'il', '0', '0', 'b', '0', '0', '0', '0', 'bd', 'bd', '0', '0', '0', '0'],
			['0', 'i', 'i', '0', 'b', 'b', '0', '0', '0', '0', '0', '0', 'bd', '0', '0', '0'],
			['0', '0', '0', 'bd', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'bd', '0', '0'],
			['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'bd', '0'],
		]
		# for i in self.board:
		# 	print(i)
		self.board = copy.deepcopy(self.vis_board)

		for y in range(len(self.vis_board)):
			for x in range(len(self.vis_board[0])):
				if self.vis_board[y][x] != '0':
					if 'b' in self.vis_board[y][x]:
						self.board[y][x] = Walls.Brick(game, (x, y), type_=self.vis_board[y][x])
					if 'i' in self.vis_board[y][x]:
						self.board[y][x] = Walls.Iron(game, (x, y), type_=self.vis_board[y][x])

		# for i in self.board:
		# 	print(i)


class Level2:
	def __init__(self, game):
		self.size = config.SIZE_BOARD_FOR_TANKS
		self.vis_board = [['0' for x in range(self.size[0])] for y in range(self.size[1])]
		self.vis_board = [
			['0', 'xz', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'iu', 'i', '0'],
			['w', 'w', '0', '0', 'bd', '0', 'bd', 'bl', 'bu', '0', 'b', '0', 'il', 'xz', 'br', 'ir'],
			['w', 'w', 'bu', 'b', 'bu', '0', 'bu', 'bu', 'br', 'bd', 'bl', 'i', 'xz', 'xz', 'xz', 'ir'],
			['w', 'br', '0', 'sh', 'sh', 'sh', '0', 'sh', '0', '0', '0', 'sh', 'xz', 'xz', 'xz', 'xz'],
			['xz', 'br', '0', '0', '0', '0', 'br', '0', '0', '0', '0', 'sh', 'xz', '0', 'ir', 'xz'],
			['xz', '0', 'bu', 'bd', 'bd', 'bd', 'bd', 'bd', 'bd', 'bd', 'bd', 'xz', 'xz', 'xz', 'ir', '0'],
			['xz', '0', '0', '0', 'b', '0', '0', 'sh', '0', '0', 'bl', 'br', '0', 'xz', 'xz', 'bl'],
			['w', 'xz', '0', 'b', '0', 'br', '0', '0', '0', '0', 'bl', '0', 'il', '0', 'xz', 'ir'],
			['w', 'bd', 'bd', '0', '0', '0', '0', '0', '0', 'bd', 'bd', '0', '0', 'iu', 'iu', '0'],
		]
		# for i in self.board:
		# 	print(i)
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
	l1 = Level1(screen)
	for y in range(len(l1.board)):
			for x in range(len(l1.board[0])):
				if l1.board[y][x] != '!':
					group.add(l1.board[y][x])
	while 1:
		group.draw(screen)
		group.update()
		pg.display.update()
