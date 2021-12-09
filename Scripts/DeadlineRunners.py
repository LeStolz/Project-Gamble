import pygame
from random import *
import heapq
from Scenes import *
from Classes import *


class DeadlineRunnersGameScene(GameScene):
	class Object:
		def __init__(self, menu, x, y, w, h, image, vel):
			self.menu = menu

			self.x = x
			self.y = y

			self.vel = vel
			self.desired_vel = vel

			self.image = Surface(image)
			self.image.position(x, y)
			self.image.resize(w, h)


		def draw(self):
			self.menu.game.draw_surface(self.image)


		def update(self):
			self.x += self.vel
			self.vel += (self.desired_vel - self.vel) / self.menu.game.FPS

			self.image.rect.x = self.x


	class Background:
		def __init__(self, menu):
			self.menu = menu

			self.background = [
				self.menu.Object(
					self.menu, 0, 0, self.menu.game.W, self.menu.game.H,
					self.menu.game.deadline_runners_assets['Background'].image, -6
				),
				self.menu.Object(
					self.menu, self.menu.game.W, 0, self.menu.game.W, self.menu.game.H,
					self.menu.game.deadline_runners_assets['Background'].image, -6
				),
			]

			self.active = False
			self.finish_line = self.menu.Object(
				self.menu, self.menu.game.W, 0, 25, self.menu.game.H, self.menu.game.deadline_runners_assets['FinishLine'].image, 0
			)


		def draw(self):
			for v in self.background:
				v.draw()

			if self.active:
				self.finish_line.draw()


		def update(self):
			if self.background[1].x <= 0:
				for i, v in enumerate(self.background):
					v.x = i * self.menu.game.W

			for v in self.background:
				v.update()

			if self.active:
				for v in self.background:
					v.desired_vel = 0

				self.finish_line.vel = self.background[1].vel
				self.finish_line.desired_vel = 0
				self.finish_line.update()


	class Obstacle(Object):
		def __init__(self, menu, x, y, w, h, image, vel, relative_vel):
			super().__init__(menu, x, y, w, h, image, vel)

			self.active = False
			self.relative_vel = relative_vel


		def update(self):
			if self.active:
				super().update()

				self.vel = self.menu.background.background[0].vel + self.relative_vel

				for v in self.menu.cars:
					if self.image.rect.colliderect(v.image.rect) and not self.menu.background.active:
						v.vel = -1
						break

				if self.x < -self.image.rect.w:
					self.active = False


	class Point(Object):
		def __init__(self, menu, x, y, w, h, image, vel):
			super().__init__(menu, x, y, w, h, image, vel)

			self.active = False


		def update(self):
			if self.active:
				super().update()

				self.vel = self.menu.background.background[0].vel

				for v in self.menu.cars:
					if self.image.rect.colliderect(v.image.rect) and not self.menu.background.active:
						pass
						self.active = False
						self.x = self.menu.game.W
						super().update()
						break

				if self.x < -self.image.rect.w:
					self.active = False


	class Car(Object):
		def __init__(self, menu, x, y, w, h, image, vel):
			super().__init__(menu, x, y, w, h, image, vel)


		def accelerate(self, desired_vel):
			self.desired_vel = desired_vel


		def update(self):
			super().update()

			if self.x >= self.menu.background.finish_line.x - 2 * self.image.rect.w:
				self.desired_vel = 0


	class Event:
		def __init__(self, time, method, arguments):
			self.time = time
			self.method = method
			self.arguments = arguments


		def __lt__(self, next):
			return self.time < next.time


	def __init__(self, game, title):
		GameScene.__init__(self, game, title)

		self.CHARACTERS = {
			'Deadliners' : [
				self.Car(self, 0, self.game.H * 1 // 6, 100, 50, self.game.deadline_runners_assets['Character'].image, random.randint(0, 1)),
				self.Car(self, 0, self.game.H * 2 // 6, 100, 50, self.game.deadline_runners_assets['Character'].image, random.randint(0, 1)),
				self.Car(self, 0, self.game.H * 3 // 6, 100, 50, self.game.deadline_runners_assets['Character'].image, random.randint(0, 1)),
				self.Car(self, 0, self.game.H * 4 // 6, 100, 50, self.game.deadline_runners_assets['Character'].image, random.randint(0, 1)),
				self.Car(self, 0, self.game.H * 5 // 6, 100, 50, self.game.deadline_runners_assets['Character'].image, random.randint(0, 1)),
			],
			'Chivalry' : [

			],
			'Aquatica' : [

			],
		}

		self.background = self.Background(self)
		self.cars = self.CHARACTERS['Deadliners'][:]
		self.obstacles = [
			self.Obstacle(
				self, self.game.W, self.cars[x].image.rect.y, self.cars[x].image.rect.w, self.cars[x].image.rect.h,
				self.game.deadline_runners_assets['Obstacle'].image, 0, 0
			) for x in range(0, len(self.cars))
		]
		self.obstacles.extend([
			self.Obstacle(
				self, self.game.W, self.cars[x].image.rect.y, self.cars[x].image.rect.w, self.cars[x].image.rect.h,
				self.game.deadline_runners_assets['Obstacle'].image, 0, self.background.background[0].vel
			) for x in range(0, len(self.cars))
		])
		self.points = [
			self.Point(
				self, self.game.W, self.cars[x].image.rect.y, self.cars[x].image.rect.w, self.cars[x].image.rect.h,
				self.game.deadline_runners_assets['Point'].image, 0
			) for x in range(0, len(self.cars))
		]

		self.event_queue = []
		heapq.heapify(self.event_queue)

		self.accelerate_cars()


	def accelerate_cars(self):
		min_x = self.cars[0].x
		max_x = self.cars[0].x

		for v in self.cars:
			min_x = min(min_x, v.x)
			max_x = max(max_x, v.x)

		if max_x > self.game.W - 4 * self.cars[0].image.rect.w:
			self.background.active = True

			for v in self.cars:
				v.desired_vel -= self.background.background[1].vel
		else:
			heapq.heappush(self.event_queue, self.Event(pygame.time.get_ticks() + 6000, self.accelerate_cars, ()))

		for v in self.cars:
			bias = 1
			bias = bias + 1 if v.x <= min_x else bias
			bias = bias - 1 if v.x >= max_x else bias

			heapq.heappush(self.event_queue, self.Event(pygame.time.get_ticks() + 2000, v.accelerate, (random.random() + bias,)))
			heapq.heappush(self.event_queue, self.Event(pygame.time.get_ticks() + 4000, v.accelerate, (0,)))


	def process_event_queue(self):
		while len(self.event_queue) > 0 and self.event_queue[0].time <= pygame.time.get_ticks():
			self.event_queue[0].method(*(self.event_queue[0].arguments))
			heapq.heappop(self.event_queue)


	def process_obstacle(self):
		for v in self.obstacles:
			if not v.active and randint(0, 750) == 0:
				v.x = self.game.W
				v.active = True


	def process_point(self):
		for v in self.points:
			if not v.active and randint(0, 750) == 0:
				v.x = self.game.W
				v.active = True


	def draw_options(self):
		if not self.background.active:
			self.process_event_queue()
			self.process_obstacle()
			self.process_point()

		self.background.draw()

		for v in self.obstacles:
			v.draw()

		for v in self.points:
			v.draw()

		for v in self.cars:
			v.draw()

		if self.lives <= 0:
			self.reset_game()
			return

		self.background.update()

		for v in self.obstacles:
			v.update()

		for v in self.points:
			v.update()

		for v in self.cars:
			v.update()