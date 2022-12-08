import pygame as pg
from Objects import config


class Brick0(pg.sprite.Sprite):
	def __init__(self, screen, pos):
		pg.sprite.Sprite.__init__(self)
		self.size = config.WIDTH // config.SIZE_BOARD_FOR_TANKS[0]
		self.screen = screen
		self.image = pg.image.load('data/Tanks/brick0.png').convert_alpha()  # картинка спрайта  # контур спрайта
		self.image = pg.transform.scale(self.image, (self.size, self.size))
		self.rect = self.image.get_rect(center=pos)
		self.rect.x, self.rect.y = self.size * pos[0], self.size * pos[1]


	def update(self):
		pass

	def is_collided_with(self, sprite):
		return self.rect.colliderect(sprite.rect)


class Brick1(pg.sprite.Sprite):
	def __init__(self, screen, pos):
		pg.sprite.Sprite.__init__(self)
		self.size = config.WIDTH // config.SIZE_BOARD_FOR_TANKS[0]
		self.screen = screen
		self.image = pg.image.load('data/Tanks/brick1.png').convert_alpha()  # картинка спрайта  # контур спрайта
		self.image = pg.transform.scale(self.image, (self.size // 2, self.size))
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = self.size * pos[0] + self.size // 2, self.size * pos[1]


	def update(self):
		pass

	def is_collided_with(self, sprite):
		return self.rect.colliderect(sprite.rect)


class Brick2(pg.sprite.Sprite):
	def __init__(self, screen, pos):
		pg.sprite.Sprite.__init__(self)
		self.size = config.WIDTH // config.SIZE_BOARD_FOR_TANKS[0]
		self.screen = screen
		self.image = pg.image.load('data/Tanks/brick2.png').convert_alpha()  # картинка спрайта  # контур спрайта
		self.image = pg.transform.scale(self.image, (self.size, self.size // 2))
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = self.size * pos[0], self.size * pos[1] + self.size // 2


	def update(self):
		pass

	def is_collided_with(self, sprite):
		return self.rect.colliderect(sprite.rect)


class Brick3(pg.sprite.Sprite):
	def __init__(self, screen, pos):
		pg.sprite.Sprite.__init__(self)
		self.size = config.WIDTH // config.SIZE_BOARD_FOR_TANKS[0]
		self.screen = screen
		self.image = pg.image.load('data/Tanks/brick3.png').convert_alpha()  # картинка спрайта  # контур спрайта
		self.image = pg.transform.scale(self.image, (self.size // 2, self.size))
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = self.size * pos[0], self.size * pos[1]


	def update(self):
		pass

	def is_collided_with(self, sprite):
		return self.rect.colliderect(sprite.rect)



class Brick4(pg.sprite.Sprite):
	def __init__(self, screen, pos):
		pg.sprite.Sprite.__init__(self)
		self.size = config.WIDTH // config.SIZE_BOARD_FOR_TANKS[0]
		self.screen = screen
		self.image = pg.image.load('data/Tanks/brick4.png').convert_alpha()  # картинка спрайта  # контур спрайта
		self.image = pg.transform.scale(self.image, (self.size, self.size // 2))
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = self.size * pos[0], self.size * pos[1]


	def update(self):
		pass

	def is_collided_with(self, sprite):
		return self.rect.colliderect(sprite.rect)
