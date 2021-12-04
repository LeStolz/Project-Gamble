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

		self.assets = self.game.buttons_assets

		self.menu_buttons = {
			'Settings' : Button(Surface(self.assets['Bottom'].image), self.assets['Settings']),
			'MiniGame' : Button(Surface(self.assets['Bottom'].image), self.assets['MiniGame']),
			'MainGame' : Button(Surface(self.assets['Bottom'].image), self.assets['MainGame']),
			'Purchase' : Button(Surface(self.assets['Bottom'].image), self.assets['Purchase']),
			'Accounts' : Button(Surface(self.assets['Bottom'].image), self.assets['Accounts']),
		}
		self.buttons = {}

		self.hover_menu_button_name = ''
		self.up_menu_button_name = ''
		self.down_menu_button_name = ''
		self.hover_button_name = ''
		self.down_button_name = ''

		count = 0
		for i, v in self.menu_buttons.items():
			v.resize(self.game.W // 5, self.game.H // 6)
			v.position(count * v.top.rect.w, self.game.H - v.top.rect.h)
			count += 1


	def draw_menu_buttons(self):
		self.check_menu_button_names()
		self.check_menu_button_input()

		for i, v in self.menu_buttons.items():
			if i == self.down_menu_button_name:
				v.down()
			elif i == self.up_menu_button_name:
				v.up()
			elif i == self.hover_menu_button_name:
				v.hover()
			else:
				v.normal()

			self.game.draw_button(v)


	def check_menu_button_names(self):
		self.hover_menu_button_name = ''

		for i, v in self.menu_buttons.items():
			if v.top.rect.collidepoint(pygame.mouse.get_pos()):
				self.hover_menu_button_name = i
				break

		if self.game.M_UP and self.down_menu_button_name != '':
			self.up_menu_button_name = self.down_menu_button_name
			self.down_menu_button_name = ''
		elif self.game.M_DOWN and self.hover_menu_button_name != '':
			self.down_menu_button_name = self.hover_menu_button_name
			self.hover_menu_button_name = ''


	def check_menu_button_input(self):
		if (self.down_menu_button_name in self.menu_buttons.keys() and self.down_menu_button_name != self.title and self.game.M_DOWN):
			self.game.switch_scene(self.title, self.down_menu_button_name)


	def draw_buttons(self):
		self.check_button_names()
		self.check_button_input()

		for i, v in self.buttons.items():
			if i == self.down_button_name:
				v.down()
			elif i == self.hover_button_name:
				v.hover()
			else:
				v.normal()

			self.game.draw_button(v)


	def check_button_names(self):
		self.hover_button_name = ''

		for i, v in self.buttons.items():
			if v.top.rect.collidepoint(pygame.mouse.get_pos()):
				self.hover_button_name = i
				break

		if self.game.M_UP and self.down_button_name != '':
			self.hover_button_name = self.down_button_name
			self.down_button_name = ''
		elif self.game.M_DOWN and self.hover_button_name != '':
			self.down_button_name = self.hover_button_name
			self.hover_button_name = ''


	def check_button_input(self):
		pass


	def draw_options(self):
		pass


	def draw_scene(self):
		self.running = True
		self.down_menu_button_name = self.title
		self.game.reset_input()

		while self.running:
			self.game.display.fill(self.game.BLACK)

			self.draw_options()

			self.game.reset_input()
			self.game.game_loop()


class OpeningsScene(MenuScene):
	def __init__(self, game, title):
		MenuScene.__init__(self, game, title)

		self.start_time = pygame.time.get_ticks()
		self.text_color = self.game.WHITE


	def draw_options(self):
		if (pygame.time.get_ticks() - self.start_time >= 650):
			self.start_time = pygame.time.get_ticks()
			self.text_color = self.game.BLACK if self.text_color == self.game.WHITE else self.game.WHITE

		self.game.draw_text('Deadline Runners', 65, self.game.RED, self.game.W // 2, self.game.H // 4, centery=False)
		self.game.draw_text('Click to continue', 35, self.text_color, self.game.W // 2, self.game.H * 3 // 4, centery=False)

		if self.game.M_DOWN:
			self.game.switch_scene('Openings', 'MainGame')


class SettingsScene(MenuScene):
	def __init__(self, game, title):
		MenuScene.__init__(self, game, title)

		self.qualities = {
			'Resolution' : ['Win', 'Full'],
			'Graphic' : ['Low', 'Medium', 'High'],
			'Sound' : ['0', '50', '100'],
		}

		self.options = {
			'Resolution' : self.game.RESOLUTION,
			'Graphic' : self.game.GRAPHIC,
			'Sound' : self.game.SOUND,
		}

		count = 0
		for i, v in self.options.items():
			self.buttons[i + 'Left'] = Button(Surface(self.assets['ArrowBottom'].image), Surface(self.assets['ArrowLeft'].image))
			self.buttons[i + 'Right'] = Button(Surface(self.assets['ArrowBottom'].image), Surface(self.assets['ArrowRight'].image))

			self.buttons[i + 'Left'].position(self.game.W * 4 // 5 - 340, self.game.H // 3 + 100 * (count - 1) - 40)
			self.buttons[i + 'Right'].position(self.game.W * 4 // 5, self.game.H // 3 + 100 * (count - 1) - 40)
			count += 1


	def check_button_input(self):
		if (self.down_button_name in self.buttons.keys() and self.game.M_DOWN):
			true_down_button_name = self.down_button_name.replace('Left', '').replace('Right', '')

			if 'Left' in self.down_button_name:
				self.options[true_down_button_name] = (self.options[true_down_button_name] - 1) % len(self.qualities[true_down_button_name])
			elif 'Right' in self.down_button_name:
				self.options[true_down_button_name] = (self.options[true_down_button_name] + 1) % len(self.qualities[true_down_button_name])

			if true_down_button_name == 'Resolution':
				self.game.RESOLUTION = self.options[true_down_button_name]
				self.game.set_window_size()
			elif true_down_button_name == 'Graphic':
				self.game.GRAPHIC = self.options[true_down_button_name]
			elif true_down_button_name == 'Sound':
				self.game.SOUND = self.options[true_down_button_name]


	def draw_options(self):
		self.draw_menu_buttons()
		self.draw_buttons()

		self.game.draw_text(self.title, 45, self.game.GREEN, self.game.W // 2, 0, centery=False)

		count = 0
		for i, v in self.options.items():
			self.game.draw_text(i, 35, self.game.WHITE, self.game.W // 5, self.game.H // 3 + 100 * (count - 1), centerx=False)
			self.game.draw_text(self.qualities[i][v], 35, self.game.WHITE, self.game.W * 4 // 5 - 123, self.game.H // 3 + 100 * (count - 1))

			self.game.draw_button(self.buttons[i + 'Left'])
			self.game.draw_button(self.buttons[i + 'Right'])
			count += 1


class MiniGameScene(MenuScene):
	def __init__(self, game, title):
		MenuScene.__init__(self, game, title)


	def draw_options(self):
		self.draw_menu_buttons()

		self.game.draw_text(self.title, 45, self.game.GREEN, self.game.W // 2, 0, centery=False)


class MainGameScene(MenuScene):
	def __init__(self, game, title):
		MenuScene.__init__(self, game, title)


	def draw_options(self):
		self.draw_menu_buttons()

		self.game.draw_text(self.title, 45, self.game.GREEN, self.game.W // 2, 0, centery=False)


class PurchaseScene(MenuScene):
	def __init__(self, game, title):
		MenuScene.__init__(self, game, title)


	def draw_options(self):
		self.draw_menu_buttons()

		self.game.draw_text(self.title, 45, self.game.GREEN, self.game.W // 2, 0, centery=False)


class AccountsScene(MenuScene):
	def __init__(self, game, title):
		MenuScene.__init__(self, game, title)


	def draw_options(self):
		self.draw_menu_buttons()

		self.game.draw_text(self.title, 45, self.game.GREEN, self.game.W // 2, 0, centery=False)