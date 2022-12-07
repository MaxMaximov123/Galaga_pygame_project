import pygame as pg
import config


class SpaceShip(pg.sprite.Sprite):
	def __init__(self, path, pos):
		pg.sprite.Sprite.__init__(self)
		self.size = 50  # размер корабля
		self.step = 30  # кол-во пикселей, на которое двигается корабль
		self.image = pg.image.load(path).convert_alpha()  # картинка спрайта
		self.image = pg.transform.scale(self.image, (self.size, self.size))
		self.rect = self.image.get_rect(center=pos)  # контур спрайта

	def update(self):
		pass


	def left_move(self):  # движение влево
		if self.rect.x > 10:
			self.rect.x -= self.step

	def right_move(self):  # движение вправо
		if self.rect.x + self.size < config.WIDTH - 10:
			self.rect.x += self.step


	def is_collided_with(self, sprite):
		return self.rect.colliderect(sprite.rect)