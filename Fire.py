import pygame as pg
import config


class Fire(pg.sprite.Sprite):
	def __init__(self, path, pos):
		pg.sprite.Sprite.__init__(self)
		self.size = 50  # размер пули
		self.speed = 300  # скорость пули пикс/сек
		self.image = pg.image.load(path).convert_alpha()  # картинка спрайта
		self.image = pg.transform.scale(self.image, (self.size, self.size))
		self.rect = self.image.get_rect(center=pos)  # контур спрайта

	def update(self):
		# print(self.rect.y)
		if self.rect.y + self.size > 0:
			self.rect.y -= self.speed / config.FPS
		else:
			self.kill()
