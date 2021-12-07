import pygame
from Scenes import *
from Classes import *


class DeadlineRunnersGameScene(GameScene):
	def __init__(self, game, title):
		GameScene.__init__(self, game, title)

		self.BACKGROUND = pygame.transform.scale(self.game.space_invader_assets['Background'].image, (self.game.W, self.game.H))


	def draw_options(self):
		self.game.display.blit(self.BACKGROUND, (0,0))

		if self.lives <= 0:
			self.reset_game()
			return