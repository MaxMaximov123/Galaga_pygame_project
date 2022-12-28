import pygame as pg
from Games import config
import random


# БАЗОВЫЙ КЛАСС СТЕНЫ
class Wall(pg.sprite.Sprite):
	can_move = True

	def __init__(self, game, pos, type_='b'):
		super().__init__(game.walls_group)
		self.pos = pos
		self.type = type_
		self.can_move = True
		self.x, self.y = config.TILE_SIZE * self.pos[0], config.TILE_SIZE * self.pos[1]

	def set_can_move(self, f):
		self.can_move = f

	def update(self, *args):
		self.render()

	def is_collided_with(self, sprite):
		return self.rect.colliderect(sprite.rect)

	def destruction(self, fire):
		return False

	def render(self):
		pass

	def tank_can_move(self):
		if pg.sprite.spritecollide(self, self.game.tanks_group, False):
			return True
		return False


# КЛАСС КИРПИЧНОЙ СТЕНКИ
class Brick(Wall):
	def __init__(self, game, pos, type_='b'):
		super().__init__(game, pos, type_=type_)
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

	# МЕХАНИКА РАЗРУШЕНИЙ
	def destruction(self, fire):
		if fire.vector_y < 0:
			if self.type_ == 'b':
				self.type_ = 'bu'
				return True
		if fire.vector_y > 0:
			if self.type_ == 'b':
				self.type_ = 'bd'
				return True

		if self.type_ == 'bu':
			self.kill()
			return True
		if self.type_ == 'bd':
			self.kill()
			return True

		if fire.vector_x < 0:
			if self.type_ == 'b':
				self.type_ = 'bl'
				return True
		if fire.vector_x > 0:
			if self.type_ == 'b':
				self.type_ = 'br'
				return True

		if self.type_ == 'br':
			self.kill()
			return True
		if self.type_ == 'bl':
			self.kill()
		return True

	# ОТРИСОВКА
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


# КЛАСС ЖЕЛЕЗНОЙ СТЕНКИ
class Iron(Wall):
	def __init__(self, game, pos, type_='i'):
		super().__init__(game, pos, type_=type_)
		self.size = config.WIDTH // config.SIZE_BOARD_FOR_TANKS[0], config.WIDTH // config.SIZE_BOARD_FOR_TANKS[0]
		self.base_size = self.size
		self.game = game
		self.pos = pos
		self.type_ = type_
		self.image0 = pg.image.load('Games/Tanks_objects/data/images/iron.png').convert_alpha()
		self.image_r = pg.image.load('Games/Tanks_objects/data/images/ironR.png').convert_alpha()
		self.image_l = pg.image.load('Games/Tanks_objects/data/images/ironL.png').convert_alpha()
		self.image_u = pg.image.load('Games/Tanks_objects/data/images/ironU.png').convert_alpha()
		self.image_d = pg.image.load('Games/Tanks_objects/data/images/ironD.png').convert_alpha()
		self.image0 = pg.transform.scale(self.image0, self.base_size)
		self.image_r = pg.transform.scale(self.image_r, (self.base_size[0] // 2, self.base_size[1]))
		self.image_l = pg.transform.scale(self.image_l, (self.base_size[0] // 2, self.base_size[1]))
		self.image_d = pg.transform.scale(self.image_d, (self.base_size[0], self.base_size[1] // 2))
		self.image_u = pg.transform.scale(self.image_u, (self.base_size[0], self.base_size[1] // 2))
		self.can_move = True
		self.update()

	# МЕХАНИКА РАЗРУШЕНИЯ
	def destruction(self, fire):
		if fire.from_main_tank and self.game.main_tank.power >= 3:
			if fire.vector_y < 0:
				if self.type_ == 'i':
					self.type_ = 'iu'
					return True
			if fire.vector_y > 0:
				if self.type_ == 'i':
					self.type_ = 'id'
					return True

			if self.type_ == 'iu':
				self.kill()
				return True
			if self.type_ == 'id':
				self.kill()
				return True

			if fire.vector_x < 0:
				if self.type_ == 'i':
					self.type_ = 'il'
					return True
			if fire.vector_x > 0:
				if self.type_ == 'i':
					self.type_ = 'ir'
					return True

			if self.type_ == 'ir':
				self.kill()
				return True
			if self.type_ == 'il':
				self.kill()
				return True
		return True

	# ОТРИСОВКА
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


# КЛАСС ВРОДЕ ЛЬДА(НЕ УВЕРЕН, ЧТО ЭТО ИМЕННО ЛЕД)
class IronXZ(pg.sprite.Sprite):
	def __init__(self, game, pos, type_='xz'):
		super().__init__(game.ice_group, game.walls_group)
		self.size = config.WIDTH // config.SIZE_BOARD_FOR_TANKS[0], config.WIDTH // config.SIZE_BOARD_FOR_TANKS[0]
		self.base_size = self.size
		self.game = game
		self.pos = pos
		self.type_ = type_
		self.image0 = pg.image.load('Games/Tanks_objects/data/images/iron_xz.png').convert_alpha()  # картинка спрайта  # контур спрайта
		self.image0 = pg.transform.scale(self.image0, self.base_size)
		self.can_move = True
		self.update()


	def tank_can_move(self):
		pass

	def destruction(self, fire):
		return False

	def set_can_move(self, f):
		self.can_move = f

	def update(self, *args):
		self.render()

	def is_collided_with(self, sprite):
		return self.rect.colliderect(sprite.rect)

	# ОТРИСОВКА
	def render(self):
		if self.type_ == 'xz':
			self.image = self.image0
			self.rect = self.image.get_rect(center=self.pos)
			self.rect.x, self.rect.y = self.base_size[0] * self.pos[0], self.base_size[1] * self.pos[1]
			self.size = self.base_size


# КЛАСС ВОДЫ
class Water(Wall):
	def __init__(self, game, pos, type_='w'):
		super().__init__(game, pos, type_=type_)
		self.size = config.WIDTH // config.SIZE_BOARD_FOR_TANKS[0], config.WIDTH // config.SIZE_BOARD_FOR_TANKS[0]
		self.base_size = self.size
		self.game = game
		self.pos = pos
		self.type_ = type_
		self.image0 = pg.image.load('Games/Tanks_objects/data/images/water.png').convert_alpha()  # картинка спрайта  # контур спрайта
		self.image0 = pg.transform.scale(self.image0, self.base_size)
		self.can_move = True
		self.update()

	def render(self):
		if self.type_ == 'w':
			self.image = self.image0
			self.rect = self.image.get_rect(center=self.pos)
			self.rect.x, self.rect.y = self.base_size[0] * self.pos[0], self.base_size[1] * self.pos[1]
			self.size = self.base_size


# КЛАСС КУСТА
class Bush(pg.sprite.Sprite):
	def __init__(self, game, pos, type_='sh'):
		super().__init__(game.bush_group)
		self.size = config.WIDTH // config.SIZE_BOARD_FOR_TANKS[0], config.WIDTH // config.SIZE_BOARD_FOR_TANKS[0]
		self.base_size = self.size
		self.game = game
		self.pos = pos
		self.type_ = type_
		if random.randint(0, 1) and 0:
			self.image0 = pg.image.load('Games/Tanks_objects/data/images/bush.png')  # картинка спрайта  # контур спрайта
		else:
			self.image0 = pg.image.load('Games/Tanks_objects/data/images/Christmas_tree.png')
		self.image0 = pg.transform.scale(self.image0, self.base_size)
		self.image0.set_colorkey((0, 0, 0))
		self.image0 = self.image0.convert_alpha()
		self.can_move = True
		self.update()

	def update(self, *args):
		self.render()
		self.tank_can_move()

	def render(self):
		if self.type_ == 'sh':
			self.image = self.image0
			self.rect = self.image.get_rect(center=self.pos)
			self.rect.x, self.rect.y = self.base_size[0] * self.pos[0], self.base_size[1] * self.pos[1]
			self.size = self.base_size

	def tank_can_move(self):
		pass

	def set_can_move(self, f):
		self.can_move = f


