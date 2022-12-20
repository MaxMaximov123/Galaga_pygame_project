from random import randint
import pygame as pg
import sys
from Games import config



def print_kills(self):
	for j in range(len(self.vis_kills)):
		if self.vis_kills[j] < self.game.kill_counts[j]:
			self.vis_kills[j] += 0.02
			break
	for i in range(len(self.vis_kills)):
		if self.vis_kills[i] >= 0:
			font = pg.font.Font(None, 40)
			string_rendered = font.render(
				'     - >     ' + str(round(self.vis_kills[i])) +
				'    PTS    ' + str(round(self.vis_kills[i]) * 100 * (i + 1)), 1, pg.Color('white'))
			intro_rect = string_rendered.get_rect()
			intro_rect.top = self.text_coord
			intro_rect.x = config.WIDTH // 7 * 2 + 40
			self.game.screen.blit(self.images[i], (config.WIDTH // 7 * 2, self.text_coord))
			self.text_coord += intro_rect.height
			self.game.screen.blit(string_rendered, intro_rect)
		self.text_coord += 15
	for i in [
		'_' * 30,
		f'TOTAL:{" " * 5}{sum([round(k) for i, k in enumerate(self.vis_kills) if k > 0])}'
		f'{" " * 10}SCORE{" " * 5}{sum([round(k) * 100 * (i + 1) for i, k in enumerate(self.vis_kills) if k > 0])}'
	]:
		font = pg.font.Font(None, 30)
		string_rendered = font.render(i, 1, pg.Color('white'))
		intro_rect = string_rendered.get_rect()
		intro_rect.top = self.text_coord
		intro_rect.x = config.WIDTH // 7 * 2
		self.text_coord += intro_rect.height
		self.game.screen.blit(string_rendered, intro_rect)
		self.text_coord += 15
	return False