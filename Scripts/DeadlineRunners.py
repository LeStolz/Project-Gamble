import pygame
from Scenes import *
from Classes import *
from math import e
from copy import copy
from random import shuffle
from pygame.transform import average_color


class DeadlineRunnersGameScene(MenuScene):
	def __init__(self, game, title):
		MenuScene.__init__(self, game, title)

		self.direction = Vector(0, 0)

		self.height_car = 100
		self.height_car = 50
		self.finish_line = self.game.W - 150
		self.cars = [[0, self.game.H / 6 * x] for x in range(1,6)]
		self.click = 0
		self.speed = [0, 0, 0, 0, 0]


	def draw_options(self):
		self.running = True
		self.speed = Car.speed_car(self)

		ob = Obstacle(self.game, self.title, self.cars, self.speed)
		ob.range_Obstacle()

		while self.running:
			self.check_input()
			self.mode_speed()

			self.game.display.fill(self.game.BLACK)
			self.game.window.blit(self.game.display, (0, 0))

			Background.move(self)
			Background.draw(self)

			for x in range (5):
				Car.draw_car(self, x)

			ob.draw_Obstacle()
			print('cool')

			pygame.display.update()


	def check_input(self):
		self.game.check_input()


	def mode_speed(self):
		self.game.check_input()

		if self.game.K_SPACE:
			self.game.reset_input()

			if self.click == 0:
				for x in range (5):
					self.speed[x] *= 2
			else:
				for x in range (5):
					self.speed[x] /= 2

			self.click = (self.click + 1) % 2


class Car(DeadlineRunnersScene):
	def draw_car(self, n):
		Car.pos_car(self, n)

		pygame.draw.rect(self.game.window, self.game.GREEN, (self.cars[n][0], self.cars[n][1], 100, self.height_car))


	def speed_car(self):
		self.speed_temp = [3, 3.5, 4, 4.5, 5]

		shuffle(self.speed_temp)

		self.speed = self.speed_temp[:]

		return self.speed


	def pos_car(self, n):
		if self.cars[n][0] < self.game.W - 150:
			self.cars[n][0] += self.speed[n]
		flag = 0
		for i in range (5):
			if self.cars[i][0] >= self.game.W - 150:
				flag += 1
			if flag == 5:
				for x in range (5):
					self.cars[x][0] = 0
					self.running = False

				Car.speed_car(self)

				self.click = 0


class Background(DeadlineRunnersScene):
	pos_bg = 0
	speed_bg = 0


	def draw(self):
		pass


	def move(self):
		self.pos_bg = Background.pos_bg
		Background.pos_bg -= Background.speed_bg

		flag = False
		for i in range (5):
			if self.cars[i][0] >= self.game.W - 150:
				flag = True
		if flag:
			self.temp = Background.speed_bg
			Background.speed_bg = 0


		else:
			Background.speed_bg = max(self.speed)
		flag = 0
		for i in range (5):
			if self.cars[i][0] <= 10:
				flag += 1
		if flag == 5:
			Background.pos_bg = 0
			self.pos_bg = 0


		if Background.speed_bg == 0:
			for x in range(5):
				self.speed[x] += self.temp


class Obstacle(DeadlineRunnersScene):
	def __init__(self, game, title, Cars, speed):
		super().__init__(game, title)
		self.cars = Cars
		self.speed = speed

		self.Ob = [[self.game.W, self.game.H / 6 * x] for x in range(1,6)]
		self.width_Obstacle = 50
		self.height_Obstacle = 50
		self.speed_temp_ob = [0, 0]

		self.rand = [0, 0]
		self.start = [1, 1]
		self.flag = [1, 1]
		self.count = [0, 0]


	def range_Obstacle(self):
		self.rand_temp = [0, 1, 2, 3, 4]
		shuffle(self.rand_temp)

		if self.flag[0]:
			self.rand[0] = self.rand_temp[0]
			self.Ob[self.rand[0]][0] += 200
		if self.flag[1]:
			self.rand[1] =  self.rand_temp[1]

		self.speed_temp_ob[0] = self.speed[self.rand[0]]
		self.speed_temp_ob[1] = self.speed[self.rand[1]]


	def draw_Obstacle(self):
		if self.count[0] == 2:
			self.start[0] = 0
		if self.count[1] == 2:
			self.start[1] = 0

		Obstacle.speed(self)
		Obstacle.move(self)
		Obstacle.check(self)

		if self.start[0] == 1:
			pygame.draw.rect(self.game.window, self.game.RED, (self.Ob[self.rand[0]][0], self.Ob[self.rand[0]][1], self.width_Obstacle, self.height_Obstacle))

		if self.start[1] == 1:
			pygame.draw.rect(self.game.window, self.game.RED, (self.Ob[self.rand[1]][0], self.Ob[self.rand[1]][1], self.width_Obstacle, self.height_Obstacle))


	def speed(self):
		self.speed_Ob = 10


	def move(self):
		if self.start[0] == 1:
			self.Ob[self.rand[0]][0] -= self.speed_Ob

			if self.Ob[self.rand[0]][0] < 0:
				self.Ob[self.rand[0]][0] = self.game.W
				self.flag[1] = 0
				self.flag[0] = 1
				self.count[0] += 1
				self.range_Obstacle()

		if self.start[1] == 1:
			self.Ob[self.rand[1]][0] -= self.speed_Ob

			if self.Ob[self.rand[1]][0] < 0:
				self.Ob[self.rand[1]][0] = self.game.W
				self.flag[0] = 0
				self.flag[1] = 1
				self.count[1] += 1
				self.range_Obstacle()


	def check(self):
		if self.start[0] == 1:
			if (self.Ob[self.rand[0]][0] - (self.cars[self.rand[0]][0] + 100)) <=  20 and (self.Ob[self.rand[0]][0] - (self.cars[self.rand[0]][0] + 100)) >= -50:
				self.speed[self.rand[0]] = -4
			else:
				self.speed[self.rand[0]] = self.speed_temp_ob[0]

			if self.cars[0][0] >= self.game.W - 150 or self.cars[1][0] >= self.game.W - 150 or self.cars[2][0] >= self.game.W - 150 or self.cars[3][0] >= self.game.W - 150 or self.cars[4][0] >= self.game.W - 150:
				self.start[0] = 0
				self.speed[self.rand[0]] = self.speed_temp_ob[0]

		if self.start[1] == 1:
			if (self.Ob[self.rand[1]][0] - (self.cars[self.rand[1]][0] + 100)) <=  20 and (self.Ob[self.rand[1]][0] - (self.cars[self.rand[1]][0] + 100)) >= -50:
				self.speed[self.rand[1]] = -4
			else:
				self.speed[self.rand[1]] = self.speed_temp_ob[1]

			if self.cars[0][0] >= self.game.W - 150 or self.cars[1][0] >= self.game.W - 150 or self.cars[2][0] >= self.game.W - 150 or self.cars[3][0] >= self.game.W - 150 or self.cars[4][0] >= self.game.W - 150:
				self.start[1] = 0
				self.speed[self.rand[1]] = self.speed_temp_ob[1]