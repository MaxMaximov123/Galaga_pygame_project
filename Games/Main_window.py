import random

import pygame as pg

from Games import config
from Games.Galaga_objects.Cursor import Cursor
from Games.Galaga_objects.Galaga import Galaga
from Games.Tanks_objects.Tanks import Tanks


class Snow(pg.sprite.Sprite):
	def __init__(self, game, f=True):
		super().__init__(game.snow_groups)
		color = pg.Color(255, 255, 255, random.randint(100, 200))
		self.game = game
		self.radius = random.randint(1, 8)
		self.image = pg.Surface((2 * self.radius, 2 * self.radius),
								pg.SRCALPHA, 32)
		pg.draw.circle(
			self.image, color,
			(self.radius, self.radius), self.radius)
		if f:
			self.x, self.y = random.randint(-20, config.WIDTH), random.randint(-20, config.HEIGHT)
		else:
			if random.randint(0, 1):
				self.x, self.y = random.randint(-20, config.WIDTH), random.randint(-20, 20)
			else:
				self.x, self.y = random.randint(-20, 20), random.randint(-20, config.HEIGHT)
		self.rect = pg.Rect(self.x, self.y, 2 * self.radius, 2 * self.radius)
		self.vector_x = random.randint(1, 5)
		self.vector_y = random.randrange(1, 5)
		self.speed = random.randint(20, 30)
		self.x, self.y = self.rect.x, self.rect.y

	def update(self):
		self.x += self.vector_x * self.speed / config.FPS
		self.y += self.vector_y * self.speed / config.FPS
		self.rect.x, self.rect.y = self.x, self.y
		if self.x > config.WIDTH or self.y > config.HEIGHT:
			self.kill()
			Snow(self.game, False)


class MainWindow:
	def __init__(self):
		self.size = config.WIDTH, config.HEIGHT
		self.screen = pg.display.set_mode(self.size)

		self.active_game = None
		self.game = True
		self.game_text_size = 30
		self.head_text_size = 50
		self.games_names_pos = []
		self.games = [Galaga, Tanks]
		self.headers_games = []
		self.correct_game = None
		self.correct_position_ind = None
		self.snow_groups = pg.sprite.Group()
		self.snow_count = random.randint(500, 1000)

	def run(self):
		pg.init()
		pg.display.set_caption('Games')
		self.headers_games = []
		running = True
		clock = pg.time.Clock()
		cursor = Cursor(self.screen)
		self.draw(config.GAMES_NAMES)
		self.correct_position_ind = 0
		while len(self.snow_groups) < self.snow_count:
				Snow(self)
		while running:
			self.screen.fill('black')
			cursor.update_pos(self.games_names_pos[self.correct_position_ind % len(self.games_names_pos)])
			for event in pg.event.get():
				if event.type == pg.QUIT:
					running = False
				if event.type == pg.KEYDOWN:
					if event.key == pg.K_DOWN:
						self.correct_position_ind += 1
					if event.key == pg.K_UP:
						self.correct_position_ind -= 1
					if event.key == pg.K_RETURN:
						self.active_game = self.games[self.correct_position_ind % len(self.games)](self)
						self.active_game.run()
						self.correct_game = self.correct_position_ind
					# self.screen.fill('black')

				if event.type == pg.MOUSEBUTTONDOWN:
					if event.button == 1:
						for ind, pos in enumerate(self.headers_games):
							if pos[0] + pos[2].get_width() > event.pos[0] > pos[0] and pos[1] + pos[2].get_height() > \
									event.pos[1] > pos[1]:
								self.correct_position_ind = ind
								break
					if event.button == 4:
						self.correct_position_ind -= 1
					if event.button == 5:
						self.correct_position_ind += 1
			self.snow_groups.update()
			self.snow_groups.draw(self.screen)
			self.draw(config.GAMES_NAMES)
			clock.tick(config.FPS)
			pg.display.flip()
		pg.quit()

	def draw(self, games_names):
		# self.screen.fill((0, 0, 0))
		font = pg.font.SysFont('monospace', self.head_text_size)
		font.bold = True
		text = font.render("Выберите игру", True, ('#ffcc00'))
		text_x = config.WIDTH // 2 - text.get_width() // 2
		text_y = config.HEIGHT // 5 - text.get_height() // 2
		self.screen.blit(text, (text_x, text_y))
		self.headers_games = []
		for h, name in enumerate(games_names):
			font = pg.font.SysFont("monospace", self.game_text_size)
			font.bold = True
			text = font.render(name, True, ('#ffcc00'))
			text_x = config.WIDTH // 2 - text.get_width() // 2
			text_y = config.HEIGHT // 15 * (h + 5) - text.get_height() // 2
			self.screen.blit(text, (text_x, text_y))
			self.games_names_pos.append([text_x - 10, text_y + text.get_height() // 2])
			self.headers_games.append([text_x, text_y, text])


if __name__ == '__main__':
	win = MainWindow().run
