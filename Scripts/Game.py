import pygame
import os
import sys
from copy import deepcopy
from Scenes import *
from Classes import *
from EggCollector import *
from SpaceInvader import *
from DeadlineRunners import *


class Game:
	def __init__(self):
		pygame.init()
		pygame.mixer.init(devicename='CABLE Input (VB-Audio Virtual Cable)')
		pygame.display.set_caption('Deadline Runners')
		pygame.event.set_allowed([
			pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.VIDEORESIZE
		])

		try:
  			self.DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '\\'
		except NameError:
  			self.DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))) + '\\'

		self.FPS = 60
		self.BLACK, self.GREY, self.WHITE, self.RED, self.GREEN, self.BLUE \
			= (0, 0, 0), (200, 200, 200), (255, 255, 255), (244, 81, 30), (67, 160, 71), (3, 155, 229)

		self.K_UP, self.K_DOWN, self.K_RIGHT, self.K_LEFT, self.K_RETURN, self.K_SPACE, self.K_BACKSPACE, self.M_UP, self.M_DOWN \
			= False, False, False, False, False, False, False, False, False
		self.unicode = ''

		self.FULLSCREEN_W, self.FULLSCREEN_H = pygame.display.Info().current_w, pygame.display.Info().current_h
		self.WINSCREEN_W, self.WINSCREEN_H = 1280, 720
		self.W, self.H = self.FULLSCREEN_W, self.FULLSCREEN_H

		self.window = pygame.display.set_mode((self.W, self.H), pygame.FULLSCREEN | pygame.RESIZABLE | pygame.DOUBLEBUF)
		self.display = pygame.Surface((self.W, self.H))
		self.font_name = self.DIRECTORY + 'Assets\\Sprites\\Font.ttf'
		self.secondary_font_name = self.DIRECTORY + 'Assets\\Sprites\\SecondaryFont.ttf'
		self.clock = pygame.time.Clock()
		self.running = True

		self.ACCOUNTS = {}
		self.ACCOUNT = {}
		self.username = ''
		self.import_data()

		self.buttons_assets = {}
		self.thumbnails_assets = {}
		self.egg_collector_assets = {}
		self.space_invader_assets = {}
		self.deadline_runners_assets = {}
		self.import_assets()

		self.space_invader_sfx = {}
		self.egg_collector_sfx = {}
		self.menu_sfx = {}
		self.deadline_runners_sfx = {}
		self.import_sfx()

		self.music = self.menu_sfx['Music']
		self.music.play(-1)

		self.scenes = {
			'Opening' : OpeningScene(self, 'Opening'),
			'Login' : LoginScene(self, 'Login'),
			'Reward' : RewardScene(self, 'Reward'),
			'Settings' : SettingsScene(self, 'Settings'),
			'Minigame' : MinigameScene(self, 'Minigame'),
			'Deadline Runners' : DeadlineRunnersScene(self, 'Deadline Runners'),
			'Deadline Runners Game' : DeadlineRunnersGameScene(self, 'Deadline Runners Game'),
			'Shop' : ShopScene(self, 'Shop'),
			'Accounts' : AccountsScene(self, 'Accounts'),
			'History' : HistoryScene(self, 'History'),
			'Egg Collector Game' : EggCollectorGameScene(self, 'Egg Collector Game'),
			'Space Invader Game' : SpaceInvaderGameScene(self, 'Space Invader Game'),
			'Escape' : EscapeScene(self, 'Escape'),
		}
		self.old_scene = 'Opening'
		self.current_scene = self.scenes['Opening']
		self.set_sound_volume()


	def import_data(self):
		account_data_file = open(self.DIRECTORY + 'Scripts\\AccountData.txt', 'r')

		while True:
			account = account_data_file.readline().rstrip('\n')

			if not account:
				break

			self.ACCOUNTS[account] = {}
			self.ACCOUNTS[account]['Name'] = str(account)
			self.ACCOUNTS[account]['Password'] = str(account_data_file.readline().rstrip('\n'))
			self.ACCOUNTS[account]['Money'] = int(account_data_file.readline().rstrip('\n'))
			self.ACCOUNTS[account]['Resolution'] = int(account_data_file.readline().rstrip('\n'))
			self.ACCOUNTS[account]['Graphic'] = int(account_data_file.readline().rstrip('\n'))
			self.ACCOUNTS[account]['Sound'] = int(account_data_file.readline().rstrip('\n'))
			self.ACCOUNTS[account]['Character set'] = int(account_data_file.readline().rstrip('\n'))
			self.ACCOUNTS[account]['Track length'] = int(account_data_file.readline().rstrip('\n'))
			self.ACCOUNTS[account]['Item'] = int(account_data_file.readline().rstrip('\n'))
			self.ACCOUNTS[account]['Items'] = {}
			self.ACCOUNTS[account]['Items']['Amulet'] = int(account_data_file.readline().rstrip('\n'))
			self.ACCOUNTS[account]['Items']['Endurance'] = int(account_data_file.readline().rstrip('\n'))
			self.ACCOUNTS[account]['Items']['Strength'] = int(account_data_file.readline().rstrip('\n'))
			self.ACCOUNTS[account]['Items']['Swiftness'] = int(account_data_file.readline().rstrip('\n'))
			self.ACCOUNTS[account]['Previous session'] = str(account_data_file.readline().rstrip('\n'))
			self.ACCOUNTS[account]['Race Number'] = int(account_data_file.readline().rstrip('\n'))
			self.ACCOUNTS[account]['Races'] = []

			for i in range(self.ACCOUNTS[account]['Race Number']):
				self.ACCOUNTS[account]['Races'].append(str(account_data_file.readline().rstrip('\n')))

			self.ACCOUNT = self.ACCOUNTS[account]
			self.username = account

		account_data_file.close()


	def export_data(self):
		account_data_file = open(self.DIRECTORY + 'Scripts\\AccountData.txt', 'w')

		previous_session_account = deepcopy(self.ACCOUNT)
		self.ACCOUNTS.pop(self.ACCOUNT['Name'])
		self.ACCOUNTS[previous_session_account['Name']] = previous_session_account

		for account in self.ACCOUNTS.keys():
			account_data_file.write(str(self.ACCOUNTS[account]['Name']) + '\n')
			account_data_file.write(str(self.ACCOUNTS[account]['Password']) + '\n')
			account_data_file.write(str(self.ACCOUNTS[account]['Money']) + '\n')
			account_data_file.write(str(self.ACCOUNTS[account]['Resolution']) + '\n')
			account_data_file.write(str(self.ACCOUNTS[account]['Graphic']) + '\n')
			account_data_file.write(str(self.ACCOUNTS[account]['Sound']) + '\n')
			account_data_file.write(str(self.ACCOUNTS[account]['Character set']) + '\n')
			account_data_file.write(str(self.ACCOUNTS[account]['Track length']) + '\n')
			account_data_file.write(str(self.ACCOUNTS[account]['Item']) + '\n')
			account_data_file.write(str(self.ACCOUNTS[account]['Items']['Amulet']) + '\n')
			account_data_file.write(str(self.ACCOUNTS[account]['Items']['Endurance']) + '\n')
			account_data_file.write(str(self.ACCOUNTS[account]['Items']['Strength']) + '\n')
			account_data_file.write(str(self.ACCOUNTS[account]['Items']['Swiftness']) + '\n')
			account_data_file.write(str(self.ACCOUNTS[account]['Previous session']) + '\n')
			account_data_file.write(str(self.ACCOUNTS[account]['Race Number']) + '\n')

			for v in self.ACCOUNTS[account]['Races']:
				account_data_file.write(str(v) + '\n')

		account_data_file.close()


	def resource_path(self, relative_path):
		try:
			base_path = sys._MEIPASS
		except Exception:
			base_path = os.path.abspath('.')

		return os.path.join(base_path, relative_path)


	def import_assets_from_directory(self, directory):
		assets = {}

		for file in os.listdir(self.DIRECTORY + directory):
			name, extension = os.path.splitext(file)

			if '.png' in extension:
				assets[name] = Surface(pygame.image.load(self.resource_path(self.DIRECTORY + directory + file)).convert_alpha())
			elif '.mp3' in extension or '.wav' in extension:
				assets[name] = pygame.mixer.Sound(self.resource_path(self.DIRECTORY + directory + file))

		return assets


	def import_assets(self):
		self.buttons_assets = self.import_assets_from_directory('Assets\\Sprites\\Buttons\\')
		self.thumbnails_assets = self.import_assets_from_directory('Assets\\Sprites\\Thumbnails\\')
		self.egg_collector_assets = self.import_assets_from_directory('Assets\\Sprites\\EggCollector\\')
		self.space_invader_assets = self.import_assets_from_directory('Assets\\Sprites\\SpaceInvader\\')
		self.deadline_runners_assets = self.import_assets_from_directory('Assets\\Sprites\\DeadlineRunners\\')


	def import_sfx(self):
		self.space_invader_sfx = self.import_assets_from_directory('Assets\\Sfx\\SpaceInvader\\')
		self.egg_collector_sfx = self.import_assets_from_directory('Assets\\Sfx\\EggCollector\\')
		self.menu_sfx = self.import_assets_from_directory('Assets\\Sfx\\Menu\\')
		self.deadline_runners_sfx = self.import_assets_from_directory('Assets\\Sfx\\Deadliners\\')


	def check_input(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.switch_scene(self.current_scene.title, 'Escape')

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP or event.key == pygame.K_w:
					self.K_UP = True
				if event.key == pygame.K_DOWN or event.key == pygame.K_s:
					self.K_DOWN = True
				if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
					self.K_RIGHT = True
				if event.key == pygame.K_LEFT or event.key == pygame.K_a:
					self.K_LEFT = True
				if event.key == pygame.K_RETURN:
					self.K_RETURN = True
				if event.key == pygame.K_SPACE:
					self.K_SPACE = True
				if event.key == pygame.K_BACKSPACE:
					self.K_BACKSPACE = True
				else:
					self.unicode = event.unicode

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_UP or event.key == pygame.K_w:
					self.K_UP = False
				if event.key == pygame.K_DOWN or event.key == pygame.K_s:
					self.K_DOWN = False
				if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
					self.K_RIGHT = False
				if event.key == pygame.K_LEFT or event.key == pygame.K_a:
					self.K_LEFT = False
				if event.key == pygame.K_RETURN:
					self.K_RETURN = False
				if event.key == pygame.K_SPACE:
					self.K_SPACE = False
				if event.key == pygame.K_BACKSPACE:
					self.K_BACKSPACE = False

			if event.type == pygame.MOUSEBUTTONUP:
				self.M_UP = True
				self.M_DOWN = False

			if event.type == pygame.MOUSEBUTTONDOWN:
				self.M_UP = False
				self.M_DOWN = True

			if event.type == pygame.VIDEORESIZE:
				self.set_window_size()


	def reset_input(self):
		self.K_UP, self.K_DOWN, self.K_RIGHT, self.K_LEFT, self.K_RETURN, self.K_SPACE, self.K_BACKSPACE, self.M_UP, self.M_DOWN \
			= False, False, False, False, False, False, False, False, False
		self.unicode = ''


	def game_loop(self):
		self.clock.tick(self.FPS)

		self.check_input()

		self.window.blit(self.display, (0, 0))
		pygame.display.update()


	def switch_scene(self, old_scene, new_scene, username=''):
		self.scenes[old_scene].running = False
		self.old_scene = old_scene
		self.current_scene = self.scenes[new_scene]

		if username != '':
			self.username = username
			self.scenes['Login'].__init__(self, 'Login')

		self.reset_input()


	def set_window_size(self):
		if self.ACCOUNT['Resolution']:
			self.W, self.H = self.FULLSCREEN_W, self.FULLSCREEN_H
			self.window = pygame.display.set_mode((self.W, self.H), pygame.FULLSCREEN | pygame.RESIZABLE | pygame.DOUBLEBUF)
		else:
			if self.W == self.FULLSCREEN_W and self.H == self.FULLSCREEN_H:
				self.W, self.H = self.WINSCREEN_W, self.WINSCREEN_H
			else:
				self.W, self.H = self.window.get_size()
			self.window = pygame.display.set_mode((self.W, self.H), pygame.RESIZABLE | pygame.DOUBLEBUF)

		self.display = pygame.Surface((self.W, self.H))

		self.import_assets()
		for i, v in self.scenes.items():
			v.__init__(self, i)


	def set_sound_volume(self):
		for v in self.space_invader_sfx.values():
			v.set_volume(self.ACCOUNT['Sound'] * 0.5)
		for v in self.egg_collector_sfx.values():
			v.set_volume(self.ACCOUNT['Sound'] * 0.5)
		for v in self.menu_sfx.values():
			v.set_volume(self.ACCOUNT['Sound'] * 0.5)
		for v in self.deadline_runners_sfx.values():
			v.set_volume(self.ACCOUNT['Sound'] * 0.5)


	def draw_text(self, text, text_size, text_color, x, y, \
		centerx=True, centery=True, right=False, secondary_font=False, outline=True, no_draw=False):
		if secondary_font:
			font = pygame.font.Font(self.secondary_font_name, 2 * text_size)
		else:
			font = pygame.font.Font(self.font_name, text_size)

		text_surface = font.render(text, False, text_color)

		text_rect = text_surface.get_rect(x=x, y=y)

		if centerx:
			text_rect.centerx = x
		if centery:
			text_rect.centery = y
		if right:
			text_rect.right = x

		if no_draw:
			return text_rect

		if outline and text_color != self.BLACK and text_color != self.WHITE and text_size < 60:
			self.draw_text(text, text_size, self.BLACK, x - 1, y, centerx, centery, right, secondary_font, outline, no_draw)
			self.draw_text(text, text_size, self.BLACK, x + 1, y, centerx, centery, right, secondary_font, outline, no_draw)
			self.draw_text(text, text_size, self.BLACK, x, y - 1, centerx, centery, right, secondary_font, outline, no_draw)
			self.draw_text(text, text_size, self.BLACK, x, y + 1, centerx, centery, right, secondary_font, outline, no_draw)
		elif outline and text_color != self.BLACK and text_color != self.WHITE and text_size >= 60:
			self.draw_text(text, text_size, self.BLACK, x, y + 5, centerx, centery, right, secondary_font, outline, no_draw)

		self.display.blit(text_surface, text_rect)

		return text_rect


	def draw_rect(self, x=-1, y=-1, w=-1, h=-1, rect_color=-1, centerx=True, centery=True, right=False, rect=-1, no_draw=False):
		if rect == -1:
			rect = pygame.Rect(x, y, w, h)

			if centerx:
				rect.centerx = x
			if centery:
				rect.centery = y
			if right:
				text_rect.right = x

		if no_draw:
			return rect

		pygame.draw.rect(self.display, rect_color, rect)

		return rect


	def draw_surface(self, surface):
		self.display.blit(surface.image, surface.rect)


	def draw_button(self, button):
		self.draw_surface(button.bottom)
		self.draw_surface(button.top)
		self.draw_text(
			button.text, 40, self.WHITE, button.top.rect.centerx + button.top.rect.h * 0.025, button.top.rect.centery - button.top.rect.h * 0.075
		)


game = Game()


while game.running:
	game.current_scene.draw_scene()