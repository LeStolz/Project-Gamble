import pygame
from Scenes import *
from Classes import *


class SpaceInvaderGameScene(GameScene):
	class Laser:
		def __init__(self, menu, x, y, img):
			self.menu = menu

			self.x = x
			self.y = y
			self.img = pygame.transform.scale(img, (160, 140))

			self.mask = pygame.mask.from_surface(self.img)


		def draw(self, window):
			window.blit(self.img, (self.x, self.y))


		def move(self, vel):
			self.y += vel


		def off_screen(self, height):
			return not(self.y <= height and self.y >= -140)


		def collision(self, obj):
			return self.menu.collide(self, obj)


	class Ship:
		def __init__(self, menu, x, y, health=100):
			self.menu = menu

			self.COOLDOWN = 20

			self.x = x
			self.y = y
			self.health = health
			self.ship_img = None
			self.laser_img = None
			self.lasers = []
			self.cool_down_counter = 0


		def draw(self, window):
			window.blit(self.ship_img, (self.x, self.y))
			for laser in self.lasers:
				laser.draw(window)


		def move_lasers(self, vel, obj):
			self.cooldown()
			for laser in self.lasers:
				laser.move(vel + 1)
				if laser.off_screen(self.menu.game.H):
					self.lasers.remove(laser)
				elif laser.collision(obj):
					obj.health -= 10
					self.lasers.remove(laser)


		def cooldown(self):
			if self.cool_down_counter >= self.COOLDOWN:
				self.cool_down_counter = 0
			elif self.cool_down_counter > 0:
				self.cool_down_counter += 1


		def shoot(self):
			if self.cool_down_counter == 0:
				laser = self.menu.Laser(self.menu, self.x, self.y, self.laser_img)
				self.lasers.append(laser)
				self.cool_down_counter = 1


		def get_width(self):
			return self.ship_img.get_width()


		def get_height(self):
			return self.ship_img.get_height()


	class Player(Ship):
		def __init__(self, menu, x, y, health=90):
			super().__init__(menu, x, y, health)

			self.score = 0
			self.ship_img = pygame.transform.scale(self.menu.game.space_invader_assets['PlayerShip'].image, (160, 140))
			self.laser_img = pygame.transform.scale(self.menu.game.space_invader_assets['PlayerLaser'].image, (160, 140))
			self.mask = pygame.mask.from_surface(self.ship_img)
			self.max_health = health


		def move_lasers(self, vel, objs):
			self.cooldown()
			for laser in self.lasers:
				laser.move(vel)
				if laser.off_screen(self.menu.game.H):
					self.lasers.remove(laser)
				else:
					for obj in objs:
						if laser.collision(obj):
							objs.remove(obj)
							self.menu.hit_sound.play()
							if laser in self.lasers:
								self.score += 50
								self.lasers.remove(laser)


		def draw(self, window):
			super().draw(window)
			self.healthbar(window)


		def healthbar(self, window):
			pygame.draw.rect(window, self.menu.game.RED, (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
			pygame.draw.rect(window, self.menu.game.GREEN, (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))


	class Enemy(Ship):
		def __init__(self, menu, x, y, color, health=100):
			super().__init__(menu, x, y, health)

			self.COLOR_MAP = {
				'Red': (self.menu.game.space_invader_assets['RedShip'].image, self.menu.game.space_invader_assets['RedLaser'].image),
				'Green': (self.menu.game.space_invader_assets['BlackShip'].image, self.menu.game.space_invader_assets['BlackLaser'].image),
				'Blue': (self.menu.game.space_invader_assets['BlueShip'].image, self.menu.game.space_invader_assets['BlueLaser'].image),
			}

			self.ship_img, self.laser_img = self.COLOR_MAP[color]
			self.ship_img = pygame.transform.scale(self.ship_img, (160, 140))
			self.laser_img = pygame.transform.scale(self.laser_img, (160, 140))
			self.mask = pygame.mask.from_surface(self.ship_img)


		def move(self, vel):
			self.y += vel


		def shoot(self):
			if self.cool_down_counter == 0:
				laser = self.menu.Laser(self.menu, self.x, self.y, self.laser_img)
				self.lasers.append(laser)
				self.cool_down_counter = 1


	def collide(self, obj1, obj2):
		offset_x = obj2.x - obj1.x
		offset_y = obj2.y - obj1.y
		return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


	def __init__(self, game, title):
		GameScene.__init__(self, game, title)

		self.laser_sound = pygame.mixer.Sound(self.game.space_invader_sfx['Laser'])
		self.hit_sound = pygame.mixer.Sound(self.game.space_invader_sfx['Hit'])

		self.BACKGROUND = pygame.transform.scale(self.game.space_invader_assets['Background'].image, (self.game.W, self.game.H))

		self.player = self.Player(self, self.game.W // 2 - 80, self.game.H - 200)

		self.level = 0

		self.enemies = []
		self.wave_length = 5
		self.enemy_vel = 2

		self.player_vel = 16
		self.laser_vel = 10


	def draw_options(self):
		self.game.display.blit(self.BACKGROUND, (0,0))

		for enemy in self.enemies:
			enemy.draw(self.game.display)

		self.player.draw(self.game.display)

		if self.lives <= 0 or self.player.health <= 0:
			self.reset_game()
			return

		self.score = self.player.score

		if len(self.enemies) == 0:
			self.level += 1
			self.wave_length += 5
			for i in range(self.wave_length):
				self.enemies.append(
					self.Enemy(self, random.randrange(50, self.game.W - 100), random.randrange(-1400, -140), random.choice(['Red', 'Blue', 'Green']))
				)

		if self.game.K_LEFT and self.player.x - self.player_vel > 0:
			self.player.x -= self.player_vel
		if self.game.K_RIGHT and self.player.x + self.player_vel + self.player.get_width() < self.game.W:
			self.player.x += self.player_vel
		if self.game.K_UP and self.player.y - self.player_vel > 0:
			self.player.y -= self.player_vel
		if self.game.K_DOWN and self.player.y + self.player_vel + self.player.get_height() + 15 < self.game.H:
			self.player.y += self.player_vel
		if self.game.K_SPACE:
			self.player.shoot()
			self.laser_sound.play()

		for enemy in self.enemies[:]:
			enemy.move(self.enemy_vel)
			enemy.move_lasers(self.laser_vel, self.player)

			if random.randrange(0, 2*60) == 1:
				enemy.shoot()

			if self.collide(enemy, self.player):
				self.player.health -= 25
				self.enemies.remove(enemy)
			elif enemy.y > self.game.H:
				self.lives -= 1
				self.enemies.remove(enemy)

		self.player.move_lasers(-self.laser_vel, self.enemies)

		self.game.draw_text('Score '+ str(self.score), 35, self.game.WHITE, self.game.W, self.game.H - 55, centery=False, right=True)
		self.game.draw_text(' Lives '+ str(self.lives), 35, self.game.WHITE, 0, self.game.H - 55, centerx=False, centery=False)