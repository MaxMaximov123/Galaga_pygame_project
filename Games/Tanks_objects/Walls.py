import pygame as pg
from Games import config


class Wall:
	can_move = True

	def set_can_move(self, f):
		Wall.can_move = f


class Brick(pg.sprite.Sprite, Wall):
	def __init__(self, game, pos, type_='b'):
		super().__init__(game.walls_group)
		self.size = config.WIDTH // config.SIZE_BOARD_FOR_TANKS[0], config.WIDTH // config.SIZE_BOARD_FOR_TANKS[0]
		self.base_size = self.size
		self.game = game
		self.pos = pos
		self.type_ = type_
		self.image0 = pg.image.load('Games/Tanks_objects/data/images/brick.png').convert_alpha()  # картинка спрайта  # контур спрайта
		self.image_r = pg.image.load('Games/Tanks_objects/data/images/brickR.png').convert_alpha()  # картинка спрайта  # контур спрайта
		self.image_l = pg.image.load('Games/Tanks_objects/data/images/brickL.png').convert_alpha()  # картинка спрайта  # контур спрайта
		self.image_u = pg.image.load('Games/Tanks_objects/data/images/brickU.png').convert_alpha()  # картинка спрайта  # контур спрайта
		self.image_d = pg.image.load('Games/Tanks_objects/data/images/brickD.png').convert_alpha()  # картинка спрайта  # контур спрайта
		self.image0 = pg.transform.scale(self.image0, self.base_size)
		self.image_r = pg.transform.scale(self.image_r, (self.base_size[0] // 2, self.base_size[1]))
		self.image_l = pg.transform.scale(self.image_l, (self.base_size[0] // 2, self.base_size[1]))
		self.image_d = pg.transform.scale(self.image_d, (self.base_size[0], self.base_size[1] // 2))
		self.image_u = pg.transform.scale(self.image_u, (self.base_size[0], self.base_size[1] // 2))
		self.can_move = True
		self.update()


	def update(self, *args):
		self.render()
		self.tank_can_move()

	def is_collided_with(self, sprite):
		return self.rect.colliderect(sprite.rect)


	def tank_can_move(self):
		if pg.sprite.spritecollideany(self, self.game.tanks_group):
			pg.sprite.spritecollideany(self, self.game.tanks_group).set_can_move(False)

	def destruction(self, fire):
		if self.game.main_tank.rect.y + 5 >= self.rect.y + self.size[1]:
			if self.type_ == 'b':
				self.type_ = 'bu'
				return True
		if self.game.main_tank.rect.y + self.game.main_tank.size <= self.rect.y:
			if self.type_ == 'b':
				self.type_ = 'bd'
				return True


		if self.type_ == 'bu':
			self.kill()
			return True
		if self.type_ == 'bd':
			self.kill()
			return True


		if self.game.main_tank.rect.x >= self.rect.x + self.size[0]:
			if self.type_ == 'b':
				self.type_ = 'bl'
				return True
		if self.game.main_tank.rect.x + self.game.main_tank.size <= self.rect.x:
			if self.type_ == 'b':
				self.type_ = 'br'
				return True


		if self.type_ == 'br':
			self.kill()
			return True
		if self.type_ == 'bl':
			self.kill()
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


class Iron(pg.sprite.Sprite, Wall):
	def __init__(self, game, pos, type_='i'):
		super().__init__(game.walls_group)
		self.size = config.WIDTH // config.SIZE_BOARD_FOR_TANKS[0], config.WIDTH // config.SIZE_BOARD_FOR_TANKS[0]
		self.base_size = self.size
		self.game = game
		self.pos = pos
		self.type_ = type_
		self.image0 = pg.image.load('Games/Tanks_objects/data/images/iron.png').convert_alpha()  # картинка спрайта  # контур спрайта
		self.image_r = pg.image.load('Games/Tanks_objects/data/images/ironR.png').convert_alpha()  # картинка спрайта  # контур спрайта
		self.image_l = pg.image.load('Games/Tanks_objects/data/images/ironL.png').convert_alpha()  # картинка спрайта  # контур спрайта
		self.image_u = pg.image.load('Games/Tanks_objects/data/images/ironU.png').convert_alpha()  # картинка спрайта  # контур спрайта
		self.image_d = pg.image.load('Games/Tanks_objects/data/images/ironD.png').convert_alpha()  # картинка спрайта  # контур спрайта
		self.image0 = pg.transform.scale(self.image0, self.base_size)
		self.image_r = pg.transform.scale(self.image_r, (self.base_size[0] // 2, self.base_size[1]))
		self.image_l = pg.transform.scale(self.image_l, (self.base_size[0] // 2, self.base_size[1]))
		self.image_d = pg.transform.scale(self.image_d, (self.base_size[0], self.base_size[1] // 2))
		self.image_u = pg.transform.scale(self.image_u, (self.base_size[0], self.base_size[1] // 2))
		self.can_move = True
		self.update()


	def update(self, *args):
		self.render()

		self.tank_can_move()

	def is_collided_with(self, sprite):
		return self.rect.colliderect(sprite.rect)


	def tank_can_move(self):
		if pg.sprite.spritecollideany(self, self.game.tanks_group):
			pg.sprite.spritecollideany(self, self.game.tanks_group).set_can_move(False)


	def destruction(self, fire):
		if fire.from_main_tank and self.game.main_tank.power >= 3:
			if self.game.main_tank.rect.y + 5 >= self.rect.y + self.size[1]:
				if self.type_ == 'i':
					self.type_ = 'iu'
			if self.game.main_tank.rect.y + self.game.main_tank.size <= self.rect.y:
				if self.type_ == 'i':
					self.type_ = 'id'

			if self.type_ == 'iu':
				self.kill()
			if self.type_ == 'id':
				self.kill()

			if self.game.main_tank.rect.x >= self.rect.x + self.size[0]:
				if self.type_ == 'i':
					self.type_ = 'il'
			if self.game.main_tank.rect.x + self.game.main_tank.size <= self.rect.x:
				if self.type_ == 'i':
					self.type_ = 'ir'

			if self.type_ == 'ir':
				self.kill()
			if self.type_ == 'il':
				self.kill()
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


class IronXZ(pg.sprite.Sprite, Wall):
	def __init__(self, game, pos, type_='xz'):
		super().__init__(game.walls_group)
		self.size = config.WIDTH // config.SIZE_BOARD_FOR_TANKS[0], config.WIDTH // config.SIZE_BOARD_FOR_TANKS[0]
		self.base_size = self.size
		self.game = game
		self.pos = pos
		self.type_ = type_
		self.image0 = pg.image.load('Games/Tanks_objects/data/images/iron_xz.png').convert_alpha()  # картинка спрайта  # контур спрайта
		self.image0 = pg.transform.scale(self.image0, self.base_size)
		self.can_move = True
		self.update()


	def update(self, *args):
		self.render()
		self.tank_can_move()

	def is_collided_with(self, sprite):
		return self.rect.colliderect(sprite.rect)


	def tank_can_move(self):
		pass


	def destruction(self, fire):
		return False


	def render(self):
		if self.type_ == 'xz':
			self.image = self.image0
			self.rect = self.image.get_rect(center=self.pos)
			self.rect.x, self.rect.y = self.base_size[0] * self.pos[0], self.base_size[1] * self.pos[1]
			self.size = self.base_size


class Water(pg.sprite.Sprite, Wall):
	def __init__(self, game, pos, type_='w'):
		super().__init__(game.walls_group)
		self.size = config.WIDTH // config.SIZE_BOARD_FOR_TANKS[0], config.WIDTH // config.SIZE_BOARD_FOR_TANKS[0]
		self.base_size = self.size
		self.game = game
		self.pos = pos
		self.type_ = type_
		self.image0 = pg.image.load('Games/Tanks_objects/data/images/water.png').convert_alpha()  # картинка спрайта  # контур спрайта
		self.image0 = pg.transform.scale(self.image0, self.base_size)
		self.can_move = True
		self.update()


	def update(self, *args):
		self.render()
		self.tank_can_move()

	def is_collided_with(self, sprite):
		return self.rect.colliderect(sprite.rect)


	def tank_can_move(self):
		if pg.sprite.spritecollideany(self, self.game.tanks_group):
			pg.sprite.spritecollideany(self, self.game.tanks_group).set_can_move(False)


	def destruction(self, fire):
		return False


	def render(self):
		if self.type_ == 'w':
			self.image = self.image0
			self.rect = self.image.get_rect(center=self.pos)
			self.rect.x, self.rect.y = self.base_size[0] * self.pos[0], self.base_size[1] * self.pos[1]
			self.size = self.base_size


class Bush(pg.sprite.Sprite, Wall):
	def __init__(self, game, pos, type_='sh'):
		super().__init__(game.bush_group, game.walls_group)
		self.size = config.WIDTH // config.SIZE_BOARD_FOR_TANKS[0], config.WIDTH // config.SIZE_BOARD_FOR_TANKS[0]
		self.base_size = self.size
		self.game = game
		self.pos = pos
		self.type_ = type_
		self.image0 = pg.image.load('Games/Tanks_objects/data/images/bush.png').convert_alpha()  # картинка спрайта  # контур спрайта
		self.image0 = pg.transform.scale(self.image0, self.base_size)
		self.image0.set_colorkey((0, 0, 0))
		self.can_move = True
		self.update()


	def update(self, *args):
		self.render()
		self.tank_can_move()

	def is_collided_with(self, sprite):
		return self.rect.colliderect(sprite.rect)


	def tank_can_move(self):
		pass


	def destruction(self, fire):
		return False


	def render(self):
		if self.type_ == 'sh':
			self.image = self.image0
			self.rect = self.image.get_rect(center=self.pos)
			self.rect.x, self.rect.y = self.base_size[0] * self.pos[0], self.base_size[1] * self.pos[1]
			self.size = self.base_size