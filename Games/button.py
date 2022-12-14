import pygame as pg
from Games import config


class Button(pg.sprite.Sprite):
	def __init__(self, pos, size, screen, path='Games/Galaga_objects/data/images/None.png', text=None, text_size=40):
		pg.sprite.Sprite.__init__(self)
		self.size = size  # размер кнопки
		self.text_size = text_size
		self.screen = screen
		self.text = text
		self.pos = pos
		self.can_move = True
		if path:
			self.image = pg.image.load(path).convert_alpha()  # картинка спрайта
			self.image = pg.transform.scale(self.image, (self.size[0], self.size[1]))
			self.rect = self.image.get_rect(center=pos)  # контур спрайта


	def is_click(self, pos):
		if self.rect.x + self.size[0] > pos[0] > self.rect.x and self.rect.y + self.size[1] > pos[1] > self.rect.y:
			return True
		return False


	def update(self):
		if self.text:
			font = pg.font.SysFont('monospace', round(self.text_size * 2 * config.K))
			text = font.render(self.text, True, (194, 152, 0))
			self.screen.blit(text, (self.pos[0] - text.get_width() // 2, self.pos[1] - text.get_height() // 2))

	def set_can_move(self, f):
		self.can_move = f