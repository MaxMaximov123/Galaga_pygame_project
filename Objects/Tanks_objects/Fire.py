import pygame as pg
from Objects import config


class Fire(pg.sprite.Sprite):
	def __init__(self, screen,  path, pos, vector_x=0, vector_y=1):
		pg.sprite.Sprite.__init__(self)
		self.step_show = 1
		self.frame_counter = self.step_show // config.FPS
		self.size = 30, 40  # размер пули
		self.speed = config.FPS * 2  # скорость пули пикс/сек
		self.screen = screen
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
		self.image = pg.transform.rotate(self.image, angle)
		self.rect = self.image.get_rect(center=pos)

	def set_can_move(self, f):
		self.can_move = f

	def update(self):
		if self.can_move:
			if config.HEIGHT > self.rect.y + self.size[1] > + self.size[1] and config.WIDTH + self.size[0] > self.rect.x + self.size[0] > 0:
				self.rect.y += self.vector_y / config.FPS
				self.rect.x += self.vector_x / config.FPS
			else:
				self.kill()
			self.frame_counter += 1
			if self.frame_counter >= config.FPS:
				self.frame_counter = 0

	def is_collided_with(self, sprite):
		return self.rect.colliderect(sprite.rect)
