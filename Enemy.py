import pygame as pg
import config
import random


class Enemy1(pg.sprite.Sprite):
	def __init__(self, path, pos, pos1):
		pg.sprite.Sprite.__init__(self)
		self.size = 30  # размер врага
		self.step = 30  # кол-во пикселей, на которое двигается корабль
		self.image = pg.image.load(path).convert_alpha()  # картинка спрайта
		self.image = pg.transform.scale(self.image, (self.size, self.size))
		self.rect = self.image.get_rect(center=pos)
		self.move = 0
		self.speed = 10
		self.os1 = pos
		self.can_move = True

	def update(self):
		if self.can_move:
			if self.move == config.FPS // self.speed:
				random.choice([self.left_move, self.right_move, self.up_move, self.down_move])()
				self.move = 0
			self.move += 1



	def left_move(self):  # движение влево
		if self.rect.x > self.step:
			self.rect.x -= self.step

	def right_move(self):  # движение вправо
		if self.rect.x + self.step < config.WIDTH - self.step:
			self.rect.x += self.step


	def up_move(self):  # движение влево
		if self.rect.y > self.step:
			self.rect.y -= self.step

	def down_move(self):  # движение вправо
		if self.rect.y + self.step < config.HEIGHT - self.size:
			self.rect.y += self.step


	def is_collided_with(self, sprite):
		return self.rect.colliderect(sprite.rect)