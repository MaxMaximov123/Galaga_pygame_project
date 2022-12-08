import pygame as pg
from Objects import config
from Objects.button import Button
from Objects.pause import Pause
from Objects.Tanks_objects.Fire import Fire
import random
from Objects.Tanks_objects.Tank import Tank
# from Main_window import MainWindow


class Tanks:
	def __init__(self, main_win=None):

		# Базовые параметры для всех игр
		pg.mixer.pre_init(44100, -16, 1, 512)
		self.main_win = main_win
		self.frame_counter = 1
		self.right_is_down = False
		self.left_is_down = False
		self.space_is_down = False
		self.up_is_down = False
		self.down_is_down = False
		self.running = True
		self.is_pause = False
		self.pause = None
		self.btn_home = None
		self.size = config.WIDTH, config.HEIGHT
		self.group = pg.sprite.Group()
		self.pause_group = pg.sprite.Group()
		self.screen = pg.display.set_mode(self.size)
		self.is_close_win = False
		self.pause_screen = self.screen
		self.step_move = 2

		self.step_shot = 2   # сколько раз в секунду можно создавать выстрел
		self.main_tank = Tank('sprites/Tanks/main_tank.png', (config.WIDTH // 2, config.HEIGHT // 15 * 13), self.screen)
		self.group.add(self.main_tank)
		self.button_menu = Button((30, 30), (30, 30), self.screen, path='sprites/menu.png')
		self.enemies = []
		self.fires = []
		# self.sound_boom.set_volume(0.1)
		self.enemies_place_left = self.size[0] // 12
		self.enemies_place_up = self.size[1] // 10
		self.enemies_matrix = [[0 for j in range(
			self.enemies_place_left * 4, self.enemies_place_left * 8, 60)] for _ in range(
			self.enemies_place_up, self.enemies_place_up * 5, 30)]


	def run(self):
		pg.init()
		pg.display.set_caption('Galaga')
		clock = pg.time.Clock()
		self.group.add(self.button_menu)
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
						self.left_is_down = True
						self.right_is_down = False
						self.up_is_down = False
						self.down_is_down = False

					if event.key in [pg.K_RIGHT, pg.K_d] and not self.is_pause:
						self.right_is_down = True
						self.left_is_down = False
						self.up_is_down = False
						self.down_is_down = False

					if event.key == pg.K_ESCAPE and not self.is_pause:
						self.start_pause()

					if event.key in [pg.K_DOWN, pg.K_s] and not self.is_pause:
						self.down_is_down = True
						self.left_is_down = False
						self.right_is_down = False
						self.up_is_down = False

					if event.key in [pg.K_UP, pg.K_w] and not self.is_pause:
						self.up_is_down = True
						self.left_is_down = False
						self.right_is_down = False
						self.down_is_down = False

					if event.key == pg.K_SPACE and not self.is_pause:
						self.space_is_down = True
						# self.frame_counter = config.FPS // self.step_shot

				if event.type == pg.KEYUP:
					if event.key in [pg.K_LEFT, pg.K_a] and not self.is_pause:
						self.left_is_down = False

					if event.key in [pg.K_RIGHT, pg.K_d] and not self.is_pause:
						self.right_is_down = False

					if event.key == pg.K_ESCAPE and not self.is_pause:
						self.start_pause()

					if event.key in [pg.K_DOWN, pg.K_s] and not self.is_pause:
						self.down_is_down = False

					if event.key in [pg.K_UP, pg.K_w] and not self.is_pause:
						self.up_is_down = False

					if event.key == pg.K_SPACE and not self.is_pause:
						self.space_is_down = False


			if config.FPS // self.frame_counter == self.step_shot:
				if self.space_is_down:
					self.fires.append(Fire('sprites/Tanks/fire1.png', (
						self.main_tank.rect.x + self.main_tank.size // 2,
						self.main_tank.rect.y + self.main_tank.size // 2), self.main_tank.vector_x, self.main_tank.vector_y))
					self.group.add(self.fires[-1])
					# self.sound_shot.play()

			if config.FPS // self.frame_counter == self.step_move:
				if self.left_is_down:
					self.main_tank.left_move()
					self.right_is_down = False
					self.up_is_down = False
					self.down_is_down = False
				if self.right_is_down:
					self.main_tank.right_move()
					self.left_is_down = False
					self.up_is_down = False
					self.down_is_down = False
				if self.up_is_down:
					self.main_tank.up_move()
					self.left_is_down = False
					self.right_is_down = False
					self.down_is_down = False
				if self.down_is_down:
					self.main_tank.down_move()
					self.left_is_down = False
					self.right_is_down = False
					self.up_is_down = False

			self.frame_counter += 1
			if self.frame_counter == config.FPS:
				self.frame_counter = 1
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


if __name__ == '__main__':
	Tanks()