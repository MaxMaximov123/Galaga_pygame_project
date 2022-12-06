import pygame as pg
import config
from SpaceShip import SpaceShip
from Fire import Fire
from button import Button
# from Main_window import MainWindow


class Galaga:
	def __init__(self):
		self.frame_counter = 0
		self.right_is_down = False
		self.left_is_down = False
		self.space_is_down = False
		self.running = True
		self.step_move = 10
		self.step_shot = 5  # сколько раз в секунду можно создавать выстрел
		self.space_ship = SpaceShip('sprites/spaceship4.png', (config.WIDTH // 2, config.HEIGHT // 15 * 14))
		self.size = config.WIDTH, config.HEIGHT
		self.group = pg.sprite.Group(self.space_ship)
		self.screen = pg.display.set_mode(self.size)
		self.is_close_win = False
		self.button_home = Button((30, 30), (30, 30), self.screen, path='sprites/menu.png')


	def run(self):
		pg.init()
		pg.display.set_caption('Galaga')
		clock = pg.time.Clock()
		self.group.add(self.button_home)
		while self.running:
			self.screen.fill('black')
			for event in pg.event.get():
				if event.type == pg.QUIT:
					self.running = False
					self.is_close_win = True
				if event.type == pg.MOUSEBUTTONDOWN:
					if event.button == 4:
						self.space_ship.left_move()
					if event.button == 5:
						self.space_ship.right_move()
					if event.button == 1:
						if self.button_home.is_click(event.pos):
							print(999)
				if event.type == pg.KEYDOWN:
					if event.key == pg.K_LEFT:
						self.left_is_down = True
						self.frame_counter = config.FPS // self.step_shot

					if event.key == pg.K_RIGHT:
						self.right_is_down = True
						self.frame_counter = config.FPS // self.step_shot

					if event.key == pg.K_SPACE:
						self.space_is_down = True
						self.frame_counter = config.FPS // self.step_shot

				if event.type == pg.KEYUP:
					if event.key == pg.K_SPACE:
						self.space_is_down = False

					if event.key == pg.K_LEFT:
						self.left_is_down = False

					if event.key == pg.K_RIGHT:
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
			self.group.draw(self.screen)
			self.group.update()
			clock.tick(config.FPS)
			pg.display.update()
		# pg.quit()


	def is_close(self):
		return self.is_close_win


	def close(self):
		pg.quit()