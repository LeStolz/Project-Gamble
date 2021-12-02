from math import e
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
		self.finishLine = self.game.DISPLAY_W - 150
		self.Cars = [[0, self.game.DISPLAY_H / 6 * x] for x in range(1,6)]
		self.click = 0
		self.speed = [0, 0, 0, 0, 0]
	

	def draw_scene(self):
		self.running = True
		self.speed = Car.speed_car(self)

		Ob = Obstacle(self.game, self.parent, self.title, self.Cars, self.speed)
		Ob.range_Obstacle()
		
		while self.running:	
			self.check_input()
			self.mode_speed()

			self.game.display.fill(self.game.BLACK)
			self.game.window.blit(self.game.display, (0, 0))

			Background.move(self)
			Background.draw(self)

			[Car.draw_car(self, x) for x in range (5)]

			Ob.draw_Obstacle()

			pygame.display.update()


	def check_input(self):
		self.game.check_input()


	def mode_speed(self):
		self.game.check_input()

		if (self.game.K_m == True):
			self.game.reset_input()

			if (self.click == 0):
				for x in range (5):
					self.speed[x] *= 2
			else:
				for x in range (5):
					self.speed[x] /= 2

			if (self.click == 0):
				self.click = 1
			else:
				self.click = 0


class Car(MainGameScene):
	def draw_car(self, n):
		Car.pos_car(self, n)

		pygame.draw.rect(self.game.window, self.game.GREEN, (self.Cars[n][0], self.Cars[n][1], self.width_car, self.height_car))
		

	def speed_car(self):
		self.speed_temp = [3, 3.5, 4, 4.5, 5]

		shuffle(self.speed_temp)

		self.speed = self.speed_temp[:]

		return self.speed


	def pos_car(self, n):
		if (self.Cars[n][0] < self.finishLine):
			self.Cars[n][0] += self.speed[n]
			
		if (self.Cars[0][0] >= self.finishLine and self.Cars[1][0] >= self.finishLine and self.Cars[2][0] >= self.finishLine and self.Cars[3][0] >= self.finishLine and self.Cars[4][0] >= self.finishLine):
			for x in range (5):
				self.Cars[x][0] = 0
				self.running = False

			Car.speed_car(self)

			self.click = 0


class Background(MainGameScene):
	pos_bg = 0
	speed_bg = 0


	def draw(self):
		BG = pygame.image.load('Background.png')

		BG = pygame.transform.scale(BG, (2800, 720))

		self.game.window.blit(BG, (self.pos_bg, 0))
	

	def move(self):
		self.pos_bg = Background.pos_bg
		Background.pos_bg -= Background.speed_bg

		if (self.Cars[0][0] >= self.finishLine or self.Cars[1][0] >= self.finishLine or self.Cars[2][0] >= self.finishLine or self.Cars[3][0] >= self.finishLine or self.Cars[4][0] >= self.finishLine):
			self.temp = Background.speed_bg
			Background.speed_bg = 0

			
		else:
			Background.speed_bg = max(self.speed)

		if (self.Cars[0][0] <= 10 and self.Cars[1][0] <= 10 and self.Cars[2][0] <= 10 and self.Cars[3][0] <= 10 and self.Cars[4][0] <= 10):
			Background.pos_bg = 0
			self.pos_bg = 0
			
		
		if (Background.speed_bg == 0):
			for x in range(5):
				self.speed[x] += self.temp


class Obstacle(MainGameScene):
	def __init__(self, game, parent, title, Cars, speed):
		super().__init__(game, parent, title)
		self.Cars = Cars
		self.speed = speed

		self.Ob = [[self.game.DISPLAY_W, self.game.DISPLAY_H / 6 * x] for x in range(1,6)]
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

		if (self.flag[0]):
			self.rand[0] = self.rand_temp[0]
			self.Ob[self.rand[0]][0] += 200
		if (self.flag[1]):
			self.rand[1] =  self.rand_temp[1]

		self.speed_temp_ob[0] = self.speed[self.rand[0]]
		self.speed_temp_ob[1] = self.speed[self.rand[1]]

		
	def draw_Obstacle(self):
		if (self.count[0] == 2):
			self.start[0] = 0
		if (self.count[1] == 2):
			self.start[1] = 0

		Obstacle.speed(self)
		Obstacle.move(self)
		Obstacle.check(self)

		if (self.start[0] == 1):
			pygame.draw.rect(self.game.window, self.game.RED, (self.Ob[self.rand[0]][0], self.Ob[self.rand[0]][1], self.width_Obstacle, self.height_Obstacle))

		if (self.start[1] == 1):
			pygame.draw.rect(self.game.window, self.game.RED, (self.Ob[self.rand[1]][0], self.Ob[self.rand[1]][1], self.width_Obstacle, self.height_Obstacle))
	

	def speed(self):
		self.speed_Ob = 10


	def move(self):
		if (self.start[0] == 1):
			self.Ob[self.rand[0]][0] -= self.speed_Ob

			if (self.Ob[self.rand[0]][0] < 0):
				self.Ob[self.rand[0]][0] = self.game.DISPLAY_W
				self.flag[1] = 0
				self.flag[0] = 1
				self.count[0] += 1
				self.range_Obstacle()

		if (self.start[1] == 1):		
			self.Ob[self.rand[1]][0] -= self.speed_Ob

			if (self.Ob[self.rand[1]][0] < 0):
				self.Ob[self.rand[1]][0] = self.game.DISPLAY_W
				self.flag[0] = 0
				self.flag[1] = 1
				self.count[1] += 1
				self.range_Obstacle()			


	def check(self):
		if (self.start[0] == 1):
			if ((self.Ob[self.rand[0]][0] - (self.Cars[self.rand[0]][0] + self.width_car)) <=  20 and (self.Ob[self.rand[0]][0] - (self.Cars[self.rand[0]][0] + self.width_car)) >= -50):
				self.speed[self.rand[0]] = -4
			else:
				self.speed[self.rand[0]] = self.speed_temp_ob[0]

			if (self.Cars[0][0] >= self.finishLine or self.Cars[1][0] >= self.finishLine or self.Cars[2][0] >= self.finishLine or self.Cars[3][0] >= self.finishLine or self.Cars[4][0] >= self.finishLine):
				self.start[0] = 0
				self.speed[self.rand[0]] = self.speed_temp_ob[0]

		if (self.start[1] == 1):
			if ((self.Ob[self.rand[1]][0] - (self.Cars[self.rand[1]][0] + self.width_car)) <=  20 and (self.Ob[self.rand[1]][0] - (self.Cars[self.rand[1]][0] + self.width_car)) >= -50):
				self.speed[self.rand[1]] = -4
			else:
				self.speed[self.rand[1]] = self.speed_temp_ob[1]

			if (self.Cars[0][0] >= self.finishLine or self.Cars[1][0] >= self.finishLine or self.Cars[2][0] >= self.finishLine or self.Cars[3][0] >= self.finishLine or self.Cars[4][0] >= self.finishLine):
				self.start[1] = 0
				self.speed[self.rand[1]] = self.speed_temp_ob[1]
		
			 



		