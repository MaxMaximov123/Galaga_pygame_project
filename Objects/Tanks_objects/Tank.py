import pygame as pg
from Objects import config


class Tank(pg.sprite.Sprite):
	def __init__(self, path, pos, screen):
		pg.sprite.Sprite.__init__(self)
		self.pos = pos
		self.size = 50  # размер танка
		self.speed = 360  # пикселе в секунду
		self.base_image = pg.image.load(path).convert_alpha()  # картинка спрайта
		self.base_image = pg.transform.scale(self.base_image, (self.size, self.size))
		self.image = self.base_image
		self.rect = self.image.get_rect(center=self.pos)  # контур спрайта
		self.screen = screen
		self.vector_x = 0
		self.vector_y = -1

	def update(self):
		pass


	def left_move(self):  # движение влево
		if self.rect.x > 15:
			self.image = pg.transform.rotate(self.base_image, 90)
			self.rect.x -= self.speed / config.FPS
			self.vector_x = -1
			self.vector_y = 0

	def right_move(self):  # движение вправо
		if self.rect.x + self.size < config.WIDTH - 15:
			self.image = pg.transform.rotate(self.base_image, -90)
			self.rect.x += self.speed / config.FPS
			self.vector_x = 1
			self.vector_y = 0


	def up_move(self):  # движение влево
		if self.rect.y > 15:
			self.image = pg.transform.rotate(self.base_image, 0)
			self.rect.y -= self.speed / config.FPS
			self.vector_x = 0
			self.vector_y = -1

	def down_move(self):  # движение вправо
		if self.rect.y + self.size < config.HEIGHT - 15:
			self.image = pg.transform.rotate(self.base_image, 180)
			self.rect.y += self.speed / config.FPS
			self.vector_x = 0
			self.vector_y = 1


	def is_collided_with(self, sprite):
		return self.rect.colliderect(sprite.rect)