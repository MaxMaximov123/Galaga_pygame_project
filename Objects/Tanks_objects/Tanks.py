import pygame as pg
from Objects import config
from Objects.button import Button
from Objects.pause import Pause
from Objects.Tanks_objects.Fire import Fire
import random
from Objects.Tanks_objects import Levels
from Objects.Tanks_objects.Tank import Tank
# from Main_window import MainWindow


class Tanks:
	def __init__(self, main_win=None):

		# Базовые параметры для всех игр
		pg.mixer.pre_init(44100, -16, 1, 512)
		pg.init()
		pg.display.set_caption('Tanks')
		self.main_win = main_win
		self.button_down = ''
		self.space_is_down = False
		self.running = True
		self.is_pause = False
		self.pause = None
		self.btn_home = None
		self.size = config.WIDTH, config.HEIGHT
		self.fires_group = pg.sprite.Group()
		self.tanks_group = pg.sprite.Group()
		self.pause_group = pg.sprite.Group()
		self.buttons_group = pg.sprite.Group()
		self.walls_group = pg.sprite.Group()
		self.screen = pg.display.set_mode(self.size)
		self.is_close_win = False
		self.pause_screen = self.screen
		self.step_move = 2

		self.step_shot = config.FPS // 3   # сколько раз в секунду можно создавать выстрел
		self.frame_counter_shot = self.step_shot
		self.main_tank = Tank('data/Tanks/main_tank.png', (config.WIDTH // 2, config.HEIGHT // 15 * 13), self.screen)
		self.main_tank_moves = {
			'left': self.main_tank.left_move,
			'right': self.main_tank.right_move,
			'up': self.main_tank.up_move,
			'down': self.main_tank.down_move}
		self.names_buttons = {
			'left': [pg.K_LEFT, pg.K_a],
			'right': [pg.K_RIGHT, pg.K_d],
			'up': [pg.K_UP, pg.K_w],
			'down': [pg.K_DOWN, pg.K_s]}
		self.tanks_group.add(self.main_tank)
		self.button_menu = Button((30, 30), (30, 30), self.screen, path='data/menu.png')
		self.enemies = []
		self.fires = []
		# self.sound_boom.set_volume(0.1)
		self.enemies_place_left = self.size[0] // 12
		self.enemies_place_up = self.size[1] // 10
		self.enemies_matrix = [[0 for j in range(
			self.enemies_place_left * 4, self.enemies_place_left * 8, 60)] for _ in range(
			self.enemies_place_up, self.enemies_place_up * 5, 30)]


		# Инициализация уровня

		self.level = Levels.Level1(self.screen)
		for y in range(len(self.level.board)):
			for x in range(len(self.level.board[0])):
				if self.level.board[y][x] != '0':
					self.walls_group.add(self.level.board[y][x])

		self.groups = [self.fires_group, self.tanks_group, self.walls_group, self.buttons_group]




	def run(self):
		clock = pg.time.Clock()
		self.buttons_group.add(self.button_menu)
		while self.running:
			# self.screen.blit(self.image_backround, (0, 0))
			self.screen.fill((0, 0, 0))
			for event in pg.event.get():
				if event.type == pg.QUIT:
					self.running = False
					self.is_close_win = True
				if event.type == pg.MOUSEBUTTONDOWN:
					if event.button == 1:
						if self.button_menu.is_click(event.pos):
							self.start_pause()

						if self.pause and self.pause.buttons[0].is_click(event.pos):
							self.running = False
							self.is_close_win = True

						if self.pause and self.pause.buttons[1].is_click(event.pos):
							self.start()

				if event.type == pg.KEYDOWN:
					if event.key in [pg.K_LEFT, pg.K_a] and not self.is_pause:
						self.button_down = 'left'

					if event.key in [pg.K_RIGHT, pg.K_d] and not self.is_pause:
						self.button_down = 'right'

					if event.key == pg.K_ESCAPE and not self.is_pause:
						self.start_pause()

					if event.key in [pg.K_DOWN, pg.K_s] and not self.is_pause:
						self.button_down = 'down'

					if event.key in [pg.K_UP, pg.K_w] and not self.is_pause:
						self.button_down = 'up'

					if event.key == pg.K_SPACE and not self.is_pause:
						self.space_is_down = True
						self.frame_counter_shot = self.step_shot

				if event.type == pg.KEYUP:
					if event.key == pg.K_ESCAPE and not self.is_pause:
						self.start_pause()

					if event.key == pg.K_SPACE and not self.is_pause:
						self.space_is_down = False
					if self.button_down and event.key in self.names_buttons[self.button_down]:
						self.button_down = ''


			if self.space_is_down and self.frame_counter_shot == self.step_shot:
				self.frame_counter_shot = 0
				self.fires.append(Fire(self.screen, 'data/Tanks/fire1.png', (
					self.main_tank.rect.x + self.main_tank.size // 2,
					self.main_tank.rect.y + self.main_tank.size // 2), self.main_tank.vector_x, self.main_tank.vector_y))
				self.fires_group.add(self.fires[-1])
				# self.sound_shot.play()

			if self.button_down:
				self.main_tank_moves[self.button_down]()

			if not self.is_pause:
				for group in self.groups:
					group.draw(self.screen)
					group.update()

			else:
				self.pause_group.draw(self.screen)
				self.pause_group.update()

			self.frame_counter_shot += 1
			if self.frame_counter_shot == config.FPS:
				self.frame_counter_shot = 0
			clock.tick(config.FPS)
			pg.display.update()
		# pg.quit()


	def is_close(self):
		return self.is_close_win

	def start_pause(self):
		self.is_pause = True
		self.pause = Pause((config.WIDTH // 2, config.HEIGHT // 5), self.screen)
		self.pause_group = self.tanks_group
		self.pause_group.add(self.fires_group)
		for i in self.pause.buttons:
			self.pause_group.add(i)
		for enemy in self.enemies:
			enemy.can_move = False

		for f in self.fires:
			f.set_can_move(False)

	def start(self):
		self.is_pause = False
		self.pause_group.remove(*self.pause.buttons)
		for enemy in self.enemies:
			enemy.can_move = True
			enemy.move = 0

		for f in self.fires:
			f.set_can_move(True)


	def close(self):
		pg.quit()


if __name__ == '__main__':
	Tanks()