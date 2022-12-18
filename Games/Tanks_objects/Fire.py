import pygame as pg
from Games import config


class Fire(pg.sprite.Sprite):
	def __init__(self, game, pos, from_main_tank=False, vector_x=0, vector_y=1):
		super().__init__(game.fires_group)
		self.step_show = 1
		self.frame_counter = self.step_show // config.FPS
		self.size = 20, 40  # размер пули
		self.speed = config.FPS * 2  # скорость пули пикс/сек
		self.game = game
		self.image = pg.image.load('Games/Tanks_objects/data/images/fire1.png').convert_alpha()  # картинка спрайта  # контур спрайта
		self.can_move = True
		self.from_main_tank = from_main_tank
		self.vector_x = vector_x * self.speed
		self.vector_y = vector_y * self.speed
		self.image = pg.transform.scale(self.image, self.size)
		if vector_x == 1:
			angle = -90
		elif vector_x == -1:
			angle = 90
		elif vector_y == 1:
			angle = 180
		else:
			angle = 0
		self.pos = pos
		self.image = pg.transform.rotate(self.image, angle)
		self.rect = self.image.get_rect(center=pos)

	def set_can_move(self, f):
		self.can_move = f

	def update(self, *args):
		if self.can_move:
			if (
					config.HEIGHT > self.rect.y + self.size[1] // 2 > + self.size[1] // 2 and
					config.WIDTH + self.size[0] // 2 > self.rect.x + self.size[0] // 2 > 0):  # ПРОВЕРКА, ЧТО ПУЛИ НА ЭКРАНЕ
				self.rect.y += self.vector_y / config.FPS
				self.rect.x += self.vector_x / config.FPS
			else:
				self.kill()

			if any([i.destruction(self) for i in pg.sprite.spritecollide(self, self.game.walls_group, False)]):  # ПРОВЕРКА КАСАНИЯ СО СТЕНОЙ
				# ИЗМЕНЕНИЕ СТЕНЫ ПРИ КАСАНИИ
				self.kill()

			if (
					pg.sprite.spritecollideany(self, self.game.tanks_group) and
					((
							not self.from_main_tank and
							pg.sprite.spritecollideany(self, self.game.tanks_group) == self.game.main_tank) or (
							self.from_main_tank and
							pg.sprite.spritecollideany(self, self.game.tanks_group) != self.game.main_tank))):  # ПРОВЕРКА КАСАНИЯ С ТАНКОМ
				pg.sprite.spritecollideany(self, self.game.tanks_group).hp -= 1  # ИЗМЕНЕНИЕ КОЛ-ВА ЖИЗНЕЙ
				pg.sprite.spritecollideany(self, self.game.tanks_group).draw_hp()
				self.kill()
			if pg.sprite.spritecollide(self, self.game.fires_group, False):
				obj = pg.sprite.spritecollide(self, self.game.fires_group, False)
				if self in obj:
					obj.remove(self)
				if obj and self.from_main_tank != obj[0].from_main_tank:
					self.kill()
					obj[0].kill()

	def is_collided_with(self, sprite):
		return self.rect.colliderect(sprite.rect)
