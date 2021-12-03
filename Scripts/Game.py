import pygame
import os
from Scenes import *
from Classes import *


class Game:
	def __init__(self):
		pygame.init()

		self.DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		self.CAPTION = "Deadline Runners"
		self.FPS = 60
		self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
		self.RED, self.GREEN, self.BLUE = (255, 0, 0), (0, 255, 0), (0, 0, 255)

		self.K_UP, self.K_DOWN, self.K_RIGHT, self.K_LEFT, self.K_KP_ENTER, self.K_SPACE, self.K_ESCAPE, self.M_UP, self.M_DOWN \
			= False, False, False, False, False, False, False, False, False
		self.W, self.H = 1280, 720

		self.window = pygame.display.set_mode((self.W, self.H))
		self.display = pygame.Surface((self.W, self.H))
		self.clock = pygame.time.Clock()
		self.font_name = self.DIRECTORY + '\\Assets\\Sprites\\Font.ttf'
		self.running = True

		self.scenes = {
			'Openings' : OpeningsScene(self, 'Openings'),
			'Settings' : SettingsScene(self, 'Settings'),
			'MiniGame' : MiniGameScene(self, 'MiniGame'),
			'MainGame' : MainGameScene(self, 'MainGame'),
			'Purchase' : PurchaseScene(self, 'Purchase'),
			'Accounts' : AccountsScene(self, 'Accounts'),
		}
		self.current_scene = self.scenes['Openings']

		pygame.display.set_caption(self.CAPTION)


	def import_assets(self, directory, assets, listed=False):
		for file in os.listdir(self.DIRECTORY + directory):
			name, extension = os.path.splitext(file)

			if '.png' in extension:
				if listed:
					assets[name] = [Surface(pygame.image.load(self.DIRECTORY + directory + file))]
				else:
					assets[name] = Surface(pygame.image.load(self.DIRECTORY + directory + file))


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


	def set_window_size(self, w, h):
		if (w == 0 and h == 0):
			self.window = pygame.display.set_mode((self.W, self.H), pygame.FULLSCREEN)
		else:
			self.window = pygame.display.set_mode((w, h))

		self.W, self.H = self.window.get_size()
		self.display = pygame.Surface((self.W, self.H))


	def draw_text(self, text, text_size, text_color, x, y, centerx=True, centery=True):
		font = pygame.font.Font(self.font_name, text_size)
		text_surface = font.render(text, False, text_color)

		text_rect = text_surface.get_rect(x=x, y=y)

		if (centerx):
			text_rect.centerx = x
		if (centery):
			text_rect.centery = y

		self.display.blit(text_surface, text_rect)

		return text_rect


	def draw_rect(self, x, y, w, h, rect_color, centerx=True, centery=True, rect=-1):
		if rect == -1:
			rect = pygame.Rect(x, y, w, h)

		if (centerx):
			rect.centerx = x
		if (centery):
			rect.centery = y

		pygame.draw.rect(self.display, rect_color, rect)

		return rect


	def draw_surface(self, surface):
		self.display.blit(surface.image, surface.rect)


game = Game()
game.set_window_size(game.W, game.H)


while game.running:
	game.current_scene.draw_scene()