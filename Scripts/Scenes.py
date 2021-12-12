import pygame
import random
import datetime
from copy import deepcopy
from Classes import *


class Scene:
	def __init__(self, game, title):
		self.game = game
		self.title = title
		self.running = False

		self.buttons_assets = self.game.buttons_assets
		self.background = self.game.deadline_runners_assets['Aquatica']
		self.background.resize(self.game.W, self.game.H)

		self.menu_buttons = {
			'Settings' : Button(Surface(self.buttons_assets['Bottom'].image), self.buttons_assets['Settings']),
			'Minigame' : Button(Surface(self.buttons_assets['Bottom'].image), self.buttons_assets['Minigame']),
			'Deadline Runners' : Button(Surface(self.buttons_assets['Bottom'].image), self.buttons_assets['DeadlineRunners']),
			'Shop' : Button(Surface(self.buttons_assets['Bottom'].image), self.buttons_assets['Shop']),
			'Accounts' : Button(Surface(self.buttons_assets['Bottom'].image), self.buttons_assets['Accounts']),
			'Escape' : Button(Surface(self.buttons_assets['ArrowBottom'].image), Surface(self.buttons_assets['Escape'].image)),
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

		self.menu_buttons['Escape'].resize(55, 55)
		self.menu_buttons['Escape'].position(self.game.W - 55, 0)

		self.last_menu_button_state = 'None'
		self.last_menu_button_name = 'None'
		self.last_button_state = 'None'
		self.last_button_name = 'None'


	def draw_menu_buttons(self):
		self.check_menu_button_names()
		self.check_menu_button_input()

		self.game.draw_text(' ' + self.game.ACCOUNT['Name'], 35, self.game.WHITE, 0, 0, centerx=False, centery=False)

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

		touched_button = False

		for i, v in self.menu_buttons.items():
			if v.top.rect.collidepoint(pygame.mouse.get_pos()):
				touched_button = True
				self.hover_menu_button_name = i
				if self.last_menu_button_state != 'Hover' or self.last_menu_button_name != i:
					self.last_menu_button_state = 'Hover'
					self.last_menu_button_name = i
					self.game.menu_sfx['ButtonDown'].play()
				break

		if not touched_button:
			self.last_menu_button_name = 'None'

		if self.game.M_UP and self.down_menu_button_name != '':
			self.up_menu_button_name = self.down_menu_button_name
			self.down_menu_button_name = ''
			self.last_menu_button_state = 'Up'
			self.last_menu_button_name = self.down_menu_button_name
		elif self.game.M_DOWN and self.hover_menu_button_name != '':
			self.down_menu_button_name = self.hover_menu_button_name
			self.hover_menu_button_name = ''
			self.last_menu_button_state = 'Down'
			self.last_menu_button_name = self.hover_menu_button_name


	def check_menu_button_input(self):
		if self.down_menu_button_name in self.menu_buttons.keys() and self.down_menu_button_name != self.title and self.game.M_DOWN:
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

		touched_button = False

		for i, v in self.buttons.items():
			if v.top.rect.collidepoint(pygame.mouse.get_pos()):
				touched_button = True
				self.hover_button_name = i
				if self.last_button_state != 'Hover' or self.last_button_name != i:
					self.last_button_state = 'Hover'
					self.last_button_name = i
					self.game.menu_sfx['ButtonDown'].play()
				break

		if not touched_button:
			self.last_button_name = 'None'

		if self.game.M_UP and self.down_button_name != '':
			self.hover_button_name = self.down_button_name
			self.down_button_name = ''
			self.last_button_state = 'Up'
			self.last_button_name = self.down_button_name
		elif self.game.M_DOWN and self.hover_button_name != '':
			self.down_button_name = self.hover_button_name
			self.hover_button_name = ''
			self.last_button_state = 'Down'
			self.last_button_name = self.hover_button_name


	def check_button_input(self):
		pass


	def draw_options(self):
		pass


	def draw_scene(self):
		self.running = True
		self.down_menu_button_name = self.title
		self.down_button_name = ''
		self.game.reset_input()

		while self.running:
			self.game.draw_surface(self.background)

			self.draw_options()

			self.game.reset_input()
			self.game.game_loop()


class GameScene(Scene):
	def __init__(self, game, title):
		Scene.__init__(self, game, title)

		self.buttons['Back'] = Button(Surface(self.buttons_assets['ArrowBottom'].image), Surface(self.buttons_assets['ArrowLeft'].image))

		self.buttons['Back'].resize(55, 55)
		self.buttons['Back'].position(0, 0)

		self.score = 0
		self.lives = 5
		self.back = False
		self.finished = False
		self.played = False

		self.start_time = pygame.time.get_ticks()


	def check_button_input(self):
		if self.down_button_name in self.buttons.keys() and self.down_button_name == 'Back' and not self.finished and self.game.M_DOWN:
			self.lives = 0
			self.back = True
			self.finished = True
			self.game.reset_input()


	def reset_game(self):
		self.finished = True
		self.lives = 0

		self.game.draw_text('Game over', 65, self.game.GREEN, self.game.W // 2, self.game.H // 3 - 65)
		if self.score >= 0:
			self.game.draw_text(f'You earned {self.score}', 35, self.game.WHITE, self.game.W // 2, self.game.H // 3 + 15)
			if not self.played and self.score > 0:
				self.game.menu_sfx['Earned'].play()
				self.played = True
		else:
			self.game.draw_text(f'You lost {-self.score}', 35, self.game.WHITE, self.game.W // 2, self.game.H // 3 + 15)
			if not self.played:
				self.game.menu_sfx['Lost'].play()
				self.played = True

		self.game.draw_text(f'Your money {self.game.ACCOUNT["Money"] + self.score}', 35, self.game.WHITE, self.game.W // 2, self.game.H // 3 + 65)

		if pygame.time.get_ticks() - self.start_time < 650:
			self.game.draw_text('Click to continue', 35, self.game.WHITE, self.game.W // 2, self.game.H * 3 // 4, centery=False)
		elif pygame.time.get_ticks() - self.start_time > 650 * 2:
			self.start_time = pygame.time.get_ticks()

		if self.game.M_DOWN:
			self.played = False

			if self.back:
				if self.title == 'Deadline Runners Game':
					self.game.switch_scene(self.title, 'Deadline Runners')
				else:
					self.game.switch_scene(self.title, 'Minigame')

				self.game.music.stop()
				self.game.music = self.game.menu_sfx['Music']
				self.game.music.play(-1)

			self.game.ACCOUNT['Money'] += self.score
			self.__init__(self.game, self.title)

		self.game.reset_input()


	def draw_scene(self):
		self.running = True
		self.down_button_name = ''
		self.game.reset_input()

		while self.running:
			self.draw_options()

			if self.title == 'Deadline Runners Game':
				self.game.reset_input()
			else:
				self.draw_buttons()

			self.game.game_loop()


class OpeningScene(Scene):
	def __init__(self, game, title):
		Scene.__init__(self, game, title)

		self.start_time = pygame.time.get_ticks()

		self.game.draw_surface(self.background)
		self.game.draw_text('Deadline Runners', 65, self.game.RED, self.game.W // 2, self.game.H // 3 - 65)


	def draw_options(self):
		if pygame.time.get_ticks() - self.start_time < 650:
			self.game.draw_text('Click to continue', 35, self.game.WHITE, self.game.W // 2, self.game.H * 3 // 4, centery=False)
		elif pygame.time.get_ticks() - self.start_time > 650 * 2:
			self.start_time = pygame.time.get_ticks()

		self.game.draw_text('Deadline Runners', 65, self.game.RED, self.game.W // 2, self.game.H // 3 - 65)

		if self.game.M_DOWN:
			self.game.switch_scene(self.title, 'Login')


class LoginScene(Scene):
	class TextBox:
		def __init__(self, text, rect):
			self.text = text
			self.rect = rect


	def __init__(self, game, title):
		Scene.__init__(self, game, title)

		self.buttons['Back'] = Button(Surface(self.buttons_assets['ArrowBottom'].image), Surface(self.buttons_assets['ArrowLeft'].image))

		self.buttons['Back'].resize(55, 55)
		self.buttons['Back'].position(0, 0)

		self.username = self.TextBox(
			self.game.username,
			self.game.draw_rect(self.game.W // 6 + 310, self.game.H // 3 + 18, self.game.W * 4 // 6 - 310, 40, self.game.GREY,
			centerx=False, no_draw=True)
		)
		self.password = self.TextBox(
			'',
			self.game.draw_rect(self.game.W // 6 + 310, self.game.H // 3 + 68, self.game.W * 4 // 6 - 310, 40, self.game.GREY,
			centerx=False, no_draw=True)
		)

		self.selected = self.username

		self.start_time = pygame.time.get_ticks()


	def check_button_input(self):
		if self.down_button_name in self.buttons.keys() and self.down_button_name == 'Back' and self.game.M_DOWN:
			self.game.switch_scene(self.title, self.game.old_scene)


	def draw_options(self):
		self.draw_buttons()

		if pygame.time.get_ticks() - self.start_time < 650:
			self.game.draw_text('Click to continue', 35, self.game.WHITE, self.game.W // 2, self.game.H * 3 // 4, centery=False)
		elif pygame.time.get_ticks() - self.start_time > 650 * 2:
			self.start_time = pygame.time.get_ticks()

		self.game.draw_text('Login', 65, self.game.GREEN, self.game.W // 2, self.game.H // 3 - 65)

		self.game.draw_rect(rect=self.username.rect, rect_color=self.game.GREY)
		self.game.draw_rect(rect=self.password.rect, rect_color=self.game.GREY)
		self.game.draw_rect(rect=self.selected.rect, rect_color=self.game.WHITE)
		self.game.draw_text('Username', 35, self.game.GREEN, self.game.W // 6, self.game.H // 3 + 15, centerx=False)
		self.game.draw_text('PassWord', 35, self.game.GREEN, self.game.W // 6, self.game.H // 3 + 65, centerx=False)
		self.game.draw_text(' ' + self.username.text, 35, self.game.BLACK, self.game.W // 6 + 310, self.game.H // 3 + 15, centerx=False)
		self.game.draw_text(' ' + self.password.text, 35, self.game.BLACK, self.game.W // 6 + 310, self.game.H // 3 + 65, centerx=False)

		if self.game.K_RETURN:
			self.selected = self.password
			self.check_account()
		elif self.game.K_BACKSPACE:
			self.selected.text = self.selected.text[:-1]
		else:
			self.selected.text += self.game.unicode

		if self.game.M_DOWN:
			if self.username.rect.collidepoint(pygame.mouse.get_pos()):
				self.selected = self.username
				return
			elif self.password.rect.collidepoint(pygame.mouse.get_pos()):
				self.selected = self.password
				return

			self.check_account()


	def check_account(self):
		self.username.text = self.username.text.lower()
		self.password.text = self.password.text.lower()

		if 'new account' in self.game.username and not 'new account' in self.username.text:
			self.game.ACCOUNTS[self.username.text] = deepcopy(self.game.ACCOUNTS[self.game.username])
			self.game.ACCOUNTS[self.username.text]['Name'] = self.username.text
			self.game.ACCOUNTS[self.username.text]['Password'] = self.password.text
			self.game.ACCOUNTS.pop(self.game.username)

		if self.username.text in self.game.ACCOUNTS and self.game.ACCOUNTS[self.username.text]['Password'] == self.password.text:
			self.game.ACCOUNT = self.game.ACCOUNTS[self.username.text]
			self.game.set_window_size()

			if (datetime.datetime.now()).strftime('%m/%d/%Y') != self.game.ACCOUNT['Previous session']:
				self.game.switch_scene(self.title, 'Reward')
			else:
				self.game.switch_scene(self.title, 'Accounts')
		else:
			pass


class HistoryScene(Scene):
	def __init__(self, game, title):
		Scene.__init__(self, game, title)

		self.buttons['Back'] = Button(Surface(self.buttons_assets['ArrowBottom'].image), Surface(self.buttons_assets['ArrowLeft'].image))

		self.buttons['Back'].resize(55, 55)
		self.buttons['Back'].position(0, 0)


	def check_button_input(self):
		if self.down_button_name in self.buttons.keys() and self.down_button_name == 'Back' and self.game.M_DOWN:
			self.game.switch_scene(self.title, self.game.old_scene)


	def draw_options(self):
		self.draw_buttons()

		self.game.draw_text('Gambling History', 45, self.game.GREEN, self.game.W // 2, 0, centery=False)

		count = 0
		for v in self.game.ACCOUNT['Races']:
			if 'Earned' in v:
				self.game.draw_text(v, 35, self.game.GREEN, self.game.W // 2, self.game.H // 6 + 65 * count, secondary_font=True)
			else:
				self.game.draw_text(v, 35, self.game.RED, self.game.W // 2, self.game.H // 6 + 65 * count, secondary_font=True)
			count += 1


class RewardScene(Scene):
	def __init__(self, game, title):
		Scene.__init__(self, game, title)

		self.score = 5000

		self.start_time = pygame.time.get_ticks()


	def draw_options(self):
		self.game.draw_text('Daily reward', 65, self.game.GREEN, self.game.W // 2, self.game.H // 3 - 65)
		self.game.draw_text(f'You earned {self.score}', 35, self.game.WHITE, self.game.W // 2, self.game.H // 3 + 15)
		self.game.draw_text(f'Your money {self.game.ACCOUNT["Money"] + self.score}', 35, self.game.WHITE, self.game.W // 2, self.game.H // 3 + 65)

		if pygame.time.get_ticks() - self.start_time < 650:
			self.game.draw_text('Click to continue', 35, self.game.WHITE, self.game.W // 2, self.game.H * 3 // 4, centery=False)
		elif pygame.time.get_ticks() - self.start_time > 650 * 2:
			self.start_time = pygame.time.get_ticks()

		if self.game.M_DOWN:
			self.game.switch_scene(self.title, 'Accounts')

			self.game.ACCOUNT['Money'] += self.score
			self.game.ACCOUNT['Previous session'] = (datetime.datetime.now()).strftime('%m/%d/%Y')
			self.__init__(self.game, self.title)

		self.game.reset_input()


class SettingsScene(Scene):
	def __init__(self, game, title):
		Scene.__init__(self, game, title)

		self.qualities = {
			'Resolution' : ['Win', 'Full'],
			'Graphic' : ['Low', 'Medium', 'High'],
			'Sound' : ['0', '50', '100'],
		}

		self.options = {
			'Resolution' : self.game.ACCOUNT['Resolution'],
			'Graphic' : self.game.ACCOUNT['Graphic'],
			'Sound' : self.game.ACCOUNT['Sound'],
		}

		count = 0
		for i, v in self.options.items():
			self.buttons[i + 'Left'] = Button(Surface(self.buttons_assets['ArrowBottom'].image), Surface(self.buttons_assets['ArrowLeft'].image))
			self.buttons[i + 'Right'] = Button(Surface(self.buttons_assets['ArrowBottom'].image), Surface(self.buttons_assets['ArrowRight'].image))

			self.buttons[i + 'Left'].position(self.game.W * 5 // 6 - 340, self.game.H // 3 + 100 * (count - 1) - 40)
			self.buttons[i + 'Right'].position(self.game.W * 5 // 6, self.game.H // 3 + 100 * (count - 1) - 40)
			count += 1


	def check_button_input(self):
		if self.down_button_name in self.buttons.keys() and self.game.M_DOWN:
			true_down_button_name = self.down_button_name.replace('Left', '').replace('Right', '')

			if 'Left' in self.down_button_name:
				self.options[true_down_button_name] = (self.options[true_down_button_name] - 1) % len(self.qualities[true_down_button_name])
			elif 'Right' in self.down_button_name:
				self.options[true_down_button_name] = (self.options[true_down_button_name] + 1) % len(self.qualities[true_down_button_name])

			if true_down_button_name == 'Resolution':
				self.game.ACCOUNT['Resolution'] = self.options[true_down_button_name]
				self.game.set_window_size()
			elif true_down_button_name == 'Graphic':
				self.game.ACCOUNT['Graphic'] = self.options[true_down_button_name]
			elif true_down_button_name == 'Sound':
				self.game.ACCOUNT['Sound'] = self.options[true_down_button_name]
				self.game.set_sound_volume()


	def draw_options(self):
		self.draw_menu_buttons()
		self.draw_buttons()

		self.game.draw_text(self.title, 45, self.game.GREEN, self.game.W // 2, 0, centery=False)

		count = 0
		for i, v in self.options.items():
			self.game.draw_text(i, 35, self.game.WHITE, self.game.W // 6, self.game.H // 3 + 100 * (count - 1), centerx=False)
			self.game.draw_text(self.qualities[i][v], 35, self.game.WHITE, self.game.W * 5 // 6 - 123, self.game.H // 3 + 100 * (count - 1))
			count += 1


class MinigameScene(Scene):
	def __init__(self, game, title):
		Scene.__init__(self, game, title)

		self.thumbnails = self.game.thumbnails_assets

		self.buttons['Egg Collector Game'] = Button(Surface(self.buttons_assets['ArrowBottom'].image), Surface(self.buttons_assets['ArrowRight'].image))
		self.buttons['Space Invader Game'] = Button(Surface(self.buttons_assets['ArrowBottom'].image), Surface(self.buttons_assets['ArrowRight'].image))

		self.buttons['Egg Collector Game'].position(self.game.W // 8 + self.game.H // 4.5 - 40, self.game.H // 6 + self.game.H // 2.25 + 45)
		self.buttons['Space Invader Game'].position(self.game.W * 7 // 8 - self.game.H * 2 // 9 - 40, self.game.H // 6 + self.game.H // 2.25 + 45)

		self.thumbnails['EggCollector'].resize(self.game.H // 2.25, self.game.H // 2.25)
		self.thumbnails['SpaceInvader'].resize(self.game.H // 2.25, self.game.H // 2.25)

		self.thumbnails['EggCollector'].position(self.game.W // 8, self.game.H // 6 + 30)
		self.thumbnails['SpaceInvader'].position(self.game.W * 7 // 8 - self.game.H // 2.25, self.game.H // 6 + 30)


	def check_button_input(self):
		if self.down_button_name in self.buttons.keys() and self.game.M_DOWN:
			if self.down_button_name == 'Space Invader Game':
				self.game.music.stop()
				self.game.music = self.game.space_invader_sfx['Music']
				self.game.music.play(-1)
			else:
				self.game.music.stop()
				self.game.music = self.game.egg_collector_sfx['Music']
				self.game.music.play(-1)
			self.game.switch_scene(self.title, self.down_button_name)


	def draw_options(self):
		self.draw_menu_buttons()
		self.draw_buttons()

		self.game.draw_surface(self.thumbnails['EggCollector'])
		self.game.draw_surface(self.thumbnails['SpaceInvader'])

		self.game.draw_text(self.title, 45, self.game.GREEN, self.game.W // 2, 0, centery=False)

		self.game.draw_text('Egg Collector', 35, self.game.WHITE, self.game.W // 8 + self.game.H // 4.5, self.game.H // 6 - 15, centery=False)
		self.game.draw_text('Space Invader', 35, self.game.WHITE, self.game.W * 7 // 8 - self.game.H * 2 // 9, self.game.H // 6 - 15, centery=False)


class DeadlineRunnersScene(Scene):
	def __init__(self, game, title):
		Scene.__init__(self, game, title)

		self.thumbnails = self.game.thumbnails_assets
		self.buttons_assets = self.game.buttons_assets

		self.qualities = {
			'Character set' : ['Chivalry', 'Deadliners', 'Aquatica'],
			'Track length' : ['Short', 'Medium', 'Long'],
		}

		self.options = {
			'Character set' : self.game.ACCOUNT['Character set'],
			'Track length' : self.game.ACCOUNT['Track length'],
		}

		for v in self.qualities['Character set']:
			self.thumbnails[v].resize(self.game.H // 2.25, self.game.H // 2.25)
			self.thumbnails[v].position(self.game.W * 5 // 6 - 174 - self.game.H // 4.5, self.game.H * 0.725 - self.game.H // 2.25 - 155)

		self.buttons['Deadline Runners Game'] = Button(
			Surface(self.buttons_assets['Bottom'].image), Surface(self.buttons_assets['DeadlineRunners'].image)
		)

		self.buttons['Deadline Runners Game'].resize(self.game.W // 5, self.game.H // 6)
		self.buttons['Deadline Runners Game'].position(self.game.W // 6 + 220 - self.game.W // 10, self.game.H // 2 - 155)

		count = 0
		for i, v in self.options.items():
			self.buttons[i + 'Left'] = Button(Surface(self.buttons_assets['ArrowBottom'].image), Surface(self.buttons_assets['ArrowLeft'].image))
			self.buttons[i + 'Right'] = Button(Surface(self.buttons_assets['ArrowBottom'].image), Surface(self.buttons_assets['ArrowRight'].image))

			self.buttons[i + 'Left'].position(self.game.W * 5 // 6 - 442, self.game.H * 0.725 + 100 * (count - 1) - 40)
			self.buttons[i + 'Right'].position(self.game.W * 5 // 6, self.game.H * 0.725 + 100 * (count - 1) - 40)
			count += 1


	def check_button_input(self):
		if self.down_button_name in self.buttons.keys() and self.game.M_DOWN:
			true_down_button_name = self.down_button_name.replace('Left', '').replace('Right', '')

			if self.down_button_name == 'Deadline Runners Game':
				self.game.scenes[self.down_button_name].__init__(self.game, self.down_button_name)
				self.game.switch_scene(self.title, self.down_button_name)
				self.character_set = self.qualities['Character set'][self.game.ACCOUNT['Character set']]
				self.game.music.stop()
				if self.character_set == 'Deadliners':
					self.game.music = self.game.deadline_runners_sfx['Deadliners']
				elif self.character_set == 'Aquatica':
					self.game.music = self.game.deadline_runners_sfx['Aquatica']
				elif self.character_set == 'Chivalry':
					self.game.music = self.game.deadline_runners_sfx['Chivalry']
				self.game.music.play(-1)
				return

			if 'Left' in self.down_button_name:
				self.options[true_down_button_name] = (self.options[true_down_button_name] - 1) % len(self.qualities[true_down_button_name])
			elif 'Right' in self.down_button_name:
				self.options[true_down_button_name] = (self.options[true_down_button_name] + 1) % len(self.qualities[true_down_button_name])

			if true_down_button_name == 'Character set':
				self.game.ACCOUNT['Character set'] = self.options[true_down_button_name]
			elif true_down_button_name == 'Track length':
				self.game.ACCOUNT['Track length'] = self.options[true_down_button_name]


	def draw_options(self):
		self.draw_menu_buttons()
		self.draw_buttons()

		self.game.draw_text(self.title, 45, self.game.GREEN, self.game.W // 2, 0, centery=False)

		self.game.draw_text('Start Race', 35, self.game.WHITE, self.game.W // 6 + 220, self.game.H // 2 - 205, centery=False)

		self.game.draw_surface(self.thumbnails[self.qualities['Character set'][self.options['Character set']]])

		count = 0
		for i, v in self.options.items():
			self.game.draw_text(i, 35, self.game.WHITE, self.game.W // 6, self.game.H * 0.725 + 100 * (count - 1), centerx=False)
			self.game.draw_text(self.qualities[i][v], 35, self.game.WHITE, self.game.W * 5 // 6 - 174, self.game.H * 0.725 + 100 * (count - 1))
			count += 1


class ShopScene(Scene):
	def __init__(self, game, title):
		Scene.__init__(self, game, title)

		self.thumbnails = self.game.thumbnails_assets
		self.buttons_assets = self.game.buttons_assets

		self.qualities = {
			'Item' : ['Amulet', 'Endurance', 'Strength', 'Swiftness'],
		}

		self.options = {
			'Item' : self.game.ACCOUNT['Item'],
		}

		self.descriptions = {
			'Amulet' : 'You can bet your all on this',
			'Endurance' : 'You have high hazard affinity',
			'Strength' : 'You are an experienced combatant',
			'Swiftness' : 'You overdosed on sugar this morning',
		}

		self.costs = {
			'Amulet' : 5000,
			'Endurance' : 1000,
			'Strength' : 2000,
			'Swiftness' : 3000,
		}

		for v in self.qualities['Item']:
			self.thumbnails[v].resize(self.game.H // 2.25, self.game.H // 2.25)
			self.thumbnails[v].position(self.game.W * 5 // 6 - 174 - self.game.H // 4.5, self.game.H * 0.281 - 155)

		self.buttons['Purchase'] = Button(
			Surface(self.buttons_assets['Bottom'].image), Surface(self.buttons_assets['Purchase'].image)
		)

		self.buttons['Purchase'].resize(self.game.W // 5, self.game.H // 6)
		self.buttons['Purchase'].position(self.game.W // 6 + 220 - self.game.W // 10, self.game.H // 2 - 155)

		count = 0
		for i, v in self.options.items():
			self.buttons[i + 'Left'] = Button(Surface(self.buttons_assets['ArrowBottom'].image), Surface(self.buttons_assets['ArrowLeft'].image))
			self.buttons[i + 'Right'] = Button(Surface(self.buttons_assets['ArrowBottom'].image), Surface(self.buttons_assets['ArrowRight'].image))

			self.buttons[i + 'Left'].position(self.game.W * 5 // 6 - 442, self.game.H * 0.725 + 100 * (count - 1) - 40)
			self.buttons[i + 'Right'].position(self.game.W * 5 // 6, self.game.H * 0.725 + 100 * (count - 1) - 40)
			count += 1


	def check_button_input(self):
		if self.down_button_name in self.buttons.keys() and self.game.M_DOWN:
			true_down_button_name = self.down_button_name.replace('Left', '').replace('Right', '')

			if self.down_button_name == 'Purchase':
				if self.costs[self.qualities['Item'][self.options['Item']]] <= self.game.ACCOUNT['Money']:
					self.game.ACCOUNT['Items'][self.qualities['Item'][self.options['Item']]] += 1
					self.game.ACCOUNT['Money'] -= self.costs[self.qualities['Item'][self.options['Item']]]
				else:
					pass

				return

			if 'Left' in self.down_button_name:
				self.options[true_down_button_name] = (self.options[true_down_button_name] - 1) % len(self.qualities[true_down_button_name])
			elif 'Right' in self.down_button_name:
				self.options[true_down_button_name] = (self.options[true_down_button_name] + 1) % len(self.qualities[true_down_button_name])

			if true_down_button_name == 'Item':
				self.game.ACCOUNT['Item'] = self.options[true_down_button_name]


	def draw_options(self):
		self.draw_menu_buttons()
		self.draw_buttons()

		self.game.draw_text(self.title, 45, self.game.GREEN, self.game.W // 2, 0, centery=False)

		self.game.draw_text(
			f'Your money {self.game.ACCOUNT["Money"]}',
			25, self.game.WHITE, self.game.W // 6 + 220,  self.game.H * 0.281 - 155, centery=False
		)
		self.game.draw_text(
			'You have ' + str(self.game.ACCOUNT['Items'][self.qualities['Item'][self.options['Item']]]),
			25, self.game.WHITE, self.game.W // 6 + 220,  self.game.H // 2 - 135 + self.game.H // 6, centery=False
		)
		self.game.draw_text(
			'Buy for ' + str(self.costs[self.qualities['Item'][self.options['Item']]]),
			35, self.game.WHITE, self.game.W // 6 + 220, self.game.H // 2 - 205, centery=False
		)

		self.game.draw_text(
			self.descriptions[self.qualities['Item'][self.options['Item']]],
			25, self.game.WHITE, self.game.W * 5 // 6 - 174, self.game.H * 0.725
		)

		self.game.draw_surface(self.thumbnails[self.qualities['Item'][self.options['Item']]])

		count = 0
		for i, v in self.options.items():
			self.game.draw_text(self.qualities[i][v], 35, self.game.WHITE, self.game.W * 5 // 6 - 174, self.game.H * 0.725 + 100 * (count - 1))
			count += 1


class AccountsScene(Scene):
	def __init__(self, game, title):
		Scene.__init__(self, game, title)

		self.buttons = {}
		offset = self.game.draw_text('Current Account', 25, self.game.GREEN, self.game.W // 2, self.game.H * 0.281 - 142, no_draw=True).w // 2

		for i, v in self.game.ACCOUNTS.items():
			if i != self.game.ACCOUNT['Name']:
				offset = max(offset, self.game.draw_text(i, 35, self.game.WHITE, self.game.W // 2, self.game.H // 2, no_draw=True).w // 2)

		count = 0
		for i, v in self.game.ACCOUNTS.items():
			if i != self.game.ACCOUNT['Name']:
				self.buttons[i] = Button(Surface(self.buttons_assets['ArrowBottom'].image), Surface(self.buttons_assets['ArrowRight'].image))
				self.buttons[i].position(self.game.W // 2 - 100 - offset, self.game.H * 0.281 - 142 + 185 - 40 + 100 * count)
				count += 1
			else:
				self.buttons['History'] = Button(Surface(self.buttons_assets['ArrowBottom'].image), Surface(self.buttons_assets['History'].image))
				self.buttons['History'].position(self.game.W // 2 - 100 - offset, self.game.H * 0.281 - 142 + 60 - 40)


	def check_button_input(self):
		if self.down_button_name in self.buttons.keys() and self.game.M_DOWN:
			if self.down_button_name == 'History':
				self.game.switch_scene(self.title, 'History')
			else:
				self.game.switch_scene(self.title, 'Login', self.down_button_name)


	def draw_options(self):
		self.draw_menu_buttons()
		self.draw_buttons()

		self.game.draw_text(self.title, 45, self.game.GREEN, self.game.W // 2, 0, centery=False)

		self.game.draw_text('Current Account', 25, self.game.GREEN, self.game.W // 2, self.game.H * 0.281 - 142)
		self.game.draw_text(self.game.ACCOUNT['Name'], 35, self.game.WHITE, self.game.W // 2, self.game.H * 0.281 - 142 + 60)
		self.game.draw_text('Change Account', 25, self.game.GREEN, self.game.W // 2, self.game.H * 0.281 - 142 + 120)

		count = 0
		for i, v in self.game.ACCOUNTS.items():
			if i != self.game.ACCOUNT['Name']:
				self.game.draw_text(i, 35, self.game.WHITE, self.game.W // 2, self.game.H * 0.281 - 142 + 185 + 100 * count)
				count += 1


class EscapeScene(Scene):
	def __init__(self, game, title):
		Scene.__init__(self, game, title)


	def draw_options(self):
		self.game.running = False

		self.game.ACCOUNT['Money'] += self.game.scenes['Deadline Runners Game'].score
		self.game.ACCOUNT['Money'] += self.game.scenes['Egg Collector Game'].score
		self.game.ACCOUNT['Money'] += self.game.scenes['Space Invader Game'].score

		self.game.export_data()

		for i, v in self.game.scenes.items():
			v.running = False
