import time
from random import randint
import pygame as pg
import sys
from Games import config


class WinScreen(pg.sprite.Sprite):
    def __init__(self, game):
        super().__init__(game.pause_group)
        self.base_img = pg.image.load(
            'Games/Tanks_objects/data/images/you_win.jpg').convert_alpha()
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

    def update(self):
        self.text_coord = config.HEIGHT // 8 * 5
        self.game.screen.blit(self.base_image, (0, 0))
        self.print_text()

    def print_text(self):
        for j in range(len(self.vis_kills)):
            if self.vis_kills[j] < self.game.kill_counts[j]:
                self.vis_kills[j] += 0.015
                break
        for i in range(len(self.vis_kills)):
            if self.vis_kills[i] >= 0:
                font = pg.font.Font(None, 50)
                string_rendered = font.render(str(round(self.vis_kills[i])), 1, pg.Color('white'))
                intro_rect = string_rendered.get_rect()
                intro_rect.top = self.text_coord
                intro_rect.x = config.WIDTH // 7 * 4
                self.game.screen.blit(self.images[i], (config.WIDTH // 7 * 3, self.text_coord))
                self.text_coord += intro_rect.height
                self.game.screen.blit(string_rendered, intro_rect)
            self.text_coord += 15
        return False



if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((config.WIDTH, config.HEIGHT))
    all_sprites = pg.sprite.Group()
    all_sprites.add(WinScreen('data/you_win.jpg'))
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
