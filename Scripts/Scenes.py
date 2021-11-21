import pygame
from copy import copy
from random import randint
from Classes import Vector
from random import randrange


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
		self.direction = Vector()
		self.car_x1, self.car_x2, self.car_x3, self.car_x4, self.car_x5 = 0, 0, 0, 0, 0

	def draw_scene(self):
		self.running = True
		while self.running:	
			self.check_input()
			self.game.display.fill(self.game.BLACK)
			self.game.window.blit(self.game.display, (0, 0))
			self.draw_car1()
			self.draw_car2()
			self.draw_car3()
			self.draw_car4()
			self.draw_car5()
			pygame.display.update()


	def draw_car1(self):
		self.speed_car()
		self.pos_car()
		carSurface = pygame.Surface((100, 50))
		pygame.draw.polygon(carSurface, self.game.RED, ((15, 0), (65, 0), (85, 15), (100, 15), (100, 40), (0, 40), (0, 15)))
		pygame.draw.circle(carSurface, self.game.GREEN, (15, 40), 10)
		pygame.draw.circle(carSurface, self.game.GREEN, (85, 40), 10)
		self.game.window.blit(carSurface, (self.car_x1, self.game.DISPLAY_H / 6))

	def draw_car2(self):
		self.speed_car()
		self.pos_car()
		carSurface = pygame.Surface((100, 50))
		pygame.draw.polygon(carSurface, self.game.RED, ((15, 0), (65, 0), (85, 15), (100, 15), (100, 40), (0, 40), (0, 15)))
		pygame.draw.circle(carSurface, self.game.GREEN, (15, 40), 10)
		pygame.draw.circle(carSurface, self.game.GREEN, (85, 40), 10)
		self.game.window.blit(carSurface, (self.car_x2, 2* self.game.DISPLAY_H / 6))
	
	def draw_car3(self):
		self.speed_car()
		self.pos_car()
		carSurface = pygame.Surface((100, 50))
		pygame.draw.polygon(carSurface, self.game.RED, ((15, 0), (65, 0), (85, 15), (100, 15), (100, 40), (0, 40), (0, 15)))
		pygame.draw.circle(carSurface, self.game.GREEN, (15, 40), 10)
		pygame.draw.circle(carSurface, self.game.GREEN, (85, 40), 10)
		self.game.window.blit(carSurface, (self.car_x3, 3 * self.game.DISPLAY_H / 6))
	
	def draw_car4(self):
		self.speed_car()
		self.pos_car()
		carSurface = pygame.Surface((100, 50))
		pygame.draw.polygon(carSurface, self.game.RED, ((15, 0), (65, 0), (85, 15), (100, 15), (100, 40), (0, 40), (0, 15)))
		pygame.draw.circle(carSurface, self.game.GREEN, (15, 40), 10)
		pygame.draw.circle(carSurface, self.game.GREEN, (85, 40), 10)
		self.game.window.blit(carSurface, (self.car_x4, 4 * self.game.DISPLAY_H / 6))
	
	def draw_car5(self):
		self.speed_car()
		self.pos_car()
		carSurface = pygame.Surface((100, 50))
		pygame.draw.polygon(carSurface, self.game.RED, ((15, 0), (65, 0), (85, 15), (100, 15), (100, 40), (0, 40), (0, 15)))
		pygame.draw.circle(carSurface, self.game.GREEN, (15, 40), 10)
		pygame.draw.circle(carSurface, self.game.GREEN, (85, 40), 10)
		self.game.window.blit(carSurface, (self.car_x5, 5 * self.game.DISPLAY_H / 6))
	
	def speed_car(self):
		speed_car = [0.1, 0.12, 0.14, 0.16, 0.18]
		
		if (self.car_x1 == 0):
			n = randrange(0, 5, 1)
			self.speed_car1 = speed_car[n]
			del speed_car[n]
		if (self.car_x2 == 0):
			n = randrange(0, 4, 1)
			self.speed_car2 = speed_car[n]
			del speed_car[n]
		if (self.car_x3 == 0):
			n = randrange(0, 3, 1)
			self.speed_car3 =speed_car[n]
			del speed_car[n]
		if (self.car_x4 == 0):
			n = randrange(0, 2, 1)
			self.speed_car4 = speed_car[n]
			del speed_car[n]
		if (self.car_x5 == 0):
			n = 0
			self.speed_car5 =speed_car[n]
			del speed_car[n]

	def pos_car(self):
		if (self.car_x1 >= self.game.DISPLAY_W - 120 and self.car_x2 >= self.game.DISPLAY_W - 120 and self.car_x3 >= self.game.DISPLAY_W - 120 and self.car_x4 >= self.game.DISPLAY_W - 120 and self.car_x5 >= self.game.DISPLAY_W - 120):
			self.car_x1, self.car_x2, self.car_x3, self.car_x4, self.car_x5  = 0, 0, 0, 0, 0 	
		else:
			if (self.car_x1 < self.game.DISPLAY_W - 120): self.car_x1 += self.speed_car1
			if (self.car_x2 < self.game.DISPLAY_W - 120): self.car_x2 += self.speed_car2
			if (self.car_x3 < self.game.DISPLAY_W - 120): self.car_x3 += self.speed_car3
			if (self.car_x4 < self.game.DISPLAY_W - 120): self.car_x4 += self.speed_car4
			if (self.car_x5 < self.game.DISPLAY_W - 120): self.car_x5 += self.speed_car5

	def check_input(self):
		self.game.check_input()
		self.direction.normalize()
