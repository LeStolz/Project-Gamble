import pygame
from copy import copy
from random import randint
from Classes import Vector


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


	def cursor(self):
		self.game.draw_text(
			text='>', size=20,
			x=self.game.DISPLAY_W // 2 - 100,
			y=self.game.DISPLAY_H // 2 + self.selected_index * 30
		)


	def draw_layout(self):
		for index, selection in enumerate(self.selections):
			self.game.draw_text(text=selection, size=20, y=self.game.DISPLAY_H // 2 + index * 30)


	def draw_scene(self):
		self.running = True

		while self.running:
			self.check_input()

			self.game.display.fill(self.game.BLACK)

			self.game.draw_text(text=self.title, size=40, y=self.game.DISPLAY_H // 2 - 50)

			self.draw_layout()

			self.cursor()

			self.game.window.blit(self.game.display, (0, 0))
			pygame.display.update()

			self.game.reset_input()


	def check_input(self):
		self.game.check_input()

		if self.game.K_UP:
			self.selected_index = (self.selected_index - 1) % len(self.selections)
		if self.game.K_DOWN:
			self.selected_index = (self.selected_index + 1) % len(self.selections)

		self.process_input(self.selections[self.selected_index])


	def process_input(self, selected):
		if self.game.K_RIGHT:
			if selected == 'Quit':
				self.game.quit()
			elif selected == 'Back':
				self.game.current_scene = self.game.scenes[self.parent]
			elif selected in self.game.scenes:
				self.game.current_scene = self.game.scenes[selected]

			self.running = False
		if self.game.K_LEFT:
			self.game.current_scene = self.game.scenes[self.parent]

			self.running = False


class SettingsMenuScene(MenuScene):
	def __init__(self, game, parent, title, selections):
		MenuScene.__init__(self, game, parent, title, selections)

		self.settings = {
			'Resolution' : {
				'Current' : 0,
				'Options' : ['Fullscreen', '1280 x 720'],
				'Apply' : self.apply_resolution,
			},
			'Graphic' : {
				'Current' : 2,
				'Options' : ['Low', 'Medium', 'High'],
				'Apply' : self.apply_graphic,
			},
			'Volume' : {
				'Current' : 2,
				'Options' : [str(x) + '%' for x in range (0, 101, 25)],
				'Apply' : self.apply_volume,
			},
		}


	def draw_layout(self):
		for index, selection in enumerate(self.selections):
			if (selection == 'Quit' or selection == 'Back'):
				self.game.draw_text(text=selection, size=20, y=self.game.DISPLAY_H // 2 + index * 30)
			else:
				self.game.draw_text(text=selection, size=20, x=self.game.DISPLAY_W // 2 - 120, y=self.game.DISPLAY_H // 2 + index * 30, centerx=False)

				self.game.draw_text(
					text=self.settings[selection]['Options'][self.settings[selection]['Current']], size=20,
					x=self.game.DISPLAY_W // 2 + 100,
					y=self.game.DISPLAY_H // 2 + index * 30,
				)


	def cursor(self):
		if (self.selections[self.selected_index] == 'Back'):
			self.game.draw_text(
				text='>', size=20,
				x=self.game.DISPLAY_W // 2 - 100,
				y=self.game.DISPLAY_H // 2 + self.selected_index * 30
			)
		else:
			self.game.draw_text(
				text='<                    >', size=20,
				x=self.game.DISPLAY_W // 2 + 100,
				y=self.game.DISPLAY_H // 2 + self.selected_index * 30
			)


	def process_input(self, selected):
		if self.game.K_RIGHT:
			if selected == 'Quit':
				self.game.quit()
				self.running = False
			elif selected == 'Back':
				self.game.current_scene = self.game.scenes[self.parent]
				self.running = False
			else:
				self.settings[selected]['Current'] = (self.settings[selected]['Current'] + 1) % len(self.settings[selected]['Options'])
				self.settings[selected]['Apply'](self.settings[selected]['Options'][self.settings[selected]['Current']])
		if self.game.K_LEFT:
			if selected == 'Back':
				self.game.current_scene = self.game.scenes[self.parent]
				self.running = False
			else:
				self.settings[selected]['Current'] = (self.settings[selected]['Current'] - 1) % len(self.settings[selected]['Options'])
				self.settings[selected]['Apply'](self.settings[selected]['Options'][self.settings[selected]['Current']])


	def apply_resolution(self, option):
		if (option == 'Fullscreen'):
			self.game.set_window_size(0, 0)
		elif (option == '1280 x 720'):
			self.game.set_window_size(1280, 720)


	def apply_graphic(self, option):
		pass


	def apply_volume(self, option):
		pass


class SnakeGameScene(Scene):
	def __init__(self, game, parent, title):
		Scene.__init__(self, game, parent, title)

		self.SIZE = 30

		self.board = 0

		self.velocity = Vector(1, 0)

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
		self.init_board()

		while self.running:
			self.check_input()

			self.game.display.fill(self.game.BLACK)
			self.game.display.blit(self.board, (0, 0))

			self.move_snake()
			self.draw_snake()

			self.draw_fruit()

			self.handle_game_over()

			self.game.window.blit(self.game.display, (0, 0))
			pygame.display.update()


	def init_board(self):
		self.board = pygame.Surface((self.SIZE * 8, self.SIZE * 8))
		self.board.fill(self.game.WHITE)

		for x in range(8):
			for y in range(8):
				if (x + y) % 2:
					pygame.draw.rect(self.board, self.game.BLACK, (x * self.SIZE, y * self.SIZE, self.SIZE, self.SIZE))


	def move_snake(self):
		self.snake_rects.append(copy(self.snake_rects[-1]))
		self.snake_rects[-1].x = (self.snake_rects[-1].x + self.velocity.x) % self.game.DISPLAY_W
		self.snake_rects[-1].y = (self.snake_rects[-1].y + self.velocity.y) % self.game.DISPLAY_H


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
		for index in range(len(self.snake_rects) - 1 - 3 * self.SIZE, -1, -self.SIZE):
			if self.snake_rects[-1].colliderect(self.snake_rects[index]):
				self.game.current_scene = self.game.scenes['Game Over']

				self.__init__(self.game, self.parent, self.title)

				self.game.display.fill(self.game.BLACK)
				self.game.reset_input()

				self.running = False

				return


	def check_input(self):
		self.game.check_input()

		if self.game.K_UP:
			self.velocity = Vector(0, -1)
		if self.game.K_DOWN:
			self.velocity = Vector(0, 1)
		if self.game.K_RIGHT:
			self.velocity = Vector(1, 0)
		if self.game.K_LEFT:
			self.velocity = Vector(-1, 0)