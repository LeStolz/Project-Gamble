from math import e
from os import X_OK, supports_effective_ids
from warnings import catch_warnings
import pygame
from copy import copy
from random import randint

from pygame.transform import average_color
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


class MainGameScene(Scene):
	def __init__(self, game, parent, title):
		Scene.__init__(self, game, parent, title)

		self.direction = Vector()

		self.width_car = 100
		self.height_car = 50
		self.finish_line = self.game.DISPLAY_W - 150
		self.cars = [[0, self.game.DISPLAY_H / 6 * x] for x in range(1,6)]
		self.click = 0
	

	def draw_scene(self):
		self.running = True

		self.speed = Car.speed_car(self)

		ob = Obstacle(self.game, self.parent, self.title, self.cars, self.speed)
		ob.range_Obstacle()

		bg = Background(self.game, self.parent, self.title, self.speed, self.cars)
		po = Point(self.game, self.parent, self.title, self.cars, self.speed)
		po.range_point()
		
		
		while self.running:	
			self.check_input()
			self.mode_speed()

			self.game.display.fill(self.game.BLACK)
			self.game.window.blit(self.game.display, (0, 0))

			bg.move()
			bg.draw()

			for x in range (5):
				Car.draw_car(self, x)

			ob.draw_Obstacle()
			po.draw_point()

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


class Car(MainGameScene):
	def draw_car(self, n):
		Car.pos_car(self, n)

		bg = Background(self.game, self.parent, self.title, self.speed, self.cars)

		pygame.draw.rect(self.game.window, self.game.GREEN, (self.cars[n][0] + bg.move(), self.cars[n][1], self.width_car, self.height_car))


	def speed_car(self):
		self.speed_temp = [7, 7.5, 8, 9, 10]

		shuffle(self.speed_temp)

		self.speed = self.speed_temp[:]

		return self.speed


	def pos_car(self, n):
		if self.cars[n][0] < 2000 - self.width_car - 50:
			self.cars[n][0] += self.speed[n]

		flag = 0
		for i in range (5):
			if self.cars[i][0] >= 2000 - self.width_car -50:
				flag += 1
			if flag == 5:
				for x in range (5):
					self.cars[x][0] = 0
					self.running = False

					Car.speed_car(self)

					self.click = 0


class Background(MainGameScene):
	def __init__(self, game, parent, title, speed, cars):
		super().__init__(game, parent, title)
		self.speed = speed
		self.cars = cars

		self.pos_bg = 0
		self.speed_bg = 0
		self.BG = pygame.image.load(r'C:\\D\\Source_Code_FIT\\Project-Gamble\\Scripts\\Background.png')
		self.BG = pygame.transform.scale(self.BG, (2000, 720))
		self.width_bg = self.BG.get_width()
		self.temp = 0
		self.car = Car(self.game, self.parent, self.title)
		self.temp_pos_bg = 0
		
	

	def draw(self):
		self.game.window.blit(self.BG, (self.temp_pos_bg, 0))
	

	def move(self):
		temp_car = max(self.cars[0][0], self.cars[1][0], self.cars[2][0], self.cars[3][0], self.cars[4][0])
		x_camera = temp_car - (self.game.DISPLAY_W / 2 - self.width_car / 2)

		if x_camera < 0:
			x_camera = 0
		if x_camera + self.game.DISPLAY_W > self.width_bg:
			x_camera = self.width_bg - self.game.DISPLAY_W
		
		self.temp_pos_bg = self.pos_bg
		self.temp_pos_bg -= x_camera
		return self.temp_pos_bg 
		

class Obstacle(MainGameScene):
	def __init__(self, game, parent, title, Cars, speed):
		super().__init__(game, parent, title)
		self.cars = Cars
		self.speed = speed

		self.Ob = [[self.game.DISPLAY_W, self.game.DISPLAY_H / 6 * x] for x in range(1,6)]
		self.width_Obstacle = 50
		self.height_Obstacle = 50
		self.speed_temp_ob = [0, 0]

		self.rand = [0, 0]
		self.start = [1, 1]
		self.flag = [1, 1]
		self.count = [0, 0]
		self.flag_Ob = False


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
				self.Ob[self.rand[0]][0] = self.game.DISPLAY_W
				self.flag[1] = 0
				self.flag[0] = 1
				self.count[0] += 1
				self.range_Obstacle()

		if self.start[1] == 1:		
			self.Ob[self.rand[1]][0] -= self.speed_Ob

			if self.Ob[self.rand[1]][0] < 0:
				self.Ob[self.rand[1]][0] = self.game.DISPLAY_W
				self.flag[0] = 0
				self.flag[1] = 1
				self.count[1] += 1
				self.range_Obstacle()			


	def check(self):
		if self.flag_Ob:
			if self.start[0] == 1:
				if abs(self.Ob[self.rand[0]][0] - (self.cars[self.rand[0]][0] + self.width_car)) <=  10:
					self.speed[self.rand[0]] = -5
				else:
					self.speed[self.rand[0]] = self.speed_temp_ob[0]

				if self.cars[0][0] >= self.finish_line or self.cars[1][0] >= self.finish_line or self.cars[2][0] >= self.finish_line or self.cars[3][0] >= self.finish_line or self.cars[4][0] >= self.finish_line:
					self.start[0] = 0
					self.speed[self.rand[0]] = self.speed_temp_ob[0]

			if self.start[1] == 1:
				if abs(self.Ob[self.rand[1]][0] - (self.cars[self.rand[1]][0] + self.width_car)) <=  10:
					self.speed[self.rand[1]] = -5
				else:
					self.speed[self.rand[1]] = self.speed_temp_ob[1]

				if self.cars[0][0] >= self.finish_line or self.cars[1][0] >= self.finish_line or self.cars[2][0] >= self.finish_line or self.cars[3][0] >= self.finish_line or self.cars[4][0] >= self.finish_line:
					self.start[1] = 0
					self.speed[self.rand[1]] = self.speed_temp_ob[1]
			

class Point(MainGameScene):
	def __init__(self, game, parent, title, cars, speed):
		super().__init__(game, parent, title)
		self.cars = cars
		self.speed = speed

		self.po = [[self.game.DISPLAY_W, self.game.DISPLAY_H / 6 * x] for x in range(1,6)]
		self.width_point = 50
		self.height_point = 50
		self.speed_temp_po = [0, 0]
		self.rand = [0, 0]
		self.count_point = [0, 0, 0, 0, 0]
		self.flag = 1
	

	def range_point(self):
		self.rand_temp = [0, 1, 2, 3, 4]
		shuffle(self.rand_temp)

		self.rand[0] = self.rand_temp[0]
		self.speed_temp_po[0] = self.speed[self.rand[0]]


	def draw_point(self):
		Point.speed(self)
		Point.move(self)
		Point.check(self)

		pygame.draw.rect(self.game.window, (255, 215, 0), (self.po[self.rand[0]][0], self.po[self.rand[0]][1], self.width_point, self.height_point))


	def speed(self):
		self.speed_po = 10
	
	def move(self):
		self.po[self.rand[0]][0] -= self.speed_po

		if self.po[self.rand[0]][0] < 0:
			self.po[self.rand[0]][0] = self.game.DISPLAY_W
			self.flag = 1
			self.range_point()


	def check(self):
		if abs(self.po[self.rand[0]][0] - self.cars[self.rand[0]][0] <= 20 and self.flag == 1):
			self.count_point[self.rand[0]] += 1
			self.flag = 0

		return self.range_point


class Skill(MainGameScene):
	def __init__(self, game, parent, title, cars, speed):
		super().__init__(game, parent, title)
		self.speed = speed
		self.speed_temp = speed
		self.cars = cars
		po = Point(self.game, self.parent, self.title, self.cars, self.speed)
		self.count_point = po.check()
		self.nv = 0
		self.flag_skill = False
		
	def quang_Deadline(self):
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
	
		
			 



		