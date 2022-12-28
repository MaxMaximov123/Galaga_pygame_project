import pygame as pg
from Games import config
from Games.Galaga_objects.SpaceShip import SpaceShip
from Games.Galaga_objects.Fire import Fire
from Games.button import Button
from Games.pause import Pause
from Games.Galaga_objects.Enemy import Enemy1
import random
# from Main_window import MainWindow


class Galaga:
	def __init__(self, main_win):
		pg.mixer.pre_init(44100, -16, 1, 512)
		self.main_win = main_win
		self.frame_counter = 0
		self.right_is_down = False
		self.left_is_down = False
		self.space_is_down = False
		self.running = True
		self.step_move = 10

		self.is_pause = False
		self.pause = None
		self.btn_home = None

		self.step_shot = 6  # сколько раз в секунду можно создавать выстрел
		self.space_ship = SpaceShip('Games/Galaga_objects/data/images/spaceship2.png', (config.WIDTH // 2, config.HEIGHT // 15 * 13))
		self.size = config.WIDTH, config.HEIGHT
		self.group = pg.sprite.Group(self.space_ship)
		self.pause_group = pg.sprite.Group()
		self.screen = pg.display.set_mode(self.size)
		self.is_close_win = False
		self.pause_screen = self.screen
		self.button_menu = Button((30, 30), (30, 30), self.screen, path='Games/Galaga_objects/data/images/menu.png')
		self.image_backround = pg.image.load("Games/Galaga_objects/data/images/Galaga_background.png").convert_alpha()  # картинка спрайта
		self.image_backround = pg.transform.scale(self.image_backround, self.size)
		self.enemies = []
		self.fires = []
		self.sound_kill = pg.mixer.Sound("Games/Galaga_objects/data/sounds/kill.mp3")
		self.sound_kill_enemy = pg.mixer.Sound("Games/Galaga_objects/data/sounds//kill_enemy.mp3")
		self.sound_shot = pg.mixer.Sound("Games/Galaga_objects/data/sounds/shot.mp3")
		# self.sound_boom.set_volume(0.1)
		self.enemies_place_left = self.size[0] // 12
		self.enemies_place_up = self.size[1] // 10
		self.enemies_matrix = [[0 for j in range(
			self.enemies_place_left * 4, self.enemies_place_left * 8, 60)] for _ in range(
			self.enemies_place_up, self.enemies_place_up * 5, 30)]

		positions = []
		for y in range(len(self.enemies_matrix)):
			for x in range(len(self.enemies_matrix[0])):
				positions += [[x, y]]
		for i in random.choices(positions, k=20):
			self.enemies.append(Enemy1('Games/Galaga_objects/data/images/enemy1.png', (
				self.enemies_place_left * i[0], self.enemies_place_up * i[1]), i))
			self.enemies_matrix[i[1]][i[0]] = 1
			self.group.add(self.enemies[-1])


	def run(self):
		pg.init()
		pg.display.set_caption('Galaga')
		clock = pg.time.Clock()
		self.group.add(self.button_menu)
		while self.running:
			self.screen.blit(self.image_backround, (0, 0))
			for event in pg.event.get():
				if event.type == pg.QUIT:
					self.running = False
					self.is_close_win = True
				if event.type == pg.MOUSEBUTTONDOWN:
					if event.button == 4 and not self.is_pause:
						self.space_ship.left_move()
					if event.button == 5 and not self.is_pause:
						self.space_ship.right_move()
					if event.button == 1:
						if self.button_menu.is_click(event.pos):
							self.start_pause()

						if self.pause and self.pause.buttons[0].is_click(event.pos):
							self.running = False
							self.is_close_win = True

						if self.pause and self.pause.buttons[1].is_click(event.pos):
							self.start()

				if event.type == pg.KEYDOWN:
					if event.key in [pg.K_LEFT, pg.K_a]:
						self.left_is_down = True
						self.frame_counter = config.FPS // self.step_shot

					if event.key == pg.K_ESCAPE and not self.is_pause:
						self.start_pause()

					if event.key in [pg.K_LEFT, pg.K_a] and not self.is_pause:
						self.right_is_down = True
						self.frame_counter = config.FPS // self.step_shot

					if event.key == pg.K_SPACE and not self.is_pause:
						self.space_is_down = True
						self.frame_counter = config.FPS // self.step_shot

				if event.type == pg.KEYUP:
					if event.key == pg.K_SPACE:
						self.space_is_down = False

					if event.key in [pg.K_LEFT, pg.K_a]:
						self.left_is_down = False

					if event.key in [pg.K_LEFT, pg.K_a]:
						self.right_is_down = False
			if self.frame_counter == config.FPS // self.step_shot:
				self.frame_counter = 0
				if self.space_is_down:
					self.fires.append(Fire('Games/Galaga_objects/data/images/fire1.png', (self.space_ship.rect.x + self.space_ship.size // 2, self.space_ship.rect.y)))
					self.group.add(self.fires[-1])
					self.sound_shot.play()

			if self.frame_counter == config.FPS // self.step_move:
				if self.left_is_down:
					self.space_ship.left_move()
				if self.right_is_down:
					self.space_ship.right_move()

			self.frame_counter += 1
			self.frame_counter = self.frame_counter % config.FPS
			if not self.is_pause:
				self.group.draw(self.screen)
				self.group.update()
			else:
				self.pause_group.draw(self.screen)
				self.pause_group.update()


			for enemy in self.enemies:
				for f in self.fires:
					if f.is_collided_with(enemy):
						self.sound_kill_enemy.play()
						self.enemies.remove(enemy)
						f.kill()
						self.fires.remove(f)
						enemy.kill()
				if enemy.is_collided_with(self.space_ship):
					self.sound_kill.play(maxtime=1)
					self.space_ship.kill()
					self.start_pause()


			clock.tick(config.FPS)
			pg.display.update()
		# pg.quit()


	def is_close(self):
		return self.is_close_win

	def start_pause(self):
		self.is_pause = True
		self.pause = Pause((config.WIDTH // 2, config.HEIGHT // 5), self.screen)
		self.pause_group = self.group
		for i in self.pause.buttons:
			self.pause_group.add(i)
		for enemy in self.enemies:
			enemy.can_move = False

		for f in self.fires:
			f.can_move = False

	def start(self):
		self.is_pause = False
		self.pause_group.remove(*self.pause.buttons)
		for enemy in self.enemies:
			enemy.can_move = True
			enemy.move = 0

		for f in self.fires:
			f.can_move = True


	def close(self):
		pg.quit()