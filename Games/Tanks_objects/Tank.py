import pygame as pg
from Games import config
import random


class MainTank(pg.sprite.Sprite):
	def __init__(self, pos, game, power=0):
		super().__init__(game.tanks_group)
		self.pos = pos
		self.size = config.WIDTH // config.SIZE_BOARD_FOR_TANKS[0]  # размер танка
		self.speed = 300  # пикселе в секунду
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
		self.x, self.y = self.rect.x, self.rect.y
		self.hp = power + 1

	def set_can_move(self, f):
		self.can_move = f

	def update(self, *args):
		if not self.can_move:
			self.x -= self.vector_x
			self.y -= self.vector_y
			# self.set_can_move(True)
		if self.hp <= 0:
			self.kill()
		self.rect.x, self.rect.y = self.x, self.y



	def tank_can_move(self):
		if pg.sprite.spritecollide(self, self.game.tanks_group, False):
			obj = pg.sprite.spritecollide(self, self.game.tanks_group, False)
			obj.remove(self)
			if obj:
				self.set_can_move(False)
				self.update()
				return False
		self.set_can_move(True)
		return True


	def left_move(self):  # движение влево
		self.tank_can_move()
		if self.x > 0 and self.can_move:
			self.image = pg.transform.rotate(self.base_image, 90)
			self.x -= self.speed / config.FPS
			self.vector_x = -1
			self.vector_y = 0

	def right_move(self):  # движение вправо
		self.tank_can_move()
		if self.x + self.size < config.WIDTH and self.can_move:
			self.image = pg.transform.rotate(self.base_image, -90)
			self.x += self.speed / config.FPS
			self.vector_x = 1
			self.vector_y = 0


	def up_move(self):  # движение влево
		self.tank_can_move()
		if self.y > 0 and self.can_move:
			self.image = pg.transform.rotate(self.base_image, 0)
			self.y -= self.speed / config.FPS
			self.vector_x = 0
			self.vector_y = -1

	def down_move(self):  # движение вправо
		self.tank_can_move()
		if self.y + self.size < config.HEIGHT and self.can_move:
			self.image = pg.transform.rotate(self.base_image, 180)
			self.y += round(self.speed / config.FPS)
			self.vector_x = 0
			self.vector_y = 1


	def is_collided_with(self, sprite):
		return self.rect.colliderect(sprite.rect)


class EnemyTank(MainTank):
	def __init__(self, pos, game, power):
		super().__init__(pos, game, 0)
		self.base_image = pg.image.load(f'Games/Tanks_objects/data/images/enemy_tank{power}.png').convert_alpha()  # картинка спрайта
		self.base_image = pg.transform.scale(self.base_image, (self.size, self.size))
		self.image = self.base_image
		self.image.set_colorkey(-1)
		self.rect = self.image.get_rect()
		self.moves = [self.left_move, self.right_move, self.up_move, self.down_move]
		self.moves_by_power = [self.move0, self.move1, self.move2, self.move3]
		if power == 1:
			self.speed *= 2
		self.rect.x, self.rect.y = self.x, self.y = (
			pos[0] * config.WIDTH // config.SIZE_BOARD_FOR_TANKS[0],
			pos[1] * config.WIDTH // config.SIZE_BOARD_FOR_TANKS[0])


	def move0(self):
		self.tank_can_move()
		self.moves[0]()

	def move1(self):
		pass

	def move2(self):
		pass

	def move3(self):
		pass


	def update(self, *args):
		self.moves_by_power[self.power]()
		if not self.can_move:
			self.x -= self.vector_x
			self.y -= self.vector_y
			# self.set_can_move(True)
		if self.hp <= 0:
			self.kill()
		self.rect.x, self.rect.y = self.x, self.y