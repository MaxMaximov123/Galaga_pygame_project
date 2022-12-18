from random import randint
import pygame as pg
import sys
from Games import config


class GameOver(pg.sprite.Sprite):
    def __init__(self, game):
        super().__init__(game.pause_group)
        self.base_img = pg.image.load(
            'Games/Tanks_objects/data/images/gameover2.png').convert_alpha()
        self.image = self.base_image = pg.transform.scale(self.base_img, (config.WIDTH, config.HEIGHT))
        self.speed = 200
        self.rect = self.image.get_rect()
        self.rect.x = -self.rect.width

    def update(self):
        if self.rect.x < 0:
            self.rect.x += self.speed / config.FPS
        # self.rect.x, self.rect.y = pos

    # координата x будет случайна


if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((config.WIDTH, config.HEIGHT))
    all_sprites = pg.sprite.Group()
    all_sprites.add(GameOver('data/gameover.png'))
    clock = pg.time.Clock()
    while 1:
        screen.fill('blue')
        for event1 in pg.event.get():
            if event1.type == pg.QUIT:
                sys.exit()

        all_sprites.update()
        all_sprites.draw(screen)
        pg.display.flip()
        clock.tick(config.FPS)
