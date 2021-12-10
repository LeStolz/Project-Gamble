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
					self.menu.game.deadline_runners_assets[self.menu.character_set].image, -6
				),
				self.menu.Object(
					self.menu, self.menu.game.W, 0, self.menu.game.W, self.menu.game.H,
					self.menu.game.deadline_runners_assets[self.menu.character_set].image, -6
				),
			]
			self.background[1].image.image = pygame.transform.flip(self.background[1].image.image, True, False)

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
				self.background[0].x = self.menu.game.W
				self.background[0], self.background[1] = self.background[1], self.background[0]

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
						if self.relative_vel == 0:
							v.vel = 0
						else:
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
						v.skills[v.skill_method_name](*v.skill_arguments)
						self.active = False
						self.x = self.menu.game.W
						super().update()
						break

				if self.x < -self.image.rect.w:
					self.active = False


	class Skill:
		def __init__(self, menu, car):
			self.menu = menu
			self.car = car

			self.skills = {
				'disappear' : self.disappear,
			}


		def disappear(self, active):
			if self.car.active != active:
				self.car.active = active
				heapq.heappush(self.menu.event_queue, self.menu.Event(pygame.time.get_ticks() + 4000, self.disappear, (True,)))


	class Car(Object, Skill):
		def __init__(self, menu, x, y, w, h, title, vel, skill_method_name, skill_arguments, bet):
			menu.Object.__init__(self, menu, x, y, w, h, menu.game.deadline_runners_assets[title].image, vel)
			menu.Skill.__init__(self, menu, self)

			self.title = title
			self.skill_method_name = skill_method_name
			self.skill_arguments = skill_arguments
			self.bet = bet

			self.active = True
			self.finish_place = -1


		def accelerate(self, desired_vel):
			self.desired_vel = desired_vel


		def update(self):
			super().update()

			self.x = min(self.x, self.menu.game.W - self.image.rect.w)

			if self.finish_place == -1:
				if self.x >= self.menu.background.finish_line.x - 2 * self.image.rect.w:
					self.desired_vel = 0.5

				if self.x >= self.menu.background.finish_line.x:
					self.menu.cars_finished.append(self)
					self.finish_place = len(self.menu.cars_finished)
					if self.finish_place <= 3:
						self.menu.score += self.bet * 2 // (2 ** (self.finish_place - 1))
						self.menu.game.ACCOUNT['Races'][0] = \
							'At ' \
							+ str((datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")) \
							+ (' Earned ' if self.menu.score >= 0 else ' Lost ') \
							+ str(abs(self.menu.score))
			else:
				self.desired_vel = 0
				if self.finish_place == 1:
					self.menu.game.draw_text(
						f'Earned {self.bet * 2}    1st', 35, self.menu.game.GREEN if self.bet > 0 else self.menu.game.RED,
						self.x - 20, self.image.rect.centery, right=True
					)
				if self.finish_place == 2:
					self.menu.game.draw_text(
						f'Earned {self.bet}    2nd', 35, self.menu.game.GREEN if self.bet > 0 else self.menu.game.RED,
						self.x - 20, self.image.rect.centery, right=True
					)
				if self.finish_place == 3:
					self.menu.game.draw_text(
						f'Earned {self.bet // 2}    3rd', 35, self.menu.game.GREEN if self.bet > 0 else self.menu.game.RED,
						self.x - 20, self.image.rect.centery, right=True
					)
				if self.finish_place == 4:
					self.menu.game.draw_text(
						f'Earned {0}    4th', 35, self.menu.game.RED, self.x - 20, self.image.rect.centery, right=True
					)
				if self.finish_place == 5:
					self.menu.game.draw_text(
						f'Earned {0}    5th', 35, self.menu.game.RED, self.x - 20, self.image.rect.centery, right=True
					)


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
				self.Car(self, 25, self.game.H * 1 // 6, 150, 150,
					'Dang', random.randint(0, 1),
					'disappear', (False,), 0
				),
				self.Car(self, 25, self.game.H * 2 // 6, 150, 150,
					'Khanh', random.randint(0, 1),
					'disappear', (False,), 0
				),
				self.Car(self, 25, self.game.H * 3 // 6, 150, 150,
					'Triet', random.randint(0, 1),
					'disappear', (False,), 0
				),
				self.Car(self, 25, self.game.H * 0.715, 150, 150,
					'Hoang', random.randint(0, 1),
					'disappear', (False,), 0
				),
				self.Car(self, 25, self.game.H * 0.84, 150, 150,
					'Dat', random.randint(0, 1),
					'disappear', (False,), 0
				),
			],
			'Chivalry' : [
				self.Car(self, 25, self.game.H * 1 // 6, 150, 150,
					'Alchemist', random.randint(0, 1),
					'disappear', (False,), 0
				),
				self.Car(self, 25, self.game.H * 2 // 6, 150, 150,
					'Archer', random.randint(0, 1),
					'disappear', (False,), 0
				),
				self.Car(self, 25, self.game.H * 3 // 6, 150, 150,
					'Knight', random.randint(0, 1),
					'disappear', (False,), 0
				),
				self.Car(self, 25, self.game.H * 4 // 6, 150, 150,
					'Thief', random.randint(0, 1),
					'disappear', (False,), 0
				),
				self.Car(self, 25, self.game.H * 0.85, 150, 150,
					'Warrior', random.randint(0, 1),
					'disappear', (False,), 0
				),
			],
			'Aquatica' : [
				self.Car(self, 25, self.game.H * 1 // 6, 150, 150,
					'Pufferfish', random.randint(0, 1),
					'disappear', (False,), 0
				),
				self.Car(self, 25, self.game.H * 2 // 6, 150, 150,
					'Electriceel', random.randint(0, 1),
					'disappear', (False,), 0
				),
				self.Car(self, 25, self.game.H * 3 // 6, 150, 150,
					'Squid', random.randint(0, 1),
					'disappear', (False,), 0
				),
				self.Car(self, 25, self.game.H * 4 // 6, 150, 150,
					'Starfish', random.randint(0, 1),
					'disappear', (False,), 0
				),
				self.Car(self, 25, self.game.H * 0.85, 150, 150,
					'Jellyfish', random.randint(0, 1),
					'disappear', (False,), 0
				),
			],
		}

		self.qualities = {
			'Character set' : ['Chivalry', 'Deadliners', 'Aquatica'],
			'Track length' : ['Short', 'Medium', 'Long'],
		}

		self.character_set = self.qualities['Character set'][self.game.ACCOUNT['Character set']]
		self.track_length = self.qualities['Track length'][self.game.ACCOUNT['Track length']]

		self.background = self.Background(self)
		self.cars = self.CHARACTERS[self.character_set][:]
		self.cars_finished = []
		self.max_w = self.cars[0].image.rect.w
		self.max_text_w = 0

		for v in self.cars:
			self.max_w = max(self.max_w, v.image.rect.w)
			self.max_text_w = max(self.max_text_w, self.game.draw_text(
				v.title, 35, self.game.WHITE, v.x + self.max_w + 25, v.y, centerx=False, centery=False
			).w)

		for i, v in enumerate(self.cars):
			self.buttons[str(i) + 'Left'] \
				= Button(Surface(self.buttons_assets['ArrowBottom'].image), Surface(self.buttons_assets['ArrowLeft'].image))
			self.buttons[str(i) + 'Right'] \
				= Button(Surface(self.buttons_assets['ArrowBottom'].image), Surface(self.buttons_assets['ArrowRight'].image))

			self.buttons[str(i) + 'Left'].position(v.x + self.max_w + 25 + self.max_text_w + 15, v.y + v.image.rect.h // 2 - 40)
			self.buttons[str(i) + 'Right'].position(v.x + self.max_w + 25 + self.max_text_w + 300, v.y + v.image.rect.h // 2 - 40)

		self.buttons['Start Race'] = Button(
			Surface(self.buttons_assets['Bottom'].image), Surface(self.buttons_assets['DeadlineRunners'].image)
		)

		self.buttons['Start Race'].resize(self.game.W // 5, self.game.H // 6)
		self.buttons['Start Race'].position(self.game.W - 250 - self.game.W // 10, self.game.H // 2 - self.game.H // 12 + 20)

		self.obstacles = [
			self.Obstacle(
				self,
				self.game.W, self.cars[x].image.rect.y + self.cars[x].image.rect.h // 2 - self.cars[x].image.rect.h // 4,
				self.cars[x].image.rect.w, self.cars[x].image.rect.h // 2,
				self.game.deadline_runners_assets['Obstacle'].image, 0, 0
			) for x in range(0, len(self.cars))
		]
		self.obstacles.extend([
			self.Obstacle(
				self,
				self.game.W, self.cars[x].image.rect.y + self.cars[x].image.rect.h // 2 - self.cars[x].image.rect.h // 4,
				self.cars[x].image.rect.w, self.cars[x].image.rect.h // 2,
				self.game.deadline_runners_assets['Obstacle'].image, 0, self.background.background[0].vel
			) for x in range(0, len(self.cars))
		])
		self.points = [
			self.Point(
				self,
				self.game.W, self.cars[x].image.rect.y + self.cars[x].image.rect.h // 2 - self.cars[x].image.rect.h // 4,
				self.cars[x].image.rect.w, self.cars[x].image.rect.h // 2,
				self.game.deadline_runners_assets['Point'].image, 0
			) for x in range(0, len(self.cars))
		]

		self.event_queue = []
		heapq.heapify(self.event_queue)

		self.background.draw()
		self.starting = True
		self.finished = False
		self.temp_money = self.game.ACCOUNT["Money"]


	def start_gamble(self):
		self.game.draw_text('Place your bets', 45, self.game.GREEN, self.game.W // 2, 0, centery=False)
		self.game.draw_text('Start Race', 35, self.game.WHITE, self.game.W - 250, self.game.H // 2 - self.game.H // 12 - 30, centery=False)
		self.game.draw_text(
			f'Your money {self.temp_money}', 25, self.game.WHITE,
			self.cars[0].x + self.max_w + 25 + self.max_text_w + 205, self.cars[0].y - 25
		)

		for v in self.cars:
			self.game.draw_text(
				v.title, 35, self.game.WHITE, v.x + self.max_w + 25, v.y + v.image.rect.h // 2, centerx=False
			)
			self.game.draw_text(
				str(v.bet), 35, self.game.WHITE, v.x + self.max_w + 25 + self.max_text_w + 205, v.y + v.image.rect.h // 2
			)


	def finish_gamble(self):
		self.finished = True
		heapq.heappush(self.event_queue, self.Event(pygame.time.get_ticks() + 6000, self.reset_game, ()))


	def check_button_input(self):
		super().check_button_input()

		if self.down_button_name in self.buttons.keys() and self.game.M_DOWN:
			true_down_button_name = self.down_button_name.replace('Left', '').replace('Right', '')

			if self.down_button_name == 'Start Race':
				self.score = self.temp_money - self.game.ACCOUNT["Money"]
				self.starting = False
				self.buttons = {
					'Back' : Button(Surface(self.buttons_assets['ArrowBottom'].image), Surface(self.buttons_assets['ArrowLeft'].image))
				}
				self.buttons['Back'].resize(55, 55)
				self.buttons['Back'].position(0, 0)
				self.accelerate_cars()

				self.game.ACCOUNT['Race Number'] += 1
				self.game.ACCOUNT['Races'].insert(
					0, 'At ' \
					+ str((datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")) \
					+ (' Earned ' if self.score >= 0 else ' Lost ') \
					+ str(abs(self.score))
				)
				if self.game.ACCOUNT['Race Number'] > 10:
					self.game.ACCOUNT['Race Number'] -= 1
					self.game.ACCOUNT['Races'].pop(-1)
				return

			if 'Left' in self.down_button_name:
				prev_bet = self.cars[int(true_down_button_name)].bet
				self.cars[int(true_down_button_name)].bet = (self.cars[int(true_down_button_name)].bet - 2000) % 22000
				if self.temp_money + prev_bet - self.cars[int(true_down_button_name)].bet >= 0:
					self.temp_money += prev_bet - self.cars[int(true_down_button_name)].bet
				else:
					self.cars[int(true_down_button_name)].bet = prev_bet
			elif 'Right' in self.down_button_name:
				prev_bet = self.cars[int(true_down_button_name)].bet
				self.cars[int(true_down_button_name)].bet = (self.cars[int(true_down_button_name)].bet + 2000) % 22000
				if self.temp_money + prev_bet - self.cars[int(true_down_button_name)].bet >= 0:
					self.temp_money += prev_bet - self.cars[int(true_down_button_name)].bet
				else:
					self.cars[int(true_down_button_name)].bet = prev_bet


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
			bias = 2
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
			if not self.starting and not v.active and randint(0, 750) == 0:
				v.x = self.game.W
				v.active = True


	def process_point(self):
		for v in self.points:
			if not self.starting and not v.active and randint(0, 750) == 0:
				v.x = self.game.W
				v.active = True


	def draw_options(self):
		self.process_event_queue()
		if not self.background.active and not self.finished:
			self.process_obstacle()
			self.process_point()

		if len(self.cars_finished) == len(self.cars) and not self.finished:
			self.finished = True
			heapq.heappush(self.event_queue, self.Event(pygame.time.get_ticks() + 6000, self.finish_gamble, ()))

		self.background.draw()

		for v in self.obstacles:
			v.draw()

		for v in self.points:
			v.draw()

		for v in self.cars:
			if v.active:
				v.draw()

		if self.lives <= 0:
			self.reset_game()
			return

		if self.starting:
			self.start_gamble()
			self.draw_buttons()
			return

		self.background.update()

		for v in self.obstacles:
			v.update()

		for v in self.points:
			v.update()

		for v in self.cars:
			v.update()

		self.draw_buttons()