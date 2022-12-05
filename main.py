import pygame as pg
from random import randint
import config
from SpaceShip import SpaceShip
from Fire import Fire


def main():
    pg.init()
    pg.display.set_caption('Galaga')
    size = config.WIDTH, config.HEIGHT
    screen = pg.display.set_mode(size)
    space_ship = SpaceShip('sprites/spaceship4.png', (config.WIDTH // 2, config.HEIGHT // 15 * 14))
    group = pg.sprite.Group(space_ship)

    running = True
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
                    space_ship.left_move()
                if event.key == pg.K_RIGHT:
                    space_ship.right_move()

                if event.key == pg.K_SPACE:
                    group.add(Fire('sprites/fire1.png', (space_ship.rect.x + space_ship.size // 2, space_ship.rect.y)))

        group.draw(screen)
        pg.display.update()
        group.update()
        clock.tick(config.FPS)
    pg.quit()



if __name__ == '__main__':
    main()