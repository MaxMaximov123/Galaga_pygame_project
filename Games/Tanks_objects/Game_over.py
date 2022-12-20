from random import randint
import pygame as pg
import sys
from Games import config
from Games.Tanks_objects.Print_kills import print_kills


class GameOver(pg.sprite.Sprite):
    def __init__(self, game):
        super().__init__(game.pause_group)
        self.base_img = pg.image.load(
            'Games/Tanks_objects/data/images/gameover.png').convert_alpha()
        self.image = self.base_image = pg.transform.scale(self.base_img, (config.WIDTH, config.HEIGHT))
        self.speed = 200
        self.images = []
        for i in range(4):
            tank_img = pg.image.load(f'Games/Tanks_objects/data/images/enemy_tank{i}.png').convert_alpha()
            tank_img = pg.transform.scale(tank_img, (40, 40))
            tank_img = pg.transform.rotate(tank_img, -90)
            self.images.append(tank_img)
        self.game = game
        self.text_coord = 50
        self.vis_kills = [-1, -1, -1, -1]
        self.rect = self.image.get_rect()
        self.rect.x = -self.rect.width

    def update(self):
        if self.rect.x < 0:
            self.rect.x += self.speed / config.FPS
        else:
            self.text_coord = config.HEIGHT // 8 * 2.5
            self.game.screen.blit(self.base_image, (0, 0))
            print_kills(self)


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
