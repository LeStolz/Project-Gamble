import pygame
from Scenes import *


class Game:
	def __init__(self):
		pygame.init()

		self.K_UP, self.K_DOWN, self.K_RIGHT, self.K_LEFT, self.K_m = False, False, False, False, False
		self.DISPLAY_W, self.DISPLAY_H = 1280, 720
		self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
		self.RED, self.GREEN, self.BLUE = (255, 0, 0), (0, 255, 0), (0, 0, 255)

		self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
		self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H), pygame.RESIZABLE)
		self.font_name = pygame.font.get_default_font()
		self.running = True

		self.scenes = {
			'Main Menu'	 : MenuScene(self, 'Main Menu', 'Main Menu',  ['Start Game', 'Options', 'Credits', 'Quit']),
			'Start Game' : MenuScene(self, 'Main Menu', 'Start Game', ['Main Game', 'Snake Game', 'Back']),
			'Options' 	 : MenuScene(self, 'Main Menu', 'Options',    ['Resolutions', 'Volume', 'Graphics', 'Back']),
			'Credits' 	 : MenuScene(self, 'Main Menu', 'Credits',	  ['Your mom', 'My mom', 'Our mom', 'Back']),
			'Game Over'  : MenuScene(self, 'Main Menu', 'Game Over',  ['Main Game', 'Snake Game', 'Back']),
			'Snake Game' : SnakeGameScene(self, 'Start Game', 'Snake Game'),
			'Main Game'  : MainGameScene(self, 'Start Game', 'Main Game'),
		}

		self.current_scene = self.scenes['Main Menu']


	def check_input(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.quit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP or event.key == pygame.K_w:
					self.K_UP = True
				if event.key == pygame.K_DOWN or event.key == pygame.K_s:
					self.K_DOWN = True
				if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
					self.K_RIGHT = True
				if event.key == pygame.K_LEFT or event.key == pygame.K_a:
					self.K_LEFT = True
				if event.key == pygame.K_m:
					self.K_m = True

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_UP or event.key == pygame.K_w:
					self.K_UP = False
				if event.key == pygame.K_DOWN or event.key == pygame.K_s:
					self.K_DOWN = False
				if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
					self.K_RIGHT = False
				if event.key == pygame.K_LEFT or event.key == pygame.K_a:
					self.K_LEFT = False
				if event.key == pygame.K_m:
					self.K_m = False


	def quit(self):
		self.running = False
		self.current_scene.running = False


	def reset_input(self):
		self.K_UP, self.K_DOWN, self.K_RIGHT, self.K_LEFT = False, False, False, False


	def draw_text(self, text, size, x=-1, y=-1, color=-1):
		x = self.DISPLAY_W // 2 if x == -1 else x
		y = self.DISPLAY_H // 2 if y == -1 else y
		color = self.WHITE if color == -1 else color

		font = pygame.font.Font(self.font_name, size)
		text_surface = font.render(text, True, color)

		text_rect = text_surface.get_rect(center=(x, y))

		self.display.blit(text_surface, text_rect)

		return text_rect


	def draw_rect(self, x=-1, y=-1, w=20, h=20, color=-1, rect=-1):
		x = self.DISPLAY_W // 2 if x == -1 else x
		y = self.DISPLAY_H // 2 if y == -1 else y
		color = self.WHITE if color == -1 else color

		if rect == -1:
			rect = pygame.Rect(x - w // 2, y - h // 2, w, h)

		pygame.draw.rect(self.display, color, rect)

		return rect
