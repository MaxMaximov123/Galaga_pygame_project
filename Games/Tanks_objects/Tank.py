import pygame as pg
from Games import config
from Games.Tanks_objects.Fire import Fire
import random
from copy import deepcopy
import time


class MainTank(pg.sprite.Sprite):
	def __init__(self, pos, game, power=0):
		super().__init__(game.tanks_group)
		self.pos = pos
		self.copy_img = None
		self.size = config.TILE_SIZE - 4  # размер танка
		self.speed = 300  # пикселе в секунду
		self.powers = ['Games/Tanks_objects/data/images/main_tank0.png']
		self.power = power
		self.base_image = pg.image.load(f'Games/Tanks_objects/data/images/main_tank{power}.png')  # картинка спрайта
		self.base_image.set_colorkey(self.base_image.get_at((0, 0)))
		self.base_image = self.base_image.convert_alpha()
		self.base_image = pg.transform.scale(self.base_image, (self.size, self.size))
		self.image = pg.transform.rotate(self.base_image, 0)
		self.rect = self.image.get_rect(center=self.pos)  # контур спрайта
		self.time_og_showing_hp = 0.1  # КАКУЮ ЧАСТЬ СЕКУНДЫ БУДЕТ ПОКАЗЫВАТЬСЯ HP
		self.game = game
		self.vector_x = 0
		self.vector_y = -1
		self.can_move = True
		self.x, self.y = self.rect.x, self.rect.y
		self.hp = self.power + 1
		self.frame_for_drawing_hp = None
		self.frame_counter = 0
		self.do_rotation = False

	def set_can_move(self, f):
		self.can_move = f

	def update(self, *args):
		"""Обновление всех состояний танков"""
		if not self.game.is_pause:
			self.frame_counter += 1
			if self.frame_counter >= config.FPS:
				self.frame_counter = 0
			if self.hp <= 0 and self == self.game.main_tank:
				self.game.game_over()
				self.kill()
			elif self.hp <= 0:
				self.game.kill_counts[self.power] += 1
				self.kill()
			self.rect.x, self.rect.y = self.x, self.y
			if self.frame_for_drawing_hp:
				if (  # отрисовка HP
					self.frame_for_drawing_hp + config.FPS // self.time_og_showing_hp) % config.FPS <= self.frame_counter:
					self.draw_hp(f=False)
				else:
					self.frame_for_drawing_hp = None

	def tank_can_move(self):
		if pg.sprite.spritecollide(self, self.game.tanks_group, False):  # СТОЛКНОВЕНИЕ С ТАНКОМ
			obj = pg.sprite.spritecollide(self, self.game.tanks_group, False)
			if self in obj:
				obj.remove(self)
				if obj:
					self.step_back(self, step=1)
					self.do_rotation = True

		if any([i.tank_can_move() for i in pg.sprite.spritecollide(self, self.game.walls_group, False)]):  # СТОЛКНОВЕНИЕ СО СТЕНОЙ
			self.step_back(self, step=1)
			self.do_rotation = True

		if pg.sprite.spritecollide(self, self.game.tanks_group, False):
			obj = pg.sprite.spritecollide(self, self.game.tanks_group, False)
			if self in obj:
				obj.remove(self)
			if (
					obj or not (config.WIDTH - self.size > self.x >= 0)
					or not (config.HEIGHT - self.size > self.y >= 0)):
				self.do_rotation = True
				self.set_can_move(False)
				return False
		self.set_can_move(True)
		return True

	def left_move(self, f=True):  # движение влево
		self.tank_can_move()
		if self.x >= 0:
			if f:
				self.image = pg.transform.rotate(self.base_image, 90)
			self.x -= self.speed / config.FPS
			self.vector_x = -1
			self.vector_y = 0

	def right_move(self, f=True):  # движение вправо
		self.tank_can_move()
		if self.x + self.size <= config.WIDTH:
			if f:
				self.image = pg.transform.rotate(self.base_image, -90)
			self.x += self.speed / config.FPS
			self.vector_x = 1
			self.vector_y = 0

	def up_move(self, f=True):  # движение влево
		self.tank_can_move()
		if self.y >= 0:
			if f:
				self.image = pg.transform.rotate(self.base_image, 0)
			self.y -= self.speed / config.FPS
			self.vector_x = 0
			self.vector_y = -1

	def down_move(self, f=True):  # движение вправо
		self.tank_can_move()
		if self.y + self.size <= config.HEIGHT:
			if f:
				self.image = pg.transform.rotate(self.base_image, 180)
			self.y += self.speed / config.FPS
			self.vector_x = 0
			self.vector_y = 1

	def is_collided_with(self, sprite):
		return self.rect.colliderect(sprite.rect)

	def draw_hp(self, f=True):
		font = pg.font.SysFont('monospace', 30)
		text = font.render(str(100 * self.hp), True, (255, 0, 0))
		self.image.blit(text, (0, 0))
		if f:
			self.frame_for_drawing_hp = self.frame_counter - 1


	def step_back(self, tank, step=1, rev=False):
		if rev:
			if config.WIDTH >= tank.x + tank.speed / config.FPS * tank.vector_x * step + tank.size >= tank.size:
				tank.x += tank.speed / config.FPS * tank.vector_x * step
			if config.HEIGHT >= tank.y + tank.speed / config.FPS * tank.vector_y * step + tank.size >= tank.size:
				tank.y += tank.speed / config.FPS * tank.vector_y * step
		else:
			if config.WIDTH >= tank.x - tank.speed / config.FPS * tank.vector_x * step + tank.size >= tank.size:
				tank.x -= tank.speed / config.FPS * tank.vector_x * step
			if config.HEIGHT >= tank.y - tank.speed / config.FPS * tank.vector_y * step + tank.size >= tank.size:
				tank.y -= tank.speed / config.FPS * tank.vector_y * step
		self.rect.x, self.rect.y = self.x, self.y
		# self.set_can_move(True)


class EnemyTank(MainTank):
	def __init__(self, pos, game, power):
		super().__init__(pos, game, power)
		self.shot_time = 1  # выстрелов в секунду
		self.base_image = pg.image.load(f'Games/Tanks_objects/data/images/enemy_tank{power}.png')  # картинка спрайта
		self.base_image = pg.transform.scale(self.base_image, (self.size, self.size))
		self.base_image.set_colorkey(self.base_image.get_at((0, 0)))
		self.base_image = self.base_image.convert_alpha()
		self.vector_x = random.randint(-1, 1)
		self.speed = 100
		if self.vector_x == 0:
			self.vector_y = random.choice([-1, 1])
		else:
			self.vector_y = 0
		if self.vector_x:  # ПОВОРОТ КАРТИНКИ
			self.image = pg.transform.rotate(self.base_image, -90 * self.vector_x)
		if self.vector_y:
			if self.vector_y > 0:
				self.image = pg.transform.rotate(self.base_image, 180 * self.vector_y)
			else:
				self.image = pg.transform.rotate(self.base_image, 0)
		self.image.set_colorkey(-1)
		self.rect = self.image.get_rect()
		self.moves = [self.left_move, self.right_move, self.up_move, self.down_move]
		self.moves_by_power = [self.move0, self.move1, self.move2, self.move3]
		if power == 1:
			self.speed *= 1.2
		self.rect.x, self.rect.y = self.x, self.y = (
			pos[0] * config.WIDTH // config.SIZE_BOARD_FOR_TANKS[0],
			pos[1] * config.WIDTH // config.SIZE_BOARD_FOR_TANKS[0])
		self.game = game

	def move0(self):
		if self.vector_x == 1:
			self.right_move()
		if self.vector_x == -1:
			self.left_move()
		if self.vector_y == 1:
			self.down_move()
		if self.vector_y == -1:
			self.up_move()

	def move1(self):
		self.move0()

	def move2(self):
		self.move0()

	def move3(self):
		self.move0()

	def update(self, *args):
		super().update(args)
		if not self.game.is_pause:
			if (config.FPS // self.shot_time) % config.FPS == self.frame_counter:
				Fire(self.game, (
					self.rect.x + self.size // 2,
					self.rect.y + self.size // 2), False, self.vector_x, self.vector_y)
			if self.do_rotation:
				random.choice(self.moves)(f=False)
				self.do_rotation = False
			else:
				self.moves_by_power[self.power]()
			if self.frame_for_drawing_hp:
				if (  # отрисовка HP
					self.frame_for_drawing_hp + config.FPS // self.time_og_showing_hp) % config.FPS <= self.frame_counter:
					self.draw_hp(f=False)
				else:
					self.frame_for_drawing_hp = None

