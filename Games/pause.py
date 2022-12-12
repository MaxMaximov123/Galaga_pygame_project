import pygame as pg
from Games import config
from Games.button import Button


class Frame(pg.sprite.Sprite):
	def __init__(self, pos, size):
		pg.sprite.Sprite.__init__(self)
		self.size = size  # размер кнопки
		self.pos = pos
		self.image = pg.image.load('Games/Galaga_objects/data/images/frame1.png').convert_alpha()  # картинка спрайта
		self.image = pg.transform.scale(self.image, (self.size[0], self.size[1]))
		self.rect = self.image.get_rect(center=pos)  # контур спрайта


class Pause:
	def __init__(self, pos, screen):
		self.buttons = []
		self.screen = screen
		self.pause_group = pg.sprite.Group()
		self.btn_home = Button((config.WIDTH // 2, config.HEIGHT // 15 * 5), (300, 25), self.screen, text='Меню')
		self.pause_group = pg.sprite.Group(self.btn_home)

		self.btn_return = Button((config.WIDTH // 2, config.HEIGHT // 15 * 6), (300, 25), self.screen, text='Продолжить')
		self.pause_group.add(self.btn_return)
		self.pos = pos
		self.buttons.append(self.btn_home)
		self.buttons.append(self.btn_return)

		self.frame = Frame((config.WIDTH // 2, config.HEIGHT // 15 * 5 + 15), (400, len(self.buttons) * 60 + 30))
		self.pause_group.add(self.frame)

		self.buttons.append(self.frame)


	def update(self):
		pass
