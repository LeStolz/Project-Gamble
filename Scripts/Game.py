import pygame
import os
from Scenes import *
from Classes import *


class Game:
	def __init__(self):
		pygame.init()
		pygame.display.set_caption('Deadline Runners')

		self.DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		self.FPS = 60
		self.BLACK, self.WHITE, self.RED, self.GREEN, self.BLUE = \
			(0, 0, 0), (255, 255, 255), (244, 81, 30), (67, 160, 71), (3, 155, 229)

		self.K_UP, self.K_DOWN, self.K_RIGHT, self.K_LEFT, self.K_KP_ENTER, self.K_SPACE, self.K_ESCAPE, self.M_UP, self.M_DOWN \
			= False, False, False, False, False, False, False, False, False

		self.W, self.H = 1280, 720
		self.RESOLUTION, self.GRAPHIC, self.SOUND = 1, 1, 1

		self.window = pygame.display.set_mode((self.W, self.H), pygame.FULLSCREEN)
		self.display = pygame.Surface((self.W, self.H))
		self.font_name = self.DIRECTORY + '\\Assets\\Sprites\\Font.ttf'
		self.clock = pygame.time.Clock()
		self.running = True

		self.buttons_assets = {}
		self.import_assets()

		self.scenes = {
			'Openings' : OpeningsScene(self, 'Openings'),
			'Settings' : SettingsScene(self, 'Settings'),
			'MiniGame' : MiniGameScene(self, 'MiniGame'),
			'MainGame' : MainGameScene(self, 'MainGame'),
			'Purchase' : PurchaseScene(self, 'Purchase'),
			'Accounts' : AccountsScene(self, 'Accounts'),
		}
		self.current_scene = self.scenes['Openings']


	def import_assets(self):
		for file in os.listdir(self.DIRECTORY + '\\Assets\\Sprites\\Buttons\\'):
			name, extension = os.path.splitext(file)

			if '.png' in extension:
				self.buttons_assets[name] = Surface(pygame.image.load(self.DIRECTORY + '\\Assets\\Sprites\\Buttons\\' + file))


	def check_input(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
				self.current_scene.running = False

			if event.type == pygame.KEYDOWN:
				if (event.key == pygame.K_UP or event.key == pygame.K_w):
					self.K_UP = True
				if (event.key == pygame.K_DOWN or event.key == pygame.K_s):
					self.K_DOWN = True
				if (event.key == pygame.K_RIGHT or event.key == pygame.K_d):
					self.K_RIGHT = True
				if (event.key == pygame.K_LEFT or event.key == pygame.K_a):
					self.K_LEFT = True
				if (event.key == pygame.K_KP_ENTER):
					self.K_KP_ENTER = True
				if (event.key == pygame.K_SPACE):
					self.K_SPACE = True
				if (event.key == pygame.K_ESCAPE):
					self.K_ESCAPE = True

			if event.type == pygame.KEYUP:
				if (event.key == pygame.K_UP or event.key == pygame.K_w):
					self.K_UP = False
				if (event.key == pygame.K_DOWN or event.key == pygame.K_s):
					self.K_DOWN = False
				if (event.key == pygame.K_RIGHT or event.key == pygame.K_d):
					self.K_RIGHT = False
				if (event.key == pygame.K_LEFT or event.key == pygame.K_a):
					self.K_LEFT = False
				if (event.key == pygame.K_KP_ENTER):
					self.K_KP_ENTER = False
				if (event.key == pygame.K_SPACE):
					self.K_SPACE = False
				if (event.key == pygame.K_ESCAPE):
					self.K_ESCAPE = False

			if event.type == pygame.MOUSEBUTTONUP:
				self.M_UP = True
				self.M_DOWN = False

			if event.type == pygame.MOUSEBUTTONDOWN:
				self.M_UP = False
				self.M_DOWN = True

			if event.type == pygame.VIDEORESIZE:
				self.set_window_size()


	def reset_input(self):
		self.K_UP, self.K_DOWN, self.K_RIGHT, self.K_LEFT, self.K_KP_ENTER, self.K_SPACE, self.K_ESCAPE, self.M_UP, self.M_DOWN \
			= False, False, False, False, False, False, False, False, False


	def game_loop(self):
		self.clock.tick(self.FPS)

		self.check_input()

		self.window.blit(self.display, (0, 0))
		pygame.display.update()


	def switch_scene(self, old_scene, new_scene):
		self.scenes[old_scene].running = False
		self.current_scene = self.scenes[new_scene]


	def set_window_size(self):
		self.W, self.H = self.window.get_size()
		if self.RESOLUTION:
			self.window = pygame.display.set_mode((self.W, self.H), pygame.FULLSCREEN)
		else:
			self.window = pygame.display.set_mode((self.W, self.H), pygame.RESIZABLE)
		self.W, self.H = self.window.get_size()

		self.display = pygame.Surface((self.W, self.H))

		self.import_assets()
		for i, v in self.scenes.items():
			v.__init__(self, i)


	def draw_text(self, text, text_size, text_color, x, y, centerx=True, centery=True, right=False):
		font = pygame.font.Font(self.font_name, text_size)
		text_surface = font.render(text, False, text_color)

		text_rect = text_surface.get_rect(x=x, y=y)

		if (centerx):
			text_rect.centerx = x
		if (centery):
			text_rect.centery = y
		if (right):
			text_rect.right = x

		self.display.blit(text_surface, text_rect)

		return text_rect


	def draw_rect(self, x=-1, y=-1, w=-1, h=-1, rect_color=-1, centerx=True, centery=True, right=False, rect=-1):
		if rect == -1:
			rect = pygame.Rect(x, y, w, h)

			if (centerx):
				rect.centerx = x
			if (centery):
				rect.centery = y
			if (right):
				text_rect.right = x

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