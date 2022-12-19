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
        self.game = game
        self.text_coord = 50
        self.vis_kills = self.game.kill_counts[:]
        self.rect = self.image.get_rect()

    def update(self):
        self.text_coord = config.HEIGHT // 2
        if sum(self.vis_kills) > 0:
            self.game.screen.blit(self.image, (0, 0))
        self.print_text()

    def print_text(self):
        for kills1, j in enumerate(self.vis_kills):
            if kills1 > 0:
                font = pg.font.Font(None, 50)
                string_rendered = font.render(str(kills1), 1, pg.Color('white'))
                intro_rect = string_rendered.get_rect()
                intro_rect.top = self.text_coord
                intro_rect.x = config.WIDTH // 4 * 3
                self.text_coord += intro_rect.height
                self.game.screen.blit(string_rendered, intro_rect)
                self.vis_kills[j] -= 1
                print(self.vis_kills)
                return True
            self.text_coord += 70
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
