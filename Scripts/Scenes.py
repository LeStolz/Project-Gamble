import pygame
from Classes import *


class Scene:
	def __init__(self, game, title):
		self.game = game
		self.title = title
		self.running = False


class OpeningsScene(Scene):
	def __init__(self, game, title):
		Scene.__init__(self, game, title)


	def draw_scene(self):
		self.running = True

		start_time = pygame.time.get_ticks()
		text_color = self.game.WHITE

		self.game.draw_text('Press SPACE to continue', 40, text_color, self.game.W // 2, self.game.H // 2)

		while self.running:
			self.game.display.fill(self.game.BLACK)

			if (pygame.time.get_ticks() - start_time >= 600):
				start_time = pygame.time.get_ticks()
				text_color = self.game.BLACK if text_color == self.game.WHITE else self.game.WHITE

			self.game.draw_text('Press SPACE to continue', 40, text_color, self.game.W // 2, self.game.H // 2)

			if self.game.K_SPACE:
				self.game.switch_scene('Openings', 'MainGame')

			self.game.game_loop()


class MenuScene(Scene):
	def __init__(self, game, title):
		Scene.__init__(self, game, title)

		self.HOVER = 1.05
		self.UP = 1.1
		self.DOWN = 1.15

		self.buttons = {}
		self.game.import_assets('\\Assets\\Sprites\\Buttons\\', self.buttons, True)
		self.menu_button_names = ['Settings', 'MiniGame', 'MainGame', 'Purchase', 'Accounts']

		self.hover_button_name = ''
		self.up_button_name = ''
		self.down_button_name = ''

		for i, v in enumerate(self.menu_button_names):
			self.buttons[v].append(Surface(self.buttons['Bottom'][0].image))

			self.buttons[v][0].resize(self.game.W // 5, self.game.H // 6)
			self.buttons[v][1].resize(self.game.W // 5, self.game.H // 6)
			self.buttons[v][0].position(i * self.buttons[v][0].rect.w, self.game.H - self.buttons[v][0].rect.h)
			self.buttons[v][1].position(i * self.buttons[v][1].rect.w, self.game.H - self.buttons[v][1].rect.h)


	def draw_navigation(self):
		for i, v in enumerate(self.menu_button_names):
			if v == self.down_button_name:
				self.buttons[v][0].position(i * self.buttons[v][0].rect.w, self.game.H - self.buttons[v][0].rect.h // self.DOWN)
			elif v == self.up_button_name:
				self.buttons[v][0].position(i * self.buttons[v][0].rect.w, self.game.H - self.buttons[v][0].rect.h // self.UP)
			elif v == self.hover_button_name:
				self.buttons[v][0].position(i * self.buttons[v][0].rect.w, self.game.H - self.buttons[v][0].rect.h // self.HOVER)
			else:
				self.buttons[v][0].position(i * self.buttons[v][0].rect.w, self.game.H - self.buttons[v][0].rect.h)

			self.game.draw_surface(self.buttons[v][1])
			self.game.draw_surface(self.buttons[v][0])


	def check_button_names(self):
		for i in self.buttons:
			if self.buttons[i][0].rect.collidepoint(pygame.mouse.get_pos()):
				self.hover_button_name = i

				if self.game.M_UP:
					self.up_button_name = i
					self.down_button_name = ''
				elif self.game.M_DOWN:
					self.up_button_name = ''
					self.down_button_name = i

				return

		self.hover_button_name = ''


	def check_switch_scene(self):
		if (self.down_button_name != '' and self.down_button_name != self.title):
			self.game.switch_scene(self.title, self.down_button_name)


	def draw_menu(self):
		pass


	def draw_scene(self):
		self.running = True
		self.down_button_name = self.title
		self.game.reset_input()

		while self.running:
			self.game.display.fill(self.game.BLACK)

			self.check_button_names()
			self.check_switch_scene()

			self.draw_navigation()
			self.draw_menu()

			self.game.reset_input()

			self.game.game_loop()


class SettingsScene(MenuScene):
	def __init__(self, game, title):
		MenuScene.__init__(self, game, title)


	def draw_menu(self):
		self.game.draw_text(self.title, 40, self.game.WHITE, self.game.W // 2, self.game.H // 2)


class MiniGameScene(MenuScene):
	def __init__(self, game, title):
		MenuScene.__init__(self, game, title)


	def draw_menu(self):
		self.game.draw_text(self.title, 40, self.game.WHITE, self.game.W // 2, self.game.H // 2)


class MainGameScene(MenuScene):
	def __init__(self, game, title):
		MenuScene.__init__(self, game, title)


	def draw_menu(self):
		self.game.draw_text(self.title, 40, self.game.WHITE, self.game.W // 2, self.game.H // 2)


class PurchaseScene(MenuScene):
	def __init__(self, game, title):
		MenuScene.__init__(self, game, title)


	def draw_menu(self):
		self.game.draw_text(self.title, 40, self.game.WHITE, self.game.W // 2, self.game.H // 2)


class AccountsScene(MenuScene):
	def __init__(self, game, title):
		MenuScene.__init__(self, game, title)


	def draw_menu(self):
		self.game.draw_text(self.title, 40, self.game.WHITE, self.game.W // 2, self.game.H // 2)