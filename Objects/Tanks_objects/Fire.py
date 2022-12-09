import pygame as pg
from Objects import config


class Fire(pg.sprite.Sprite):
	def __init__(self, game,  path, pos, vector_x=0, vector_y=1):
		pg.sprite.Sprite.__init__(self)
		self.step_show = 1
		self.frame_counter = self.step_show // config.FPS
		self.size = 20, 50  # размер пули
		self.speed = config.FPS * 2  # скорость пули пикс/сек
		self.game = game
		self.image = pg.image.load(path).convert_alpha()  # картинка спрайта  # контур спрайта
		self.can_move = True
		self.vector_x = vector_x * self.speed
		self.vector_y = vector_y * self.speed
		self.image = pg.transform.scale(self.image, self.size)
		if vector_x == 1:
			angle = -90
		elif vector_x == -1:
			angle = 90
		elif vector_y == 1:
			angle = 180
		else:
			angle = 0
		self.pos = pos
		self.image = pg.transform.rotate(self.image, angle)
		self.rect = self.image.get_rect(center=pos)

	def set_can_move(self, f):
		self.can_move = f

	def update(self, *args):
		if self.can_move:
			if config.HEIGHT > self.rect.y + self.size[1] > + self.size[1] and config.WIDTH + self.size[0] > self.rect.x + self.size[0] > 0:
				self.rect.y += self.vector_y / config.FPS
				self.rect.x += self.vector_x / config.FPS
			else:
				self.kill()

			for x, y in self.game.walls:
				if self.is_collided_with(self.game.level.board[y][x]) and 'b' in self.game.level.vis_board[y][x]:
					try:
						if self.game.main_tank.rect.y >= self.game.level.board[y][x].rect.y + self.game.level.board[y][x].size[1]:
							if self.game.level.board[y][x].type_ == 'b':
								self.game.level.board[y][x].type_ = 'bu'
								self.game.level.vis_board[y][x] = 'bu'
								return
						if self.game.main_tank.rect.y + self.game.main_tank.size <= self.game.level.board[y][x].rect.y:
							if self.game.level.board[y][x].type_ == 'b':
								self.game.level.board[y][x].type_ = 'bd'
								self.game.level.vis_board[y][x] = 'bd'
								return


						if self.game.level.board[y][x].type_ == 'bu':
							self.game.walls.remove([x, y])
							self.game.level.board[y][x].kill()
							self.game.level.board[y][x] = self.game.level.vis_board[y][x] = '0'
							return
						if self.game.level.board[y][x].type_ == 'bd':
							self.game.walls.remove([x, y])
							self.game.level.board[y][x].kill()
							self.game.level.board[y][x] = self.game.level.vis_board[y][x] = '0'
							return


						if self.game.main_tank.rect.x >= self.game.level.board[y][x].rect.x + self.game.level.board[y][x].size[0]:
							if self.game.level.board[y][x].type_ == 'b':
								self.game.level.board[y][x].type_ = 'bl'
								self.game.level.vis_board[y][x] = 'bl'
								return
						if self.game.main_tank.rect.x + self.game.main_tank.size <= self.game.level.board[y][x].rect.x:
							if self.game.level.board[y][x].type_ == 'b':
								self.game.level.board[y][x].type_ = 'br'
								self.game.level.vis_board[y][x] = 'br'
								return


						if self.game.level.board[y][x].type_ == 'br':
							self.game.walls.remove([x, y])
							self.game.level.board[y][x].kill()
							self.game.level.board[y][x] = self.game.level.vis_board[y][x] = '0'
							return
						if self.game.level.board[y][x].type_ == 'bl':
							self.game.walls.remove([x, y])
							self.game.level.board[y][x].kill()
							self.game.level.board[y][x] = self.game.level.vis_board[y][x] = '0'
							return

					finally:
						self.kill()


	def is_collided_with(self, sprite):
		return self.rect.colliderect(sprite.rect)
