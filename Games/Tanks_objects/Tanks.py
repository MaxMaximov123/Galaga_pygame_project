import random
import sys

import pygame as pg

from Games import config
from Games.Tanks_objects import Levels
from Games.Tanks_objects.Create_new_level import Creater
from Games.Tanks_objects.Fire import Fire
from Games.Tanks_objects.Game_over import GameOver
from Games.Tanks_objects.Tank import MainTank, EnemyTank
from Games.button import Button
from Games.pause import Pause
from os import listdir
from Games.Tanks_objects.Win_screen import WinScreen
from os.path import isfile, join


# from Main_window import MainWindow


class Tanks:
	level_num = 0  # НОМЕР УРОВНЯ
	max_count_enemies = 5  # количество врагов на экране в любой момент времен
	max_count_enemies_in_game = random.randint(10, 15)  # количество врагов за всю игру

	def __init__(self, main_win=None):
		# Базовые параметры для всех игр
		pg.mixer.pre_init(44100, -16, 1, 512)
		pg.init()
		pg.display.set_caption('Tanks')
		self.level_num = Tanks.level_num  # НОМЕР УРОВНЯ
		self.levels = [
			f for f in listdir('Games/Tanks_objects/data/levels') if
			isfile(join('Games/Tanks_objects/data/levels', f))]  # ОБЪЕКТЫ УРОВНИ
		self.main_win = main_win  # СТАРТОВОЕ ОКНО
		self.button_down = ''  # КАКАЯ КНОПКА НАЖАТА
		self.space_is_down = False  # НАЖАТ ЛИ ПРОБЕЛ
		self.running = True  # ЗАПУСК ИГРЫ
		self.is_pause = False  # ЗАПУЩЕНА ЛИ ПАУЗА
		self.pause = None  # ОБЪЕКТ ПАУЗА
		self.btn_home = None  # КНОПКА МЕНЮ
		self.size = config.WIDTH, config.HEIGHT  # РАЗМЕР ОКНА
		self.clock = pg.time.Clock()

		# НЕОБХОДИМЫЕ ГРУППЫ СПРАЙТОВ
		self.fires_group = pg.sprite.Group()
		self.tanks_group = pg.sprite.Group()
		self.pause_group = pg.sprite.Group()
		self.buttons_group = pg.sprite.Group()
		self.walls_group = pg.sprite.Group()
		self.bush_group = pg.sprite.Group()
		self.all_groups = pg.sprite.Group()
		self.all_groups.add()

		self.screen = pg.display.set_mode(self.size)
		self.is_close_win = False
		self.pause_screen = self.screen
		self.step_move = 2

		self.step_shot = config.FPS // 4  # сколько раз в секунду можно создавать выстрел
		self.frame_counter_shot = self.step_shot
		self.main_tank = MainTank((config.WIDTH // 2, config.HEIGHT // 15 * 13), self, power=3)
		self.main_tank_moves = {
			'left': self.main_tank.left_move,
			'right': self.main_tank.right_move,
			'up': self.main_tank.up_move,
			'down': self.main_tank.down_move}
		self.reverse_main_tank_moves = {
			'right': self.main_tank.left_move,
			'left': self.main_tank.right_move,
			'down': self.main_tank.up_move,
			'up': self.main_tank.down_move}
		self.names_buttons = {
			'left': [pg.K_LEFT, pg.K_a],
			'right': [pg.K_RIGHT, pg.K_d],
			'up': [pg.K_UP, pg.K_w],
			'down': [pg.K_DOWN, pg.K_s]}
		self.kill_counts = [0, 0, 0, 0]
		self.all_tanks_count = 0
		self.button_menu = Button((30, 30), (30, 30), self.screen, path='Games/Tanks_objects/data/images/menu.png')
		self.enemies = []
		self.fires = []
		self.MYEVENTTYPE = pg.USEREVENT + 1
		pg.time.set_timer(self.MYEVENTTYPE, 2000)
		self.enemies_place_left = self.size[0] // 12
		self.enemies_place_up = self.size[1] // 10
		self.enemies_matrix = [[0 for j in range(
			self.enemies_place_left * 4, self.enemies_place_left * 8, 60)] for _ in range(
			self.enemies_place_up, self.enemies_place_up * 5, 30)]

		# Инициализация уровня
		self.walls = []
		self.fields_to_generate = []  # СПИСОК ПОЛЕЙ ДЛЯ ГЕНЕРАЦИИ ТАНКОВ
		self.coords_in_board = []
		self.level = None

		self.groups = [self.tanks_group, self.walls_group, self.tanks_group, self.buttons_group, self.fires_group, self.bush_group]

	def run(self):
		self.buttons_group.add(self.button_menu)
		self.start_screen()
		self.level = Levels.Level(
			self, f'Games/Tanks_objects/data/levels/level{self.level_num % len(self.levels)}.csv')  # ПУТЬ К ФАЙЛУ УРОВНЯ
		while self.running:
			self.screen.fill((0, 0, 0))
			self.main_tank.set_can_move(True)
			for event in pg.event.get():
				if event.type == pg.QUIT:
					self.running = False
					self.terminate()
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

					if event.key == pg.K_n:
						mods = pg.key.get_mods()
						if mods & pg.KMOD_CTRL:
							create = Creater(self)

				if event.type == self.MYEVENTTYPE:
					if self.all_tanks_count < self.max_count_enemies_in_game:
						if len(self.tanks_group) <= Tanks.max_count_enemies:
							self.generate_new_enemy(random.randint(0, 3))
							self.all_tanks_count += 1

			if self.space_is_down and self.frame_counter_shot == self.step_shot:  # СОЗДАНИЕ ПУЛИ ПРИ НАЖАТИИ ПРОБЕЛА
				self.frame_counter_shot = 0
				Fire(self, (
					self.main_tank.rect.x + self.main_tank.size // 2,
					self.main_tank.rect.y + self.main_tank.size // 2),
					True,
					self.main_tank.vector_x, self.main_tank.vector_y)

			if not self.is_pause:  # УСЛОВИЕ НА ЗАПУЩЕННУЮ ИГРУ
				# ОБНОВЛЯЕМ ВСЕ ГРУППЫ
				for group in self.groups:
					group.draw(self.screen)
					group.update()
			else:
				self.pause_group.draw(self.screen)
				self.pause_group.update()

			if sum(self.kill_counts) >= self.max_count_enemies_in_game and not self.is_pause:
				self.win()
			if self.button_down:  # НАЖАТИЕ ОДНОЙ ИЗ КНОПОК ДВИЖЕНИЯ
				if self.main_tank.can_move:
					self.main_tank_moves[self.button_down]()

			self.frame_counter_shot += 1  # СЧЕТЧИК КАДРОВ
			if self.frame_counter_shot == config.FPS:
				self.frame_counter_shot = 0
			self.clock.tick(config.FPS)
			pg.display.update()

	def is_close(self):
		return self.is_close_win

	def start_pause(self):
		self.is_pause = True
		self.pause = Pause((config.WIDTH // 2, config.HEIGHT // 5), self.screen)
		self.pause_group.add(*self.groups)
		for f in self.pause_group:
			f.set_can_move(False)
		self.pause_group.add(self.pause.buttons)

	def start(self):
		self.is_pause = False
		self.pause_group.remove(*self.pause.buttons)
		for f in self.fires_group:
			f.set_can_move(True)

	def close(self):
		pg.quit()

	def game_over(self):
		self.is_pause = True
		self.pause_group.add(*self.groups)
		for f in self.pause_group:
			f.set_can_move(False)
		self.all_groups.add(GameOver(self))

	def win(self):
		self.is_pause = True
		self.pause_group.add(*self.groups)
		self.all_groups.add(WinScreen(self))

	def generate_new_enemy(self, power):
		self.coords_in_board = []
		for row in range(len(self.level.vis_board)):
			for col in range(len(self.level.vis_board[0])):
				if self.level.vis_board[row][col] == '0':
					self.coords_in_board.append([col, row])

		if len(self.tanks_group) <= Tanks.max_count_enemies:
			enemy_tank = EnemyTank(random.choice(self.coords_in_board), self, power)
			while not enemy_tank.tank_can_move() and self.coords_in_board:
				enemy_tank.kill()
				enemy_tank = EnemyTank(random.choice(self.coords_in_board), self, power)

	def terminate(self):
		pg.quit()
		sys.exit()


	def start_screen(self):
		intro_text = ["ТАНКИ 1.0", "",
					  "Правила игры:",
					  "Используйте клавиши стрелок или WASD",
					  "для движения и пробел для стрельбы"]

		fon = pg.transform.scale(pg.image.load('Games/Tanks_objects/data/images/fon.gif'), (config.WIDTH, config.HEIGHT))
		self.screen.blit(fon, (0, 0))
		self.print_level(self.levels[self.level_num % len(self.levels)])

		while True:
			for event in pg.event.get():
				if event.type == pg.QUIT:
					self.terminate()
				if event.type == pg.KEYDOWN:
					if event.key in [pg.K_a, pg.K_LEFT]:
						self.level_num -= 1
						self.screen.blit(fon, (0, 0))
						self.print_level(self.levels[self.level_num % len(self.levels)])
					elif event.key in [pg.K_d, pg.K_RIGHT]:
						self.level_num += 1
						self.screen.blit(fon, (0, 0))
						self.print_level(self.levels[self.level_num % len(self.levels)])
					else:
						return

				if event.type == pg.MOUSEBUTTONDOWN:
					return  # начинаем игру
			pg.display.flip()
			self.clock.tick(config.FPS)

	def print_level(self, level):
		intro_text = ["ТАНКИ 1.0", "",
					  "Правила игры:",
					  "Используйте клавиши стрелок или WASD",
					  "для движения и пробел для стрельбы"]
		font = pg.font.Font(None, 30)
		text_coord = 50
		for line in intro_text:
			string_rendered = font.render(line, 1, pg.Color('white'))
			intro_rect = string_rendered.get_rect()
			text_coord += 10
			intro_rect.top = text_coord
			intro_rect.x = 10
			text_coord += intro_rect.height
			self.screen.blit(string_rendered, intro_rect)
		string_rendered = font.render('Уровень: ' + level[:-4], 1, pg.Color('white'))
		intro_rect = string_rendered.get_rect()
		text_coord += 10
		intro_rect.top = text_coord
		intro_rect.x = 10
		text_coord += intro_rect.height
		self.screen.blit(string_rendered, intro_rect)


if __name__ == '__main__':
	Tanks()
