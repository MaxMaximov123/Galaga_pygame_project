import pygame as pg
import config
from SpaceShip import SpaceShip
from Fire import Fire
from button import Button
from pause import Pause
# from Main_window import MainWindow


class Galaga:
	def __init__(self, main_win):
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
		self.space_ship = SpaceShip('sprites/spaceship4.png', (config.WIDTH // 2, config.HEIGHT // 15 * 13))
		self.size = config.WIDTH, config.HEIGHT
		self.group = pg.sprite.Group(self.space_ship)
		self.pause_group = pg.sprite.Group()
		self.screen = pg.display.set_mode(self.size)
		self.is_close_win = False
		self.pause_screen = self.screen
		self.button_menu = Button((30, 30), (30, 30), self.screen, path='sprites/menu.png')
		self.image_backround = pg.image.load("sprites/Galaga_background.png").convert_alpha()  # картинка спрайта
		self.image_backround = pg.transform.scale(self.image_backround, self.size)


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
							self.is_pause = True
							self.pause = Pause((config.WIDTH // 2, config.HEIGHT // 5), self.screen)
							self.pause_group = self.group
							for i in self.pause.buttons:
								self.pause_group.add(i)

						if self.pause and self.pause.buttons[0].is_click(event.pos):
							self.running = False
							self.is_close_win = True

						if self.pause and self.pause.buttons[1].is_click(event.pos):
							self.pause_group.remove(*self.pause.buttons)
							self.is_pause = False

				if event.type == pg.KEYDOWN:
					if event.key == pg.K_LEFT:
						self.left_is_down = True
						self.frame_counter = config.FPS // self.step_shot

					if event.key == pg.K_ESCAPE and not self.is_pause:
						self.is_pause = True
						self.pause = Pause((config.WIDTH // 2, config.HEIGHT // 5), self.screen)
						self.pause_group = self.group
						for i in self.pause.buttons:
							self.pause_group.add(i)

					if event.key == pg.K_RIGHT and not self.is_pause:
						self.right_is_down = True
						self.frame_counter = config.FPS // self.step_shot

					if event.key == pg.K_SPACE and not self.is_pause:
						self.space_is_down = True
						self.frame_counter = config.FPS // self.step_shot

				if event.type == pg.KEYUP:
					if event.key == pg.K_SPACE and not self.is_pause:
						self.space_is_down = False

					if event.key == pg.K_LEFT and not self.is_pause:
						self.left_is_down = False

					if event.key == pg.K_RIGHT and not self.is_pause:
						self.right_is_down = False
			if self.frame_counter == config.FPS // self.step_shot:
				self.frame_counter = 0
				if self.space_is_down:
					self.group.add(Fire('sprites/fire1.png', (self.space_ship.rect.x + self.space_ship.size // 2, self.space_ship.rect.y)))

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


			clock.tick(config.FPS)
			pg.display.update()
		# pg.quit()


	def is_close(self):
		return self.is_close_win


	def close(self):
		pg.quit()