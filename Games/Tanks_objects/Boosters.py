import pygame as pg
from Games import config


class Booster(pg.sprite.Sprite):
	def __init__(self, game, pos):
		super().__init__(game.boosters_group)
		self.size = 50, 50  # размер улучшения
		self.game = game
		self.f = 1
		self.image = pg.image.load('Games/Tanks_objects/data/images/fire1.png')  # картинка спрайта  # контур спрайта
		self.image = pg.transform.scale(self.image, self.size)
		self.image.set_colorkey(-1)
		self.image = self.image.convert_alpha()
		self.can_move = True
		self.pos = pos[0] * config.TILE_SIZE, pos[1] * config.TILE_SIZE
		self.step = 0
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = self.pos
		self.y = self.rect.y

	def set_can_move(self, f):
		self.can_move = f

	def update(self, *args):
		if 20 > self.step and self.f:
			self.step += 0.1
			self.y += 0.1
		elif self.step > 0:
			self.f = 0
			self.step -= 0.1
			self.y -= 0.1
		else:
			self.f = 1
		self.rect.y = self.y
		self.rect.y += 0.01 * self.f

		if self.game.main_tank in pg.sprite.spritecollide(self, self.game.tanks_group, False):
			print(9999)


	def is_collided_with(self, sprite):
		return self.rect.colliderect(sprite.rect)
