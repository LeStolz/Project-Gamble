import pygame
from Classes import *


class Scene:
	def __init__(self, game, title):
		self.game = game
		self.title = title
		self.running = False


class MenuScene(Scene):
	def __init__(self, game, title):
		Scene.__init__(self, game, title)

		self.buttons = self.game.import_assets('\\Assets\\Sprites\\Buttons\\')
		self.buttons = {i : Button(Surface(self.buttons['Bottom'].image), v) for i, v in self.buttons.items()}

		self.menu_button_names = ['Settings', 'MiniGame', 'MainGame', 'Purchase', 'Accounts']

		self.hover_button_name = ''
		self.up_button_name = ''
		self.down_button_name = ''

		for i, v in enumerate(self.menu_button_names):
			self.buttons[v].resize(self.game.W // 5, self.game.H // 6)
			self.buttons[v].position(i * self.buttons[v].top.rect.w, self.game.H - self.buttons[v].top.rect.h)


	def draw_navigation(self):
		for i, v in enumerate(self.menu_button_names):
			if v == self.down_button_name:
				self.buttons[v].down()
			elif v == self.up_button_name:
				self.buttons[v].up()
			elif v == self.hover_button_name:
				self.buttons[v].hover()
			else:
				self.buttons[v].normal()

			self.game.draw_button(self.buttons[v])


	def check_button_names(self):
		for i, v in self.buttons.items():
			if v.top.rect.collidepoint(pygame.mouse.get_pos()):
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
		if (self.up_button_name in self.menu_button_names and self.up_button_name != self.title):
			self.game.switch_scene(self.title, self.up_button_name)


	def draw_menu(self):
		pass


	def draw_scene(self):
		self.running = True
		self.up_button_name = self.title
		self.game.reset_input()

		while self.running:
			self.game.display.fill(self.game.BLACK)

			self.check_button_names()
			self.check_switch_scene()

			self.draw_menu()

			self.game.reset_input()

			self.game.game_loop()


class OpeningsScene(MenuScene):
	def __init__(self, game, title):
		MenuScene.__init__(self, game, title)

		self.start_time = pygame.time.get_ticks()
		self.text_color = self.game.WHITE


	def draw_menu(self):
		if (pygame.time.get_ticks() - self.start_time >= 600):
			self.start_time = pygame.time.get_ticks()
			self.text_color = self.game.BLACK if self.text_color == self.game.WHITE else self.game.WHITE

		self.game.draw_text('Deadline Runners', 60, self.game.RED, self.game.W // 2, self.game.H // 2.75)
		self.game.draw_text('Press SPACE to continue', 30, self.text_color, self.game.W // 2, self.game.H // 1.25)

		if self.game.K_SPACE:
			self.game.switch_scene('Openings', 'MainGame')


class SettingsScene(MenuScene):
	def __init__(self, game, title):
		MenuScene.__init__(self, game, title)


	def draw_menu(self):
		self.draw_navigation()

		self.game.draw_text(self.title, 40, self.game.GREEN, self.game.W // 2, self.game.H // 2)


class MiniGameScene(MenuScene):
	def __init__(self, game, title):
		MenuScene.__init__(self, game, title)


	def draw_menu(self):
		self.draw_navigation()

		self.game.draw_text(self.title, 40, self.game.GREEN, self.game.W // 2, self.game.H // 2)


class MainGameScene(MenuScene):
	def __init__(self, game, title):
		MenuScene.__init__(self, game, title)


	def draw_menu(self):
		self.draw_navigation()

		self.game.draw_text(self.title, 40, self.game.GREEN, self.game.W // 2, self.game.H // 2)


class PurchaseScene(MenuScene):
	def __init__(self, game, title):
		MenuScene.__init__(self, game, title)


	def draw_menu(self):
		self.draw_navigation()

		self.game.draw_text(self.title, 40, self.game.GREEN, self.game.W // 2, self.game.H // 2)


class AccountsScene(MenuScene):
	def __init__(self, game, title):
		MenuScene.__init__(self, game, title)


	def draw_menu(self):
		self.draw_navigation()

		self.game.draw_text(self.title, 40, self.game.GREEN, self.game.W // 2, self.game.H // 2)