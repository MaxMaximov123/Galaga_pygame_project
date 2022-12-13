import pygame as pg
from Games import config


class MainTank(pg.sprite.Sprite):
	def __init__(self, pos, game, power=0):
		super().__init__(game.tanks_group, game.all_groups)
		self.pos = pos
		self.size = config.WIDTH // config.SIZE_BOARD_FOR_TANKS[0]  # размер танка
		self.speed = config.FPS * 1  # пикселе в секунду
		self.powers = ['Games/Tanks_objects/data/images/main_tank0.png']
		self.power = power
		self.base_image = pg.image.load(f'Games/Tanks_objects/data/images/main_tank{power}.png').convert_alpha()  # картинка спрайта
		self.base_image = pg.transform.scale(self.base_image, (self.size, self.size))
		self.image = self.base_image
		self.rect = self.image.get_rect(center=self.pos)  # контур спрайта
		self.game = game
		self.vector_x = 0
		self.vector_y = -1
		self.can_move = True

	def set_can_move(self, f):
		self.can_move = f

	def update(self, *args):
		pass


	def left_move(self):  # движение влево
		if self.rect.x > 0 and self.can_move:
			self.image = pg.transform.rotate(self.base_image, 90)
			self.rect.x -= self.speed / config.FPS
			self.vector_x = -1
			self.vector_y = 0

	def right_move(self):  # движение вправо
		if self.rect.x + self.size < config.WIDTH and self.can_move:
			self.image = pg.transform.rotate(self.base_image, -90)
			self.rect.x += self.speed / config.FPS
			self.vector_x = 1
			self.vector_y = 0


	def up_move(self):  # движение влево
		if self.rect.y > 0 and self.can_move:
			self.image = pg.transform.rotate(self.base_image, 0)
			self.rect.y -= self.speed / config.FPS
			self.vector_x = 0
			self.vector_y = -1

	def down_move(self):  # движение вправо
		if self.rect.y + self.size < config.HEIGHT and self.can_move:
			self.image = pg.transform.rotate(self.base_image, 180)
			self.rect.y += round(self.speed / config.FPS)
			self.vector_x = 0
			self.vector_y = 1


	def is_collided_with(self, sprite):
		return self.rect.colliderect(sprite.rect)


class EnemyTank0(MainTank):
	def __init__(self, power, pos, game):
		super().__init__(power, pos, game)