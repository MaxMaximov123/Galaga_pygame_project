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
		self.image0 = pg.image.load('data/Tanks/brick0.png').convert_alpha()  # картинка спрайта  # контур спрайта
		self.image_r = pg.image.load('data/Tanks/brick1.png').convert_alpha()  # картинка спрайта  # контур спрайта
		self.image_l = pg.image.load('data/Tanks/brick3.png').convert_alpha()  # картинка спрайта  # контур спрайта
		self.image_u = pg.image.load('data/Tanks/brick4.png').convert_alpha()  # картинка спрайта  # контур спрайта
		self.image_d = pg.image.load('data/Tanks/brick2.png').convert_alpha()  # картинка спрайта  # контур спрайта
		self.image0 = pg.transform.scale(self.image0, self.base_size)
		self.image_r = pg.transform.scale(self.image_r, (self.base_size[0] // 2, self.base_size[1]))
		self.image_l = pg.transform.scale(self.image_l, (self.base_size[0] // 2, self.base_size[1]))
		self.image_d = pg.transform.scale(self.image_d, (self.base_size[0], self.base_size[1] // 2))
		self.image_u = pg.transform.scale(self.image_u, (self.base_size[0], self.base_size[1] // 2))
		self.update()


	def update(self, *args):
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

	def is_collided_with(self, sprite):
		return self.rect.colliderect(sprite.rect)
