import pygame as pg
import config
from SpaceShip import SpaceShip
from Fire import Fire


class Galaga:
	def run(self):
		pg.init()
		pg.display.set_caption('Galaga')
		size = config.WIDTH, config.HEIGHT
		screen = pg.display.set_mode(size)
		space_ship = SpaceShip('sprites/spaceship4.png', (config.WIDTH // 2, config.HEIGHT // 15 * 14))
		group = pg.sprite.Group(space_ship)
		step_shot = 5  # сколько раз в секунду можно создавать выстрел
		step_move = 10
		running = True
		space_is_down = False
		left_is_down = False
		right_is_down = False
		frame_counter = 0
		clock = pg.time.Clock()
		while running:
			screen.fill('black')
			for event in pg.event.get():
				if event.type == pg.QUIT:
					running = False
				if event.type == pg.MOUSEBUTTONDOWN:
					if event.button == 4:
						space_ship.left_move()

					if event.button == 5:
						space_ship.right_move()
				if event.type == pg.KEYDOWN:
					if event.key == pg.K_LEFT:
						left_is_down = True
						frame_counter = config.FPS // step_shot

					if event.key == pg.K_RIGHT:
						right_is_down = True
						frame_counter = config.FPS // step_shot

					if event.key == pg.K_SPACE:
						space_is_down = True
						frame_counter = config.FPS // step_shot

				if event.type == pg.KEYUP:
					if event.key == pg.K_SPACE:
						space_is_down = False

					if event.key == pg.K_LEFT:
						left_is_down = False

					if event.key == pg.K_RIGHT:
						right_is_down = False
			if frame_counter == config.FPS // step_shot:
				frame_counter = 0
				if space_is_down:
					group.add(Fire('sprites/fire1.png', (space_ship.rect.x + space_ship.size // 2, space_ship.rect.y)))

			if frame_counter == config.FPS // step_move:
				if left_is_down:
					space_ship.left_move()
				if right_is_down:
					space_ship.right_move()

			frame_counter += 1
			frame_counter = frame_counter % config.FPS
			group.draw(screen)
			pg.display.update()
			group.update()
			clock.tick(config.FPS)
		pg.quit()