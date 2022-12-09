import pygame as pg
from Objects import config


class Brick(pg.sprite.Sprite):
	def __init__(self, game, pos, type_='b'):
		pg.sprite.Sprite.__init__(self)
		self.size = config.WIDTH // config.SIZE_BOARD_FOR_TANKS[0], config.WIDTH // config.SIZE_BOARD_FOR_TANKS[0]
		self.base_size = self.size
		self.game = game
		self.pos = pos
		self.type_ = type_
		self.image0 = pg.image.load('data/Tanks/brick.png').convert_alpha()  # картинка спрайта  # контур спрайта
		self.image_r = pg.image.load('data/Tanks/brickR.png').convert_alpha()  # картинка спрайта  # контур спрайта
		self.image_l = pg.image.load('data/Tanks/brickL.png').convert_alpha()  # картинка спрайта  # контур спрайта
		self.image_u = pg.image.load('data/Tanks/brickU.png').convert_alpha()  # картинка спрайта  # контур спрайта
		self.image_d = pg.image.load('data/Tanks/brickD.png').convert_alpha()  # картинка спрайта  # контур спрайта
		self.image0 = pg.transform.scale(self.image0, self.base_size)
		self.image_r = pg.transform.scale(self.image_r, (self.base_size[0] // 2, self.base_size[1]))
		self.image_l = pg.transform.scale(self.image_l, (self.base_size[0] // 2, self.base_size[1]))
		self.image_d = pg.transform.scale(self.image_d, (self.base_size[0], self.base_size[1] // 2))
		self.image_u = pg.transform.scale(self.image_u, (self.base_size[0], self.base_size[1] // 2))
		self.update()


	def update(self, *args):
		self.render()

		self.tank_can_move()

	def is_collided_with(self, sprite):
		return self.rect.colliderect(sprite.rect)


	def tank_can_move(self):
		if self.game.main_tank.is_collided_with(self):
			self.game.main_tank_can_move = False

	def destruction(self, x, y):
		if self.game.main_tank.rect.y + 5 >= self.game.level.board[y][x].rect.y + self.game.level.board[y][x].size[1]:
			if self.game.level.board[y][x].type_ == 'b':
				self.game.level.board[y][x].type_ = 'bu'
				self.game.level.vis_board[y][x] = 'bu'
				return True
		if self.game.main_tank.rect.y + self.game.main_tank.size <= self.game.level.board[y][x].rect.y:
			if self.game.level.board[y][x].type_ == 'b':
				self.game.level.board[y][x].type_ = 'bd'
				self.game.level.vis_board[y][x] = 'bd'
				return True


		if self.game.level.board[y][x].type_ == 'bu':
			self.game.walls.remove([x, y])
			self.game.level.board[y][x].kill()
			self.game.level.board[y][x] = self.game.level.vis_board[y][x] = '0'
			return True
		if self.game.level.board[y][x].type_ == 'bd':
			self.game.walls.remove([x, y])
			self.game.level.board[y][x].kill()
			self.game.level.board[y][x] = self.game.level.vis_board[y][x] = '0'
			return True


		if self.game.main_tank.rect.x >= self.game.level.board[y][x].rect.x + self.game.level.board[y][x].size[0]:
			if self.game.level.board[y][x].type_ == 'b':
				self.game.level.board[y][x].type_ = 'bl'
				self.game.level.vis_board[y][x] = 'bl'
				return True
		if self.game.main_tank.rect.x + self.game.main_tank.size <= self.game.level.board[y][x].rect.x:
			if self.game.level.board[y][x].type_ == 'b':
				self.game.level.board[y][x].type_ = 'br'
				self.game.level.vis_board[y][x] = 'br'
				return True


		if self.game.level.board[y][x].type_ == 'br':
			self.game.walls.remove([x, y])
			self.game.level.board[y][x].kill()
			self.game.level.board[y][x] = self.game.level.vis_board[y][x] = '0'
			return True
		if self.game.level.board[y][x].type_ == 'bl':
			self.game.walls.remove([x, y])
			self.game.level.board[y][x].kill()
			self.game.level.board[y][x] = self.game.level.vis_board[y][x] = '0'
			return True


	def render(self):
		if self.type_ == 'b':
			self.image = self.image0
			self.rect = self.image.get_rect(center=self.pos)
			self.rect.x, self.rect.y = self.base_size[0] * self.pos[0], self.base_size[1] * self.pos[1]
			self.size = self.base_size
		elif self.type_ == 'br':
			self.image = self.image_r
			self.rect = self.image.get_rect()
			self.rect.x, self.rect.y = self.base_size[0] * self.pos[0] + self.base_size[0] // 2, self.base_size[1] * self.pos[1]
			self.size = self.base_size[0] // 2, self.base_size[1]
		elif self.type_ == 'bd':
			self.image = self.image_d
			self.rect = self.image.get_rect()
			self.rect.x, self.rect.y = self.base_size[0] * self.pos[0], self.base_size[1] * self.pos[1] + self.base_size[1] // 2
			self.size = self.base_size[0], self.base_size[1] // 2

		elif self.type_ == 'bl':
			self.image = self.image_l
			self.rect = self.image.get_rect()
			self.rect.x, self.rect.y = self.base_size[0] * self.pos[0], self.base_size[1] * self.pos[1]
			self.size = self.base_size[0] // 2, self.base_size[1]

		elif self.type_ == 'bu':
			self.image = self.image_u
			self.rect = self.image.get_rect()
			self.rect.x, self.rect.y = self.base_size[0] * self.pos[0], self.base_size[1] * self.pos[1]
			self.size = self.base_size[0], self.base_size[1] // 2

	def render(self):
		if self.type_ == 'b':
			self.image = self.image0
			self.rect = self.image.get_rect(center=self.pos)
			self.rect.x, self.rect.y = self.base_size[0] * self.pos[0], self.base_size[1] * self.pos[1]
			self.size = self.base_size
		elif self.type_ == 'br':
			self.image = self.image_r
			self.rect = self.image.get_rect()
			self.rect.x, self.rect.y = self.base_size[0] * self.pos[0] + self.base_size[0] // 2, self.base_size[1] * self.pos[1]
			self.size = self.base_size[0] // 2, self.base_size[1]
		elif self.type_ == 'bd':
			self.image = self.image_d
			self.rect = self.image.get_rect()
			self.rect.x, self.rect.y = self.base_size[0] * self.pos[0], self.base_size[1] * self.pos[1] + self.base_size[1] // 2
			self.size = self.base_size[0], self.base_size[1] // 2

		elif self.type_ == 'bl':
			self.image = self.image_l
			self.rect = self.image.get_rect()
			self.rect.x, self.rect.y = self.base_size[0] * self.pos[0], self.base_size[1] * self.pos[1]
			self.size = self.base_size[0] // 2, self.base_size[1]

		elif self.type_ == 'bu':
			self.image = self.image_u
			self.rect = self.image.get_rect()
			self.rect.x, self.rect.y = self.base_size[0] * self.pos[0], self.base_size[1] * self.pos[1]
			self.size = self.base_size[0], self.base_size[1] // 2


class Iron(pg.sprite.Sprite):
	def __init__(self, game, pos, type_='i'):
		pg.sprite.Sprite.__init__(self)
		self.size = config.WIDTH // config.SIZE_BOARD_FOR_TANKS[0], config.WIDTH // config.SIZE_BOARD_FOR_TANKS[0]
		self.base_size = self.size
		self.game = game
		self.pos = pos
		self.type_ = type_
		self.image0 = pg.image.load('data/Tanks/iron.png').convert_alpha()  # картинка спрайта  # контур спрайта
		self.image_r = pg.image.load('data/Tanks/ironR.png').convert_alpha()  # картинка спрайта  # контур спрайта
		self.image_l = pg.image.load('data/Tanks/ironL.png').convert_alpha()  # картинка спрайта  # контур спрайта
		self.image_u = pg.image.load('data/Tanks/ironU.png').convert_alpha()  # картинка спрайта  # контур спрайта
		self.image_d = pg.image.load('data/Tanks/ironD.png').convert_alpha()  # картинка спрайта  # контур спрайта
		self.image0 = pg.transform.scale(self.image0, self.base_size)
		self.image_r = pg.transform.scale(self.image_r, (self.base_size[0] // 2, self.base_size[1]))
		self.image_l = pg.transform.scale(self.image_l, (self.base_size[0] // 2, self.base_size[1]))
		self.image_d = pg.transform.scale(self.image_d, (self.base_size[0], self.base_size[1] // 2))
		self.image_u = pg.transform.scale(self.image_u, (self.base_size[0], self.base_size[1] // 2))
		self.update()


	def update(self, *args):
		self.render()

		self.tank_can_move()

	def is_collided_with(self, sprite):
		return self.rect.colliderect(sprite.rect)


	def tank_can_move(self):
		if self.game.main_tank.is_collided_with(self):
			self.game.main_tank_can_move = False

	def destruction(self, x, y):
		return True


	def render(self):
		if self.type_ == 'i':
			self.image = self.image0
			self.rect = self.image.get_rect(center=self.pos)
			self.rect.x, self.rect.y = self.base_size[0] * self.pos[0], self.base_size[1] * self.pos[1]
			self.size = self.base_size
		elif self.type_ == 'ir':
			self.image = self.image_r
			self.rect = self.image.get_rect()
			self.rect.x, self.rect.y = self.base_size[0] * self.pos[0] + self.base_size[0] // 2, self.base_size[1] * self.pos[1]
			self.size = self.base_size[0] // 2, self.base_size[1]
		elif self.type_ == 'id':
			self.image = self.image_d
			self.rect = self.image.get_rect()
			self.rect.x, self.rect.y = self.base_size[0] * self.pos[0], self.base_size[1] * self.pos[1] + self.base_size[1] // 2
			self.size = self.base_size[0], self.base_size[1] // 2

		elif self.type_ == 'il':
			self.image = self.image_l
			self.rect = self.image.get_rect()
			self.rect.x, self.rect.y = self.base_size[0] * self.pos[0], self.base_size[1] * self.pos[1]
			self.size = self.base_size[0] // 2, self.base_size[1]

		elif self.type_ == 'iu':
			self.image = self.image_u
			self.rect = self.image.get_rect()
			self.rect.x, self.rect.y = self.base_size[0] * self.pos[0], self.base_size[1] * self.pos[1]
			self.size = self.base_size[0], self.base_size[1] // 2


class IronXZ(pg.sprite.Sprite):
	def __init__(self, game, pos, type_='xz'):
		pg.sprite.Sprite.__init__(self)
		self.size = config.WIDTH // config.SIZE_BOARD_FOR_TANKS[0], config.WIDTH // config.SIZE_BOARD_FOR_TANKS[0]
		self.base_size = self.size
		self.game = game
		self.pos = pos
		self.type_ = type_
		self.image0 = pg.image.load('data/Tanks/iron_xz.png').convert_alpha()  # картинка спрайта  # контур спрайта
		self.image0 = pg.transform.scale(self.image0, self.base_size)
		self.update()


	def update(self, *args):
		self.render()
		self.tank_can_move()

	def is_collided_with(self, sprite):
		return self.rect.colliderect(sprite.rect)


	def tank_can_move(self):
		pass


	def destruction(self, x, y):
		return False


	def render(self):
		if self.type_ == 'xz':
			self.image = self.image0
			self.rect = self.image.get_rect(center=self.pos)
			self.rect.x, self.rect.y = self.base_size[0] * self.pos[0], self.base_size[1] * self.pos[1]
			self.size = self.base_size


class Water(pg.sprite.Sprite):
	def __init__(self, game, pos, type_='w'):
		pg.sprite.Sprite.__init__(self)
		self.size = config.WIDTH // config.SIZE_BOARD_FOR_TANKS[0], config.WIDTH // config.SIZE_BOARD_FOR_TANKS[0]
		self.base_size = self.size
		self.game = game
		self.pos = pos
		self.type_ = type_
		self.image0 = pg.image.load('data/Tanks/water.png').convert_alpha()  # картинка спрайта  # контур спрайта
		self.image0 = pg.transform.scale(self.image0, self.base_size)
		self.update()


	def update(self, *args):
		self.render()
		self.tank_can_move()

	def is_collided_with(self, sprite):
		return self.rect.colliderect(sprite.rect)


	def tank_can_move(self):
		if self.game.main_tank.is_collided_with(self):
			self.game.main_tank_can_move = False


	def destruction(self, x, y):
		return False


	def render(self):
		if self.type_ == 'w':
			self.image = self.image0
			self.rect = self.image.get_rect(center=self.pos)
			self.rect.x, self.rect.y = self.base_size[0] * self.pos[0], self.base_size[1] * self.pos[1]
			self.size = self.base_size


class Bush(pg.sprite.Sprite):
	def __init__(self, game, pos, type_='sh'):
		pg.sprite.Sprite.__init__(self)
		self.size = config.WIDTH // config.SIZE_BOARD_FOR_TANKS[0], config.WIDTH // config.SIZE_BOARD_FOR_TANKS[0]
		self.base_size = self.size
		self.game = game
		self.pos = pos
		self.type_ = type_
		self.image0 = pg.image.load('data/Tanks/bush.png').convert_alpha()  # картинка спрайта  # контур спрайта
		self.image0 = pg.transform.scale(self.image0, self.base_size)
		self.update()


	def update(self, *args):
		self.render()
		self.tank_can_move()

	def is_collided_with(self, sprite):
		return self.rect.colliderect(sprite.rect)


	def tank_can_move(self):
		pass


	def destruction(self, x, y):
		return False


	def render(self):
		if self.type_ == 'sh':
			self.image = self.image0
			self.rect = self.image.get_rect(center=self.pos)
			self.rect.x, self.rect.y = self.base_size[0] * self.pos[0], self.base_size[1] * self.pos[1]
			self.size = self.base_size