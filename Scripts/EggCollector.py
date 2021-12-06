import pygame
from Scenes import *
from Classes import *


class EggCollectorScene(MenuScene):
	class Gio():
		def __init__(self, menu):
			self.menu = menu

			self.x = 100
			self.y = 410

			self.surface = self.menu.game.egg_collector_assets['Basket'].image
			self.rect = self.surface.get_rect()
			self.rect.w -= 40
			self.rect.h -= 80


		def draw(self):
			self.menu.game.display.blit(self.surface, (self.x, self.y))


		def update(self, moveLeft, moveRight):
			if moveLeft == True:
				self.x -= 15
			if moveRight == True:
				self.x += 15
			if self.x + 130 > 700:
				self.x = 700 - 130
			if self.x < 0:
				self.x = 0

			self.rect.x = self.x +20
			self.rect.y = self.y +20


	class Day():
		def __init__(self, menu):
			self.menu = menu

			self.x = 0
			self.y = 30

			self.surface = self.menu.game.egg_collector_assets['Chicken'].image


		def draw(self):
			self.menu.game.display.blit(self.surface, (self.x, self.y))


	class Trung():
		def __init__(self, menu):
			self.menu = menu

			self.surface = self.menu.game.egg_collector_assets['Egg'].image
			self.rect = self.surface.get_rect()
			self.rect.w -= 23
			self.rect.h -= 53
			self.x = random.choice([120,360,600])
			self.y = 110


		def draw(self):
			self.menu.game.display.blit(self.surface, (self.x, self.y))


		def reset_pos(self):
			self.x = random.choice([130, 360, 600])
			self.y = 110


		def update(self): #hàm update chuyển động của trung
			if self.y < 500: #nếu vẫn chưa rơi khỏi màn hình
				self.y += 5 #tăng y thêm 1, đồng nghĩa với trung rơi xuống 1
			else: #nếu y đã lớn hơn chiều cao màn hình
				self.reset_pos() #
			self.rect.x = self.x+15
			self.rect.y = self.y+35


	class Shit():
		def __init__(self, menu):
			self.menu = menu

			self.surface = self.menu.game.egg_collector_assets['Shit'].image
			self.rect = self.surface.get_rect()
			self.rect.w -= 32
			self.rect.h -= 50

			self.trung = self.menu.Trung(self.menu)

			if self.trung.x == 120 :
				self.x = random.choice([360,600])
			if self.trung.x == 360 :
				self.x = random.choice([120,600])
			if self.trung.x == 600 :
				self.x = random.choice([360,120])

			self.y = 110


		def draw(self):
			self.menu.game.display.blit(self.surface, (self.x, self.y))


		def reset_pos(self): #hàm reset vị trí của ball
			if self.trung.x == 120 :
				self.x = random.choice([360,600])
			if self.trung.x == 360 :
				self.x = random.choice([120,600])
			if self.trung.x == 600 :
				self.x = random.choice([360,120])
			self.y = 110


		def update(self): #hàm update chuyển động của trung
			if self.y < 500: #nếu vẫn chưa rơi khỏi màn hình
				self.y += 9 #tăng y thêm 1, đồng nghĩa với trung rơi xuống 1
			else: #nếu y đã lớn hơn chiều cao màn hình
				self.reset_pos() #
				self.menu.soshit += 1
			self.rect.x = self.x+20
			self.rect.y = self.y+30


	class Trungvang():
		def __init__(self, menu):
			self.menu = menu

			self.surface = self.menu.game.egg_collector_assets['GoldenEgg'].image
			self.rect = self.surface.get_rect()
			self.rect.w -= 23
			self.rect.h -= 53
			self.flag = False

			self.trung = self.menu.Trung(self.menu)

			if self.trung.x == 120 :
				self.x = random.choice([360,600])
			if self.trung.x == 360 :
				self.x = random.choice([120,600])
			if self.trung.x == 600 :
				self.x = random.choice([360,120])

			self.y = 110


		def draw(self):
			self.menu.game.display.blit(self.surface, (self.x, self.y))


		def reset_pos(self):
			#noise.play()
			self.x = random.choice([130, 360, 600])  #vị trí x ngẫu nhiên
			self.y = 110


		def update(self): #hàm update chuyển động của trung
			if self.menu.soshit % 10 == 0:
				self.flag = True

			if self.flag:
				if self.y < 500: #nếu vẫn chưa rơi khỏi màn hình
					self.y += 5 #tăng y thêm 1, đồng nghĩa với trung rơi xuống 1
				else: #nếu y đã lớn hơn chiều cao màn hình
					flag = False
					self.reset_pos()

				self.rect.x = self.x+15
				self.rect.y = self.y+35
			else:
				self.x = -100
				self.y = -100


	def __init__(self, game, title):
		MenuScene.__init__(self, game, title)

		self.die = 0
		self.soshit = 0

		self.shit = self.Shit(self)
		self.day = self.Day(self)
		self.gio = self.Gio(self)
		self.trung = self.Trung(self)
		self.trungvang = self.Trungvang(self)

		self.moveLeft = False
		self.moveRight = False
		self.score  = -10


	def draw_options(self):
		self.game.draw_text(self.title, 45, self.game.WHITE, self.game.W // 2, 0, centery=False)

		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					moveLeft = True
				if event.key == pygame.K_RIGHT:
					moveRight = True

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT:
					moveLeft = False
				if event.key == pygame.K_RIGHT:
					moveRight = False

		if (self.gio.rect.colliderect(self.trung.rect)):
			self.trung.reset_pos()
			self.score = self.score + 5
		if (self.gio.rect.colliderect(self.shit.rect)):
			self.shit.reset_pos()
			self.score = self.score - 5
			self.die += 1
		if (self.gio.rect.colliderect(self.trungvang.rect)):
			self.trungvang.x=-100
			self.trungvang.y=-100
			self.score = self.score + 10

		if self.die == 6:
			self.game.switch_scene(self.title, 'Minigame')

		self.game.draw_text(str(self.score), 35, self.game.WHITE, self.game.W, 0, centery=False, right=True)

		self.shit.draw()
		self.trung.draw()
		self.day.draw()
		self.gio.draw()
		self.trungvang.draw()
		self.gio.update(self.moveLeft, self.moveRight)
		self.trung.update()
		self.shit.update()
		self.trungvang.update()