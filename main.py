import pygame as pg
from Galaga import Galaga
import config
from Cursor import Cursor

games = {}
games_names_pos = []


def draw(screen, games_names):
	global games_names_pos
	screen.fill((0, 0, 0))
	font = pg.font.SysFont('monospace', 50)
	text = font.render("Выберите игру", True, ('white'))
	text_x = config.WIDTH // 2 - text.get_width() // 2
	text_y = config.HEIGHT // 5 - text.get_height() // 2
	screen.blit(text, (text_x, text_y))
	for h, name in enumerate(games_names):
		font = pg.font.SysFont("monospace", 30)
		text = font.render(name, True, ('white'))
		text_x = config.WIDTH // 2 - text.get_width() // 2
		text_y = config.HEIGHT // 15 * (h + 5) - text.get_height() // 2
		screen.blit(text, (text_x, text_y))
		games_names_pos.append([text_x - 10, text_y + text.get_height() // 2])


def main():
	pg.init()
	pg.display.set_caption('Games')
	size = config.WIDTH, config.HEIGHT
	screen = pg.display.set_mode(size)
	running = True
	clock = pg.time.Clock()
	cursor = Cursor(screen)
	draw(screen, config.GAMES_NAMES)
	correct_position = 0
	while running:
		draw(screen, config.GAMES_NAMES)
		cursor.update_pos(games_names_pos[correct_position % len(games_names_pos)])
		for event in pg.event.get():
			if event.type == pg.QUIT:
				running = False
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_DOWN:
					correct_position += 1
				if event.key == pg.K_UP:
					correct_position -= 1

		pg.display.flip()
		clock.tick(config.FPS)
	pg.quit()


if __name__ == '__main__':
	main()
