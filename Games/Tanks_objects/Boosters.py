import pygame as pg
from Games import config


class Booster(pg.sprite.Sprite):
    def __init__(self, game, pos):
        super().__init__(game.boosters_group)
        self.size = 30, 30  # размер улучшения
        self.game = game
        self.f = 1
        self.image = pg.image.load('Games/Tanks_objects/data/images/shield_booster.png')  # картинка спрайта  # контур спрайта
        self.image = pg.transform.scale(self.image, self.size)
        self.image.set_colorkey((0, 0, 0))
        self.image = self.image.convert_alpha()
        self.can_move = True
        self.pos = pos[0] * config.TILE_SIZE, pos[1] * config.TILE_SIZE
        self.step = 0
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.pos
        self.y = self.rect.y
        self.active_boost = False

    def set_can_move(self, f):
        self.can_move = f

    def update(self, *args):
        if 10 > self.step and self.f:
            self.step += 0.05
            self.y += 0.05
        elif self.step > 0:
            self.f = 0
            self.step -= 0.05
            self.y -= 0.05
        else:
            self.f = 1
        self.rect.y = self.y

        if self.game.main_tank in pg.sprite.spritecollide(self, self.game.tanks_group, False):
            self.boost()


    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)


    def boost(self):
        pass


class ShieldBooster(Booster):
    def boost(self):
        self.active_boost = True

    def update(self, *args):
        super().update()
        if self.active_boost:
            self.image = pg.image.load('Games/Tanks_objects/data/images/None.png')
            self.image = pg.transform.scale(self.image, (config.TILE_SIZE * 2 ** 0.5, config.TILE_SIZE * 2 ** 0.5))
            pg.draw.circle(self.game.screen, 'blue', (self.game.main_tank.rect.x + config.TILE_SIZE // 2,
                                                      self.game.main_tank.rect.y + config.TILE_SIZE // 2),
                           config.TILE_SIZE * 2 ** 0.5 // 2, 3)
            print(pg.sprite.spritecollide(self, self.game.fires_group, False))
            for fire in pg.sprite.spritecollide(self, self.game.fires_group, False):
                print(fire.from_main_tank)
                if not fire.from_main_tank:
                    fire.kill()
