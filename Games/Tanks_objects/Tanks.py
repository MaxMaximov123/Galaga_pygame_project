import random
import sys
from os import listdir
from os.path import isfile, join

from PIL import Image
from Games.Tanks_objects import Levels
from Games.Tanks_objects.Boosters import *
from Games.Tanks_objects.Create_new_level import Creater
from Games.Tanks_objects.Fire import Fire
from Games.Tanks_objects.Game_over import GameOver
from Games.Tanks_objects.Tank import MainTank, EnemyTank
from Games.Tanks_objects.Win_screen import WinScreen
from Games.button import Button
from Games.pause import Pause


def split_animated_gif(gif_file_path):
	ret = []
	gif = Image.open(gif_file_path)
	for frame_index in range(gif.n_frames):
		gif.seek(frame_index)
		frame_rgba = gif.convert("RGBA")
		pygame_image = pg.image.fromstring(
			frame_rgba.tobytes(), frame_rgba.size, frame_rgba.mode
		)
		ret.append(pygame_image)
	return ret


class Snow(pg.sprite.Sprite):
	def __init__(self, game, f=True):
		super().__init__(game.snow_groups)
		color = pg.Color(255, 255, 255, random.randint(100, 200))
		self.game = game
		self.radius = random.randint(1, 6)
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
		self.speed = random.randint(10, 20)
		self.x, self.y = self.rect.x, self.rect.y

	def update(self):
		self.x += self.vector_x * self.speed / config.FPS
		self.y += self.vector_y * self.speed / config.FPS
		self.rect.x, self.rect.y = self.x, self.y
		if self.x > config.WIDTH or self.y > config.HEIGHT:
			self.kill()
			Snow(self.game, False)

	def set_can_move(self, f):
		pass


# КЛАСС ИГРЫ
class Tanks:
	level_num = 0  # НОМЕР УРОВНЯ
	max_count_enemies = 5  # количество врагов на экране в любой момент времен
	max_count_enemies_in_game = random.randint(15, 40)  # количество врагов за всю игру

	def __init__(self, main_win=None):
		# Базовые параметры для всех игр
		self.coords_in_board1 = []
		pg.mixer.pre_init(44100, -16, 1, 512)
		pg.init()
		pg.display.set_caption('Tanks')
		self.level_num = Tanks.level_num  # НОМЕР УРОВНЯ
		self.levels = [
			f for f in listdir('Games/Tanks_objects/data/levels') if
			isfile(join('Games/Tanks_objects/data/levels', f))]  # ОБЪЕКТЫ УРОВНИ
		self.main_win = main_win  # СТАРТОВОЕ ОКНО
		self.button_down = ''  # КАКАЯ КНОПКА НАЖАТА
		self.last_button_down = ''
		self.space_is_down = False  # НАЖАТ ЛИ ПРОБЕЛ
		self.running = True  # ЗАПУСК ИГРЫ
		self.is_pause = False  # ЗАПУЩЕНА ЛИ ПАУЗА
		self.pause = None  # ОБЪЕКТ ПАУЗА
		self.btn_home = None  # КНОПКА МЕНЮ
		self.size = config.WIDTH, config.HEIGHT  # РАЗМЕР ОКНА
		self.clock = pg.time.Clock()  # СОЗДАЕМ ОБЪЕКТ ЧАСЫ

		# ЗВУКИ
		self.sound_shot = pg.mixer.Sound("Games/Tanks_objects/data/sounds/shot.mp3")
		self.sound_shot.set_volume(0.2)
		self.sound_sart = pg.mixer.Sound("Games/Tanks_objects/data/sounds/start.mp3")
		self.sound_sart.set_volume(0.2)
		self.sound_kill = pg.mixer.Sound("Games/Tanks_objects/data/sounds/kill.mp3")
		self.sound_kill.set_volume(0.2)

		# НЕОБХОДИМЫЕ ГРУППЫ СПРАЙТОВ
		self.fires_group = pg.sprite.Group()  # ГРУППА ПУЛЬ
		self.boosters_group = pg.sprite.Group()  # ГРУППА БОНУСОВ
		self.tanks_group = pg.sprite.Group()  # ГРУППА ВСЕХ ТАНКОВ
		self.pause_group = pg.sprite.Group()  # ГРУППА СПРАЙТОВ ДЛЯ ПАУЗЫ
		self.buttons_group = pg.sprite.Group()  # ГРУППА КНОПОК
		self.walls_group = pg.sprite.Group()  # ГРУППА СТЕН
		self.bush_group = pg.sprite.Group()  # ГРУППА С КУСТАМИ
		self.ice_group = pg.sprite.Group()  # ГРУППА С КУСТАМИ
		self.snow_groups = pg.sprite.Group()
		self.all_groups = pg.sprite.Group()  # ВСЕ СПРАЙТЫ

		self.screen = pg.display.set_mode(self.size)  # ИНИЦИАЛИЗАЦИЯ ЭКРАНА
		self.is_close_win = False  # ФЛАГ ЗАКРЫТОГО ОКНА
		self.pause_screen = self.screen  # ЭКРАН ПАУЗЫ
		self.step_move = 2  # ШАГ ДВИЖЕНИЯ

		self.step_shot = config.FPS // 4  # сколько раз в секунду можно создавать выстрел
		self.frame_counter_shot = self.step_shot  # СЧЕТЧИК КАДРОВ
		self.main_tank = MainTank((
			config.SIZE_BOARD_FOR_TANKS[0] // 2 * config.TILE_SIZE,
			config.HEIGHT - config.TILE_SIZE), self, power=0)  # СОЗДАНИЕ ПОЛЬЗОВАТЕЛЬСКОГО ТАНКА
		self.main_tank_moves = {
			'left': self.main_tank.left_move,
			'right': self.main_tank.right_move,
			'up': self.main_tank.up_move,
			'down': self.main_tank.down_move}  # ФУНКЦИИ ДВИЖЕНИЙ ВПЕРЕД
		self.reverse_main_tank_moves = {
			'right': self.main_tank.left_move,
			'left': self.main_tank.right_move,
			'down': self.main_tank.up_move,
			'up': self.main_tank.down_move}  # ЫУНКЦИИ ДВИЖЕНИЙ НАЗАД
		self.names_buttons = {
			'left': [pg.K_LEFT, pg.K_a],
			'right': [pg.K_RIGHT, pg.K_d],
			'up': [pg.K_UP, pg.K_w],
			'down': [pg.K_DOWN, pg.K_s]}  # КНОПКИ ДЛЯ ДВИЖЕНИЯ
		self.kill_counts = [0, 0, 0, 0]  # КОЛ-ВО УБИТЫХ ТАНКОВ ПО КАТЕГОРИЯМ
		self.all_tanks_count = 0  # КОЛ-ВО УБИТЫХ ТАНКОВ
		self.button_menu = Button(
			(30, 30), (30, 30), self.screen,
			path='Games/Tanks_objects/data/images/menu.png')  # КНОПКА ПАУЗЫ
		self.enemies = []  # ВРАЖЕСКИЕ ТАНКИ
		self.fires = []  # СНАРДЫ ВЫСТРЕЛОВ
		self.MYEVENTTYPE = pg.USEREVENT + 1  # СОБЫТИЕ ДЛЯ СОЗДАНИЯ ВРАЖЕСКОГО ТАНКА
		pg.time.set_timer(self.MYEVENTTYPE, 2000)
		self.TIMEFORBOOSTERS = pg.USEREVENT + 2  # СОБЫТИЕ ДЛЯ ПОЯВЛЕНИЯ БОНУСА
		pg.time.set_timer(self.TIMEFORBOOSTERS, 5000)
		self.boosters = [KillTanksBooster, StopTimeBooster, UpPowerBooster, ShieldBooster]

		# Инициализация уровня
		self.walls = []
		self.fields_to_generate = []  # СПИСОК ПОЛЕЙ ДЛЯ ГЕНЕРАЦИИ ТАНКОВ
		self.coords_in_board = []
		self.level = None

		self.groups = [
			self.tanks_group, self.walls_group,
			self.tanks_group, self.buttons_group,
			self.fires_group, self.boosters_group, self.bush_group, self.snow_groups]  # ВСЕ ГРУППЫ В ПОРЯДКЕ ИХ ОТРИСОВКИ

	# ЗАПУСК ИГРЫИ ИГРОВОЙ ЦИКЛ
	def run(self):
		flag_ice = False
		for i in range(random.randint(500, 1000)):
			Snow(self)
		self.buttons_group.add(self.button_menu)
		self.start_screen()  # ЗАПУСК СТАРТОВОГО ОКНА
		self.level = Levels.Level(
			self,
			f'Games/Tanks_objects/data/levels/level{self.level_num % len(self.levels)}.csv')  # ПУТЬ К ФАЙЛУ УРОВНЯ
		self.sound_sart.play()
		while self.running:
			self.screen.fill((0, 0, 0))
			self.main_tank.set_can_move(True)
			# ОБРАБОТКА СОБЫТИЙ
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

					if event.key == pg.K_ESCAPE:
						if not self.is_pause:
							self.start_pause()
						else:
							self.running = False
							self.is_close_win = True

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
					if not self.is_pause:
						for tank in self.tanks_group:
							if tank != self.main_tank:
								tank.is_pause = False
						if self.all_tanks_count < self.max_count_enemies_in_game:
							if len(self.tanks_group) <= Tanks.max_count_enemies:
								if self.generate_new_enemy(random.randint(0, 3)):
									self.all_tanks_count += 1

				if event.type == self.TIMEFORBOOSTERS and not self.is_pause:
					if random.choice(range(3)) == 0:
						self.generate_new_booster()

			if self.button_down:
				self.last_button_down = self.button_down

			if self.space_is_down and self.frame_counter_shot == self.step_shot and self.main_tank.hp:  # СОЗДАНИЕ ПУЛИ ПРИ НАЖАТИИ ПРОБЕЛА
				self.frame_counter_shot = 0
				Fire(self, (
					self.main_tank.rect.x + self.main_tank.size // 2,
					self.main_tank.rect.y + self.main_tank.size // 2),
					 True,
					 self.main_tank.vector_x, self.main_tank.vector_y)
				self.sound_shot.play()

			# ПРОВЕРКА НА ПОБЕДУ
			if sum(self.kill_counts) >= self.max_count_enemies_in_game and not self.is_pause:
				self.win()
			if self.button_down:  # НАЖАТИЕ ОДНОЙ ИЗ КНОПОК ДВИЖЕНИЯ
				if self.main_tank.can_move:
					self.main_tank_moves[self.button_down]()

			if not self.is_pause:  # УСЛОВИЕ НА ЗАПУЩЕННУЮ ИГРУ
				# ОБНОВЛЯЕМ ВСЕ ГРУППЫ
				for group in self.groups:
					group.draw(self.screen)
					group.update()
				if pg.sprite.spritecollideany(self.main_tank, self.ice_group):
					self.button_down = self.last_button_down
					flag_ice = True
				elif flag_ice:
					self.last_button_down = self.button_down = ''
					flag_ice = False
			else:
				self.pause_group.draw(self.screen)
				self.pause_group.update()
			self.print_tank_counts()

			self.frame_counter_shot += 1  # СЧЕТЧИК КАДРОВ
			if self.frame_counter_shot == config.FPS:
				self.frame_counter_shot = 0
			self.clock.tick(config.FPS)
			pg.display.update()

	# ЗАКРЫТА ЛИ ИГРА
	def is_close(self):
		return self.is_close_win

	# ЗАПУСК ПАУЗЫ
	def start_pause(self):
		self.is_pause = True
		self.pause = Pause((config.WIDTH // 2, config.HEIGHT // 5), self.screen)
		self.pause_group.add(*self.groups)
		for f in self.pause_group:
			f.set_can_move(False)
		self.pause_group.add(self.pause.buttons)

	# ПРОДОЛЖЕНИЕ ИГРЫ
	def start(self):
		self.is_pause = False
		self.pause_group.remove(*self.pause.buttons)
		for f in self.fires_group:
			f.set_can_move(True)

	# ЗАКРЫТИЕ ОКНА
	def close(self):
		pg.quit()

	# ЗАПСК ОКНА ПРИГРЫША
	def game_over(self):
		self.is_pause = True
		self.pause_group.add(*self.groups)
		for f in self.pause_group:
			f.set_can_move(False)
		self.all_groups.add(GameOver(self))

	# ЗАПУСК ОКНА ВЫИГРЫША
	def win(self):
		self.is_pause = True
		self.pause_group.add(*self.groups)
		self.all_groups.add(WinScreen(self))

	# СОЗДАНИЕ НОВОГО ВРАЖЕСКОГО ТАНКА
	def generate_new_enemy(self, power):
		self.coords_in_board = []
		for row in range(len(self.level.vis_board)):
			for col in range(len(self.level.vis_board[0])):
				if self.level.vis_board[row][col] == '0':
					self.coords_in_board.append([col, row])

		if len(self.tanks_group) <= Tanks.max_count_enemies and self.coords_in_board:
			enemy_tank = EnemyTank(random.choice(self.coords_in_board), self, power)
			while not enemy_tank.tank_can_move() and self.coords_in_board:
				enemy_tank.kill()
				enemy_tank = EnemyTank(random.choice(self.coords_in_board), self, power)
			return True
		else:
			return False

	# СОЗДАНИЕ НОВОГО БОНУСА
	def generate_new_booster(self):
		self.coords_in_board1 = []
		for row in range(len(self.level.vis_board)):
			for col in range(len(self.level.vis_board[0])):
				if self.level.vis_board[row][col] == '0':
					self.coords_in_board1.append([col, row])

		if len(self.boosters_group) == 0 and self.coords_in_board1:
			random.choice(self.boosters)(self, random.choice(self.coords_in_board1))

	# ЗАВЕРШЕНИЕ ИГРЫ ПРИ ЗАКРЫТИИ ОКНА
	def terminate(self):
		pg.quit()
		sys.exit()

	# СТАРТОВОЕ ОКНО
	def start_screen(self):
		frames = []
		for frame in split_animated_gif("Games/Tanks_objects/data/images/fon.gif"):
			frames += [frame] * 10

		frame_index = 0
		fon = pg.transform.scale(frames[frame_index % len(frames)],
								 (config.WIDTH, config.HEIGHT))
		self.screen.blit(fon, (0, 0))
		self.print_level(self.levels[self.level_num % len(self.levels)])

		while True:
			frame_index += 1
			fon = pg.transform.scale(frames[frame_index % len(frames)],
									 (config.WIDTH, config.HEIGHT))
			self.screen.blit(fon, (0, 0))
			self.print_level(self.levels[self.level_num % len(self.levels)])
			for event in pg.event.get():
				if event.type == pg.QUIT:
					self.terminate()
				if event.type == pg.KEYDOWN:
					if event.key in [pg.K_a, pg.K_LEFT]:
						self.level_num -= 1
					elif event.key in [pg.K_d, pg.K_RIGHT]:
						self.level_num += 1
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

	def print_tank_counts(self):
		if not self.is_pause:
			font = pg.font.Font(None, 60)
			string_rendered = font.render(f'{sum(self.kill_counts)} / {self.max_count_enemies_in_game}', 1,
										  pg.Color('#ffcc00'))
			intro_rect = string_rendered.get_rect()
			intro_rect.top = config.TILE_SIZE // 4
			intro_rect.x = config.WIDTH - config.TILE_SIZE * 2
			self.screen.blit(string_rendered, intro_rect)


if __name__ == '__main__':
	Tanks()
