import pygame
from random import *
from Scenes import *
from Classes import *


class DeadlineRunnersGameScene(GameScene):
	def __init__(self, game, title):
		GameScene.__init__(self, game, title)

		self.finish_line = self.game.W - 150


	def draw_scene(self):
		self.running = True

		self.Car = Car(self.game, self.title)
		self.speed_cars = self.Car.speed_car()

		self.Background = Background(self.game, self.title, self.speed_cars, self.Car.cars)

		self.Obstacle = Obstacle(self.game, self.title, self.speed_cars, self.Car.cars)
		self.Obstacle.range_ob()

		self.Point = Point(self.game, self.title, self.speed_cars, self.Car.cars)
		self.count_po = self.Point.move_po()

		self.Skill = Skill(self.game, self.title, self.speed_cars, self.Car.cars, self.count_po)


		while self.running:
			self.check_input()

			self.game.display.fill(self.game.BLACK)
			self.game.window.blit(self.game.display, (0, 0))

			self.Background.draw_bg()

			for n in range (5):
				self.Car.draw_car(n)

			self.Point.draw_po()
			self.Obstacle.draw_ob()
			self.Skill.range_skill()

			pygame.display.update()


	def check_input(self):
		self.game.check_input()


class Car(DeadlineRunnersScene):
	def __init__(self, game, title):
		DeadlineRunnersScene.__init__(self, game, title)
		self.width_car, self.height_car = 100, 50
		self.finish_line = self.game.W - 150
		self.cars = [[0, self.game.H / 6 * x] for x in range(1,6)]
		self.flag_draw_car = [True for i in range (5)]


	def draw_car(self, n):
		if self.flag_draw_car[n]:
			Car.pos_car(self, n)
			pygame.draw.rect(self.game.window, self.game.GREEN, (self.cars[n][0], self.cars[n][1], self.width_car, self.height_car))


	def speed_car(self):
		self.speed_temp = [0.2, 0.25, 0.3, 0.25, 0.2]

		shuffle(self.speed_temp)

		self.speed_cars = self.speed_temp[:]

		return self.speed_cars


	def pos_car(self, n):
		if self.cars[n][0] <= self.finish_line:
			self.cars[n][0] += self.speed_cars[n]


class Background(DeadlineRunnersScene):
	def __init__(self, game, title, speed_cars, cars):
		DeadlineRunnersScene.__init__(self, game, title)
		self.speed_cars = speed_cars
		self.speed_cars_temp = [speed_cars[i] + 1 for i in range (5)]
		self.cars = cars
		self.pos_bg = 0
		self.finish_line = self.game.W - 150
		self.BG = pygame.transform.scale(self.game.deadline_runners_assets['Background'].image, (self.game.W, self.game.H))
		self.BG = pygame.transform.scale(self.BG, (10000, 720))
		self.width_bg = self.BG.get_width()


	def draw_bg (self):
		self.move_bg()

		self.game.window.blit(self.BG, (self.pos_bg, 0))


	def speed_bg(self):
		self.speed_bg = 1


	def move_bg (self):
		Background.speed_bg(self)

		flag = False

		for i in range (5):
			if self.cars[i][0] >= self.finish_line:
				flag = True

		if flag:
			self.speed_bg = 0
			for i in range (5):
				self.speed_cars[i] = self.speed_cars_temp[i]

		self.pos_bg -= self.speed_bg


class Obstacle(DeadlineRunnersScene):
	def __init__(self, game, title, speed_cars, cars):
		DeadlineRunnersScene.__init__(self, game, title)
		self.speed_cars = speed_cars
		self.speed_cars_temp = speed_cars[:]
		self.cars = cars
		self.finish_line = self.game.W - 150
		self.y_ob = self.game.H / 6
		self.width_Obstacle = 50
		self.height_Obstacle = 50
		self.width_car = 100
		self.time = [0 for i in range (5)]
		self.start_ob = True
		self.flag_ob = [True, True]
		self.lane_ob = [0 for i in range(5)]


	def draw_ob (self):
		if self.start_ob:
			self.move_ob()

			pygame.draw.rect(self.game.window, self.game.RED, (self.pos_ob[0], self.y_ob * self.lane_ob[0], self.width_Obstacle, self.height_Obstacle))
			pygame.draw.rect(self.game.window, self.game.RED, (self.pos_ob[1], self.y_ob * self.lane_ob[1], self.width_Obstacle, self.height_Obstacle))


	def range_ob (self):
		self.pos_ob_temp = [self.game.W + 100 * i for i in range (1, 6)]

		shuffle(self.pos_ob_temp)

		self.pos_ob = self.pos_ob_temp[:]

		self.lane_ob_temp = [1, 2, 3, 4, 5]

		shuffle(self.lane_ob_temp)

		self.lane_ob = self.lane_ob_temp[:]

		return self.pos_ob[2], self.lane_ob[2], self.lane_ob

	def Speed_ob(self):
		self.speed_ob = 1.5


	def move_ob(self):
		self.Speed_ob()

		self.pos_ob[0] -= self.speed_ob
		self.pos_ob[1] -= self.speed_ob

		if self.pos_ob[0] <= 0 and self.pos_ob[1] <= 0:
			self.range_ob()

		# ob 1
		if self.flag_ob[0]:
			if abs(self.pos_ob[0] - self.cars[self.lane_ob[0] - 1][0] - self.width_car) <= 5:
				self.time[0] = pygame.time.get_ticks()

				self.speed_cars[self.lane_ob[0] - 1] = -1

			if pygame.time.get_ticks() - self.time[0] >= 100:
				self.speed_cars[self.lane_ob[0] - 1] = self.speed_cars_temp[self.lane_ob[0] - 1]

		# ob 2
		if self.flag_ob[1]:
			if abs(self.pos_ob[1] - self.cars[self.lane_ob[1] - 1][0] - self.width_car) <= 5:
				self.time[1] = pygame.time.get_ticks()

				self.speed_cars[self.lane_ob[1] - 1] = -1

			if pygame.time.get_ticks() - self.time[1] >= 100:
				self.speed_cars[self.lane_ob[1] - 1] = self.speed_cars_temp[self.lane_ob[1] - 1]

		# start
		flag  = False
		for i in range (5):
			if self.cars[i][0] >=self.finish_line:
				flag = True
		if flag:
			self.start_ob = False


class Point(DeadlineRunnersScene):
	def __init__(self, game, title, speed_cars, cars):
		DeadlineRunnersScene.__init__(self, game, title)
		self.speed_cars = speed_cars
		self.cars = cars
		self.width_car = 100
		self.finish_line = self.game.W - 150
		self.y_po = self.game.H / 6
		self.width_Point = 50
		self.height_Point = 50
		self.time = [0 for i in range (5)]
		self.start_po = True
		self.count_po = [0 for i in range (5)]

		self.Obstacle = Obstacle(self.game, self.title, self.speed_cars, self.cars)
		self.pos_po  = self.Obstacle.range_ob()[0]
		self.lane_po = self.Obstacle.range_ob()[1]

	def draw_po (self):
		if self.start_po:
			self.move_po()
			pygame.draw.rect(self.game.window, (255, 215, 0), (self.pos_po, self.y_po * self.lane_po, self.width_Point, self.height_Point))


	def Speed_po(self):
		self.speed_po = 1.5


	def move_po(self):
		self.Speed_po()
		self.pos_po -= self.speed_po

		if self.pos_po <= 0:
			self.pos_po  = self.Obstacle.range_ob()[0]
			self.lane_po = self.Obstacle.range_ob()[1]

		flag  = False
		for i in range (5):
			if self.cars[i][0] >= self.finish_line and self.pos_po < self.cars[i][0]:
				flag = True
		if flag:
			self.start_po = False

		if abs(self.pos_po - self.cars[self.lane_po - 1][0] - self.width_car) <= 5:
			self.count_po[self.lane_po - 1] = 1
		# print(self.count_po)

		return self.count_po




class Skill(DeadlineRunnersScene):
	def __init__(self, game, title, speed_cars, cars, count_po):
		DeadlineRunnersScene.__init__(self, game, title)
		self.speed_cars = speed_cars
		self.speed_cars_temp = speed_cars[:]
		self.cars = cars
		self.count_po = count_po
		self.finish_line = self.game.W - 150
		self.Obstacle = Obstacle(self.game, self.title, self.speed_cars, self.cars)
		self.Car = Car(self.game, self.title)
		self.lane_ob =  self.Obstacle.range_ob()[2]

		self.nv = 0

		self.flag = False
		self.flag_skill = True

		self.time_skill = [0 for i in range(5)]
		self.rand_skill = randrange (0, 2)


	def range_skill(self):
		self.lane_ob =  self.Obstacle.range_ob()[2]

		for i in range (5):
			if self.count_po[i] == 1:
				self.flag = True
				self.nv = i
				self.count_po[self.nv] = 0

		if self.flag:
			self.skill_6()


	# tat ca cham tru ban than
	def skill_1 (self):
		if self.flag_skill:
			for i in range(5):
				if i != self.nv:
					self.speed_cars[i] = -1
					self.time_skill[0] = pygame.time.get_ticks()
					self.flag_skill = False

		if pygame.time.get_ticks() - self.time_skill[0] >= 500:
			for i in range(5):
				self.speed_cars[i] = self.speed_cars_temp[i]
			self.nv = 0
			self.flag = False
			self.flag_skill = True


	# Tang toc ban than
	def skill_2(self):
		if self.flag_skill:
			for i in range(5):
				if i == self.nv:
					self.speed_cars[i] *= 2
					self.time_skill[1] = pygame.time.get_ticks()
					self.flag_skill = False

		if pygame.time.get_ticks() - self.time_skill[1] >= 500:
			for i in range(5):
				self.speed_cars[i] = self.speed_cars_temp[i]
			self.nv = 0
			self.flag = False
			self.flag_skill = True


	# tranh hieu ung !loi
	def skill_3 (self):
		if self.flag_skill:
			if self.nv == self.lane_ob[0]:
					self.Obstacle.flag_ob[0] = False
					self.time_skill[2] = pygame.time.get_ticks()
					self.flag_skill = False

			elif self.nv == self.lane_ob[1]:
				self.Obstacle.flag_ob[1] = False
				self.time_skill[2] = pygame.time.get_ticks()
				self.flag_skill = False

		if pygame.time.get_ticks() - self.time_skill[2] >= 500:
			self.Obstacle.flag_ob[0] = True
			self.Obstacle.flag_ob[1] = True
			self.nv = 0
			self.flag = False
			self.flag_skill = True


# Teleport
	def skill_4(self):
		if self.flag_skill:
				self.cars[self.nv][0] += 100
				self.time_skill[1] = pygame.time.get_ticks()
				self.flag_skill = False

		if pygame.time.get_ticks() - self.time_skill[1] >= 10:
			self.nv = 0
			self.flag = False
			self.flag_skill = True

# tia chop
	def skill_5 (self):
		if self.flag_skill:
			for i in range(5):
				if i != self.nv:
					self.speed_cars[i] = 0
					self.time_skill[0] = pygame.time.get_ticks()
					self.flag_skill = False

		if pygame.time.get_ticks() - self.time_skill[0] >= 1000:
			for i in range(5):
				self.speed_cars[i] = self.speed_cars_temp[i]
			self.nv = 0
			self.flag = False
			self.flag_skill = True

# choang bat ki
	def skill_6 (self):
		if self.flag_skill:
			while True:
				rand_nv = randrange(0, 4)
				if rand_nv != self.nv:
					break

			self.speed_cars[rand_nv] = -1
			self.time_skill[0] = pygame.time.get_ticks()
			self.flag_skill = False

		if pygame.time.get_ticks() - self.time_skill[0] >= 500:
			for i in range(5):
				self.speed_cars[i] = self.speed_cars_temp[i]
			self.nv = 0
			self.flag = False
			self.flag_skill = True
