import pygame
from copy import copy
from random import randint
from pygame.constants import BIG_ENDIAN

from Classes import Vector
from random import shuffle


class Scene:
	def __init__(self, game, parent, title):
		self.game = game
		self.parent = parent
		self.title = title
		self.running = True


class MenuScene(Scene):
	def __init__(self, game, parent, title, selections):
		Scene.__init__(self, game, parent, title)

		self.selections = selections
		self.selected_index = 0


	def draw_scene(self):
		self.running = True

		while self.running:
			self.check_input()
			self.game.display.fill(self.game.BLACK)

			self.game.draw_text(text=self.title, size=40, y=self.game.DISPLAY_H // 2 - 50)

			for index, selection in enumerate(self.selections):
				self.game.draw_text(text=selection, size=20, y=self.game.DISPLAY_H // 2 + index * 30)

			self.game.draw_text(
				text='>', size=20,
				x=self.game.DISPLAY_W // 2 - 100,
				y=self.game.DISPLAY_H // 2 + self.selected_index * 30
			)

			self.game.window.blit(self.game.display, (0, 0))
			pygame.display.update()

			self.game.reset_input()


	def check_input(self):
		self.game.check_input()

		if self.game.K_UP:
			self.selected_index = (self.selected_index - 1) % len(self.selections)
		if self.game.K_DOWN:
			self.selected_index = (self.selected_index + 1) % len(self.selections)

		selected_name = self.selections[self.selected_index]

		if self.game.K_RIGHT:
			if selected_name == 'Quit':
				self.game.quit()
			elif selected_name == 'Back':
				self.game.current_scene = self.game.scenes[self.parent]
			elif selected_name in self.game.scenes:
				self.game.current_scene = self.game.scenes[selected_name]

			self.running = False
		if self.game.K_LEFT:
			self.game.current_scene = self.game.scenes[self.parent]

			self.running = False


class SnakeGameScene(Scene):
	def __init__(self, game, parent, title):
		Scene.__init__(self, game, parent, title)

		self.SIZE = 20

		self.speed = 1
		self.direction = Vector()

		self.snake_length = 4
		self.snake_rects = [
			self.game.draw_rect(
				x=randint(0 + self.SIZE, self.game.DISPLAY_W - self.SIZE),
				y=randint(0 + self.SIZE, self.game.DISPLAY_H - self.SIZE),
				w=self.SIZE, h=self.SIZE, color=self.game.RED
			)
		]

		self.fruit_rect = self.game.draw_rect(
			x=randint(0 + self.SIZE, self.game.DISPLAY_W - self.SIZE),
			y=randint(0 + self.SIZE, self.game.DISPLAY_H - self.SIZE),
			w=self.SIZE, h=self.SIZE, color=self.game.RED
		)


	def draw_scene(self):
		self.running = True

		while self.running:
			self.check_input()
			self.game.display.fill(self.game.BLACK)

			self.move_snake()
			self.draw_snake()

			self.draw_fruit()

			self.handle_game_over()

			self.game.window.blit(self.game.display, (0, 0))
			pygame.display.update()


	def move_snake(self):
		self.snake_rects.append(copy(self.snake_rects[-1]))
		self.snake_rects[-1].x += self.direction.x * self.speed
		self.snake_rects[-1].y += self.direction.y * self.speed

		self.snake_rects[-1].x = \
			self.snake_rects[-1].x if self.snake_rects[-1].x >= -self.SIZE else self.game.DISPLAY_W + self.SIZE
		self.snake_rects[-1].x = \
			self.snake_rects[-1].x if self.snake_rects[-1].x <= self.game.DISPLAY_W + self.SIZE else -self.SIZE

		self.snake_rects[-1].y = \
			self.snake_rects[-1].y if self.snake_rects[-1].y >= -self.SIZE else self.game.DISPLAY_H + self.SIZE
		self.snake_rects[-1].y = \
			self.snake_rects[-1].y if self.snake_rects[-1].y <= self.game.DISPLAY_H + self.SIZE else -self.SIZE


	def draw_snake(self):
		if len(self.snake_rects) > self.snake_length * self.SIZE:
			self.snake_rects.pop(0)

		for index in range(len(self.snake_rects) - 1, -1, -self.SIZE):
			self.game.draw_rect(color=self.game.GREEN, rect=self.snake_rects[index])


	def draw_fruit(self):
		if self.snake_rects[-1].colliderect(self.fruit_rect):
			self.snake_length += 1

			self.fruit_rect.x = randint(0 + self.SIZE, self.game.DISPLAY_W - self.SIZE)
			self.fruit_rect.y = randint(0 + self.SIZE, self.game.DISPLAY_H - self.SIZE)

		self.game.draw_rect(color=self.game.RED, rect=self.fruit_rect)


	def handle_game_over(self):
		for index in range(len(self.snake_rects) - 1 - self.SIZE, -1, -self.SIZE):
			if self.snake_rects[-1].colliderect(self.snake_rects[index]):
				collision_direction = (Vector(rect=self.snake_rects[index]) - Vector(rect=self.snake_rects[-1])).normalize()

				if collision_direction / self.direction > 0.8:
					self.game.current_scene = self.game.scenes['Game Over']

					self.__init__(self.game, self.parent, self.title)

					self.game.display.fill(self.game.BLACK)
					self.game.reset_input()

					self.running = False

					return


	def check_input(self):
		self.game.check_input()

		if self.game.K_UP or self.game.K_DOWN or self.game.K_RIGHT or self.game.K_LEFT:
			self.direction = Vector()

		if self.game.K_UP:
			self.direction.y -= 1
		if self.game.K_DOWN:
			self.direction.y += 1
		if self.game.K_RIGHT:
			self.direction.x += 1
		if self.game.K_LEFT:
			self.direction.x -= 1

		self.direction.normalize()

# ================================================================================================================

class MainGameScene(Scene):
	def __init__(self, game, parent, title):
		Scene.__init__(self, game, parent, title)
		self.width_window, self.height_window = pygame.display.get_surface().get_size()
		self.finish_line = self.width_window - 150

	def draw_scene(self):
		self.running = True
		
		self.Car = Car(self.game, self.parent, self.title)
		self.speed_cars = self.Car.speed_car()

		self.Background = Background(self.game, self.parent, self.title, self.speed_cars, self.Car.cars)
		self.Obstacle = Obstacle(self.game, self.parent, self.title, self.speed_cars, self.Car.cars)
		self.Obstacle.range_ob()
		self.Point = Point(self.game, self.parent, self.title, self.speed_cars, self.Car.cars)
		self.Point.range_po()
		while self.running:
			self.check_input()

			self.game.display.fill(self.game.BLACK)
			self.game.window.blit(self.game.display, (0, 0))

			self.width_window, self.height_window = pygame.display.get_surface().get_size()
			
			self.Background.draw_bg()

			for n in range (5):
				self.Car.draw_car(n)

			self.Point.draw_po()
			self.Obstacle.draw_ob()
			

			pygame.display.update()
	

	def check_input(self):
		self.game.check_input()

class Car(MainGameScene):
	def __init__(self, game, parent, title):
		super().__init__(game, parent, title)
		self.width_car = 100
		self.height_car = 50
		self.cars = [[0, self.height_window / 6 * x] for x in range(1,6)]
		
	
	def draw_car(self, n):
		Car.pos_car(self, n)
		print(self.speed_cars)
		pygame.draw.rect(self.game.window, self.game.GREEN, (self.cars[n][0], self.cars[n][1], self.width_car, self.height_car))


	def speed_car(self):
		self.speed_temp = [0.2, 0.25, 0.3, 0.25, 0.2]

		shuffle(self.speed_temp)

		self.speed_cars = self.speed_temp[:]

		return self.speed_cars


	def pos_car(self, n):		
		if self.cars[n][0] <= self.finish_line:
			self.cars[n][0] += self.speed_cars[n]

class Background(MainGameScene):
	def __init__(self, game, parent, title,speed_cars, cars):
		super().__init__(game, parent, title)
		self.speed_cars =speed_cars
		self.speed_cars_remove = self.speed_cars[:]
		self.speed_cars_temp = [self.speed_cars[i] + 2 for i in range (5)]
		self.cars = cars
		self.BG = pygame.image.load(r'C:\\D\\Source_Code_FIT\\Project-Gamble\\Scripts\\Background.png')
		self.BG = pygame.transform.scale(self.BG, (10000, 720))
		self.width_bg = self.BG.get_width()
		self.pos_bg = 0

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
			self.speed_cars = self.speed_cars_temp[:]

		self.pos_bg -= self.speed_bg


class Obstacle(MainGameScene):
	def __init__(self, game, parent, title, speed_cars, cars):
		super().__init__(game, parent, title)
		self.speed_cars = speed_cars
		self.cars = cars
		self.y_ob = self.height_window / 6
		self.width_Obstacle = 50
		self.height_Obstacle = 50
		self.time = [0 for i in range (5)]

	def draw_ob (self):
		self.move_ob()
		pygame.draw.rect(self.game.window, self.game.RED, (self.pos_ob[0], self.y_ob * self.lane_ob[0], self.width_Obstacle, self.height_Obstacle))
		pygame.draw.rect(self.game.window, self.game.RED, (self.pos_ob[1], self.y_ob * self.lane_ob[1], self.width_Obstacle, self.height_Obstacle))

	def range_ob (self):
		self.pos_ob_temp = [self.width_window + 50 * i for i in range (1, 6)]
		
		shuffle(self.pos_ob_temp)

		self.pos_ob = self.pos_ob_temp[:]

		self.lane_ob_temp = [1, 2, 3, 4, 5]

		shuffle(self.lane_ob_temp)

		self.lane_ob = self.lane_ob_temp[:]
		self.speed_temp_ob = self.speed_cars
	
	def speed_ob(self):
		self.speed_ob = 1

	def move_ob(self):
		self.pos_ob[0] -= 1.5
		self.pos_ob[1] -= 1.5

		if self.pos_ob[0] <= 0 and self.pos_ob[1] <= 0:
			self.range_ob()

		# if abs(self.pos_ob[0] - self.cars[self.lane_ob[0] - 1][0]) == 0:
		# 	self.time[0] = pygame.time.get_ticks()
		# 	self.speed_cars[self.lane_ob[0] - 1] = -0.5
		# 	self.speed_cars[self.lane_ob[0] - 1] = self.speed_temp_ob[self.lane_ob_temp[0] - 1]
		
		# if pygame.time.get_ticks() - self.time[0] == 300:
		# 	self.speed_cars[self.lane_ob[0] - 1] = self.speed_temp_ob[self.lane_ob[0] - 1]

class Point(MainGameScene):
	def __init__(self, game, parent, title, speed_cars, cars):
		super().__init__(game, parent, title)
		self.speed_cars = speed_cars
		self.cars = cars
		self.y_po = self.height_window / 6
		self.width_Point = 50
		self.height_Point = 50
		self.time = [0 for i in range (5)]

	def draw_po (self):
		self.move_po()
		pygame.draw.rect(self.game.window, (255, 215, 0), (self.pos_po[0], self.y_po * self.lane_po[0], self.width_Point, self.height_Point))

	def range_po (self):
		self.pos_po_temp = [self.width_window + 50 * i for i in range (1, 6)]
		
		shuffle(self.pos_po_temp)

		self.pos_po = self.pos_po_temp[:]

		self.lane_po_temp = [1, 2, 3, 4, 5]

		shuffle(self.lane_po_temp)

		self.lane_po = self.lane_po_temp[:]
		self.speed_temp_po = self.speed_cars
	
	def speed_po(self):
		self.speed_po = 1

	def move_po(self):
		self.pos_po[0] -= 1.5

		if self.pos_po[0] <= 0:
			self.range_po()

class Skill(MainGameScene):
	def __init__(self, game, parent, title, cars, speed):
		super().__init__(game, parent, title)
		self.speed = speed
		self.speed_temp = speed
		self.cars = cars
		self.po = Point(self.game, self.parent, self.title, self.cars, self.speed)
		self.nv = 0
		self.flag_skill = False
		
	def quang_Deadline(self):
		print(self.po.check())
		for i in range (5):
			if self.count_point[i] == 1:
				self.nv = i
				break
		if self.flag_skill:
			for i in range (4):
				if i != self.nv:
					self.speed[i] = 0
					self.count_point[self.nv] = 0
		else:
			for i in range (4):
				self.speed = self.speed_temp[:]
	
	def giam_Deadline(self):
		for i in range (5):
			if self.count_point[i] == 1:
				self.nv = i
				break
		if self.flag_skill:
			self.speed[self.nv] *= 1.2
			self.count_point[self.nv] = 0
		else:
			for i in range (4):
				self.speed = self.speed_temp[:]


	def tranh_hieu_ung(self):
		for i in range (5):
			if self.count_point[i] == 1:
				self.nv = i
				break
		if self.flag_skill:
			if (self.nv == self.rand[0]):
				self.flag_Ob = False
				self.start[0] = 0

			if (self.nv == self.rand[1]):
				self.flag_Ob = False
				self.start[1] = 0
	

	def hang_rao_thuc_an(self):
		pass
	

	def hieu_ung_tu_nguoi_khac(self):
		pass


			










		


