import pygame
from Scenes import *
from Classes import *


class EggCollectorGameScene(GameScene):
	class Basket():
		def __init__(self, menu):
			self.menu = menu

			self.x = self.menu.game.W // 2 - 230 // 2
			self.y = self.menu.game.H - 155

			self.image = pygame.transform.scale(self.menu.game.egg_collector_assets['Basket'].image, (230, 155))

			self.rect = self.image.get_rect()
			self.rect.w = 200
			self.rect.h = 10

			self.rect.x = self.x + self.rect.w // 4
			self.rect.y = self.y + self.rect.h


		def draw(self):
			self.menu.game.display.blit(self.image, (self.x, self.y))


		def update(self):
			if self.menu.game.K_LEFT:
				self.x -= 30
			if self.menu.game.K_RIGHT:
				self.x += 30

			self.x = min(self.x, self.menu.game.W - 230)
			self.x = max(self.x, 0)

			self.rect.x = self.x + self.rect.w // 4
			self.rect.y = self.y + self.rect.h


	class Chickens():
		def __init__(self, menu):
			self.menu = menu

			self.x = 0
			self.y = 0

			self.image = pygame.transform.scale(self.menu.game.egg_collector_assets['Chickens'].image, (self.menu.game.W, self.menu.game.H // 3.25))


		def draw(self):
			self.menu.game.display.blit(self.image, (self.x, self.y))


		def update(self):
			pass


	class Egg():
		def __init__(self, menu):
			self.menu = menu

			self.pos = [self.menu.game.W // 6, self.menu.game.W // 1.925, self.menu.game.W // 1.175]

			self.image = pygame.transform.scale(self.menu.game.egg_collector_assets['Egg'].image, (72, 84))

			self.rect = self.image.get_rect()
			self.rect.w = 72
			self.rect.h = 10

			self.x = random.choice(self.pos)
			self.y = self.menu.game.H // 6.25


		def reset_pos(self):
			self.x = random.choice(self.pos)

			self.y = self.menu.game.H // 6.25


		def draw(self):
			self.menu.game.display.blit(self.image, (self.x, self.y))


		def update(self):
			if self.y > self.menu.game.H:
				self.reset_pos()

			self.y += 10
			self.rect.x = self.x
			self.rect.y = self.y + 84 - 10


	class Shit():
		def __init__(self, menu):
			self.menu = menu

			self.pos = [self.menu.game.W // 6, self.menu.game.W // 1.925, self.menu.game.W // 1.175]

			self.image = pygame.transform.scale(self.menu.game.egg_collector_assets['Shit'].image, (72, 84))

			self.rect = self.image.get_rect()
			self.rect.w = 72
			self.rect.h = 10

			self.x = random.choice(self.pos)
			self.y = self.menu.game.H // 6.25


		def reset_pos(self):
			self.x = random.choice(self.pos)

			self.y = self.menu.game.H // 6.25


		def draw(self):
			self.menu.game.display.blit(self.image, (self.x, self.y))


		def update(self):
			if self.y > self.menu.game.H:
				self.reset_pos()
				self.menu.num_shit += 1

			self.y += 15
			self.rect.x = self.x
			self.rect.y = self.y + 84 - 10


	class GoldenEgg():
		def __init__(self, menu):
			self.menu = menu

			self.pos = [self.menu.game.W // 6, self.menu.game.W // 1.925, self.menu.game.W // 1.175]

			self.image = pygame.transform.scale(self.menu.game.egg_collector_assets['GoldenEgg'].image, (48, 56))

			self.rect = self.image.get_rect()
			self.rect.w = 48
			self.rect.h = 10

			self.x = random.choice(self.pos)
			self.y = self.menu.game.H // 6.25

			self.flag = False


		def reset_pos(self):
			self.x = random.choice(self.pos)

			self.y = self.menu.game.H // 6.25


		def draw(self):
			if self.menu.num_shit >= 10:
				self.menu.num_shit = 0
				self.flag = True

			if not self.flag:
				return

			self.menu.game.display.blit(self.image, (self.x, self.y))


		def update(self):
			if self.menu.num_shit >= 10:
				self.menu.num_shit = 0
				self.flag = True

			if not self.flag:
				return

			if self.y > self.menu.game.H:
				self.reset_pos()
				self.flag = False

			self.y += 20
			self.rect.x = self.x
			self.rect.y = self.y + 56 - 10


	def __init__(self, game, title):
		GameScene.__init__(self, game, title)

		self.hit_sound = pygame.mixer.Sound(self.game.space_invader_sfx['Hit'])

		self.BACKGROUND = pygame.transform.scale(self.game.space_invader_assets['Background'].image, (self.game.W, self.game.H))

		self.num_shit = 0

		self.basket = self.Basket(self)
		self.shit = self.Shit(self)
		self.egg = self.Egg(self)
		self.golden_egg = self.GoldenEgg(self)
		self.chickens = self.Chickens(self)


	def draw_options(self):
		self.game.display.blit(self.BACKGROUND, (0,0))

		self.basket.draw()
		self.shit.draw()
		self.egg.draw()
		self.golden_egg.draw()
		self.chickens.draw()

		if self.lives <= 0:
			self.reset_game()
			return

		if self.basket.rect.colliderect(self.egg.rect):
			self.egg.reset_pos()
			self.score += 100
			self.hit_sound.play()
		if self.basket.rect.colliderect(self.shit.rect):
			self.shit.reset_pos()
			self.score -= 100
			self.lives -= 1
			self.hit_sound.play()
		if self.basket.rect.colliderect(self.golden_egg.rect):
			self.golden_egg.reset_pos()
			self.score += 500
			self.hit_sound.play()

		self.score = max(self.score, 0)

		self.chickens.update()
		self.basket.update()
		self.shit.update()
		self.egg.update()
		self.golden_egg.update()

		self.game.draw_text('Score '+ str(self.score), 35, self.game.WHITE, self.game.W, self.game.H - 55, centery=False, right=True)
		self.game.draw_text(' Lives '+ str(self.lives), 35, self.game.WHITE, 0, self.game.H - 55, centerx=False, centery=False)