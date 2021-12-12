import pygame
from random import *
import heapq
from Scenes import *
from Classes import *


class DeadlineRunnersGameScene(GameScene):
	class Object:
		def __init__(self, menu, x, y, w, h, image, vel):
			self.menu = menu

			self.x = x
			self.y = y
			self.w = w
			self.h = h

			self.vel = vel
			self.desired_vel = vel

			self.image = Surface(image)
			self.image.position(x, y)
			self.image.resize(w, h)


		def draw(self):
			self.menu.game.draw_surface(self.image)


		def update(self):
			self.x += self.vel
			self.vel += (self.desired_vel - self.vel) / self.menu.game.FPS

			self.image.rect.x = self.x


	class SpriteSheet(Object):
		def __init__(self, menu, x, y, w, h, image, vel, step_num, cooldown, w_or_h, scale):
			super().__init__(menu, x, y, w, h, image, vel)
			self.sheet = image
			self.step_num = step_num
			self.cooldown = cooldown
			self.scale = scale

			if w_or_h == 'w':
				self.cut_w_or_h = [self.w, 0]
			else:
				self.cut_w_or_h = [0, self.h]

			self.animation_list = []

			self.start_time = pygame.time.get_ticks()

			self.frame = 0

			self.load()


		def get(self, step):
			sheet = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
			sheet.blit(self.sheet, (0, 0), (self.cut_w_or_h[0] * step, self.cut_w_or_h[1] * step, self.w, self.h))
			sheet = pygame.transform.scale(sheet, (self.w * self.scale, self.h * self.scale))
			return sheet


		def load(self):
			for x in range (self.step_num):
				self.animation_list.append(self.get(x))

			self.w *= self.scale
			self.h *= self.scale
			self.image.resize(self.w, self.h)


		def update(self):
			super().update()
			if pygame.time.get_ticks() - self.start_time >= self.cooldown:
				self.frame = (self.frame + 1) % len(self.animation_list)
				self.start_time = pygame.time.get_ticks()


		def draw(self):
			self.menu.game.display.blit(self.animation_list[self.frame], (self.x, self.y))


	class Background:
		def __init__(self, menu, finish_line_y, finish_line_h):
			self.menu = menu

			self.background = [
				self.menu.Object(
					self.menu, 0, 0, self.menu.game.W, self.menu.game.H,
					self.menu.game.deadline_runners_assets[self.menu.character_set].image, -6
				),
				self.menu.Object(
					self.menu, self.menu.game.W, 0, self.menu.game.W, self.menu.game.H,
					self.menu.game.deadline_runners_assets[self.menu.character_set].image, -6
				),
			]
			self.background[1].image.image = pygame.transform.flip(self.background[1].image.image, True, False)

			self.active = False

			self.finish_line = self.menu.Object(
				self.menu,
				self.menu.game.W, finish_line_y, 60, finish_line_h,
				self.menu.game.deadline_runners_assets['FinishLine'].image, 0
			)


		def draw(self):
			for v in self.background:
				v.draw()

			if self.active or self.menu.track_length == 0:
				self.finish_line.draw()


		def update(self):
			if self.background[1].x <= 0:
				self.background[0].x = self.menu.game.W
				self.background[0], self.background[1] = self.background[1], self.background[0]

			for v in self.background:
				v.update()

			if self.active:
				for v in self.background:
					v.desired_vel = 0

				self.finish_line.vel = self.background[1].vel
				self.finish_line.desired_vel = self.background[1].desired_vel
				self.finish_line.update()


	class Obstacle(Object):
		def __init__(self, menu, car_id, x, y, w, h, image, vel, relative_vel):
			super().__init__(menu, x, y, w, h, image, vel)

			self.car_id = car_id
			self.active = False
			self.relative_vel = relative_vel


		def update(self):
			if self.active:
				super().update()

				self.vel = self.menu.background.background[0].vel + self.relative_vel

				if self.image.rect.colliderect(self.menu.cars[self.car_id].image.rect) and not self.menu.background.active:
					if self.relative_vel == 0:
						self.menu.cars[self.car_id].vel = 0
					else:
						self.menu.cars[self.car_id].vel = -1

				if self.x < -self.w:
					self.active = False


	class Point(Object):
		def __init__(self, menu, car_id, x, y, w, h, image, vel):
			super().__init__(menu, x, y, w, h, image, vel)

			self.car_id = car_id
			self.active = False


		def update(self):
			if self.active:
				super().update()

				self.vel = self.menu.background.background[0].vel

				if self.image.rect.colliderect(self.menu.cars[self.car_id].image.rect) and not self.menu.background.active:
					self.menu.cars[self.car_id].skills[self.menu.cars[self.car_id].title](*self.menu.cars[self.car_id].skill_arguments)
					self.menu.game.deadline_runners_sfx['Powerup'].play()
					self.active = False
					self.x = self.menu.game.W
					super().update()

				if self.x < -self.w:
					self.active = False


	class Skill:
		def __init__(self, menu, car):
			self.menu = menu
			self.car = car
			self.skill_active = False

			self.skills = {
				'Dang' : self.dang,
				'Khanh' : self.khanh,
				'Hoang' : self.hoang,
				'Triet' : self.triet,
				'Dat' : self.dat,

				'Alchemist' : self.alchemist,
				'Archer' : self.archer,
				'Knight' : self.knight,
				'Thief' : self.thief,
				'Warrior' : self.warrior,

				'Pufferfish' : self.speed,
				'Electriceel' : self.speed,
				'Squid' : self.speed,
				'Starfish' : self.speed,
				'Jellyfish' : self.speed,
			}


		def dang(self, active, in_effect=False):
			if not self.skill_active and not active and not in_effect:
				self.skill_active = True
				self.menu.SpriteSheet.__init__(self, self.menu, self.x, self.y - self.w // self.scale // 50, self.w // self.scale, self.h // self.scale,
					self.menu.game.deadline_runners_assets['DangSkill'].image, self.vel, self.step_num, self.cooldown, self.w_or_h, self.scale)
				for i in range(4):
					heapq.heappush(self.menu.event_queue, self.menu.Event(pygame.time.get_ticks() + i * self.cooldown, self.dang, (False, True)))
				heapq.heappush(self.menu.event_queue, self.menu.Event(pygame.time.get_ticks() + 4 * self.cooldown, self.dang, (True, True)))
			if self.skill_active and in_effect and not self.menu.background.active:
				for v in self.menu.cars:
					if v.title != self.title:
						v.desired_vel = min(v.desired_vel, self.menu.base_vel // 2)
			if self.skill_active and active:
				self.skill_active = False
				self.menu.SpriteSheet.__init__(self, self.menu, self.x, self.y + self.w // self.scale // 50, self.w // self.scale, self.h // self.scale,
					self.menu.game.deadline_runners_assets['Dang'].image, self.vel, self.step_num, self.cooldown, self.w_or_h, self.scale)


		def khanh(self, active, in_effect=False):
			if not self.skill_active and not active and not in_effect:
				self.skill_active = True
				self.menu.SpriteSheet.__init__(self, self.menu, self.x, self.y - self.w // self.scale // 75, self.w // self.scale, self.h // self.scale,
					self.menu.game.deadline_runners_assets['KhanhSkill'].image, self.vel, self.step_num, self.cooldown, self.w_or_h, self.scale)

				self.menu.skills = [
					self.menu.Obstacle(
						self.menu, x,
						self.menu.game.W, self.menu.cars[x].y + self.menu.cars[x].h // 2 - 90 // 2,
						110, 90,
						self.menu.game.deadline_runners_assets['KhanhEffect'].image, 0, 0
					) for x in range(0, len(self.menu.cars)) if self.menu.cars[x].title != self.title
				]
				for v in self.menu.skills:
					v.active = True

				heapq.heappush(self.menu.event_queue, self.menu.Event(pygame.time.get_ticks() + self.cooldown * 4, self.khanh, (True, True)))
			if self.skill_active and in_effect and not self.menu.background.active:
				self.desired_vel = (self.menu.base_vel + self.menu.base_bias)
			if self.skill_active and active:
				self.skill_active = False
				self.menu.SpriteSheet.__init__(self, self.menu, self.x, self.y + self.w // self.scale // 75, self.w // self.scale, self.h // self.scale,
					self.menu.game.deadline_runners_assets['Khanh'].image, self.vel, self.step_num, self.cooldown, self.w_or_h, self.scale)


		def triet(self, active, in_effect=False):
			if not self.skill_active and not active and not in_effect:
				self.skill_active = True
				self.menu.SpriteSheet.__init__(self, self.menu, self.x, self.y, self.w // self.scale, self.h // self.scale,
					self.menu.game.deadline_runners_assets['TrietSkill'].image, self.vel, self.step_num, self.cooldown, self.w_or_h, self.scale)
				for i in range(2, 5):
					heapq.heappush(self.menu.event_queue, self.menu.Event(pygame.time.get_ticks() + self.menu.base_acceleration_cooldown // i, self.triet, (False, True)))
				heapq.heappush(self.menu.event_queue, self.menu.Event(pygame.time.get_ticks() + self.menu.base_acceleration_cooldown, self.triet, (True, True)))
			if self.skill_active and in_effect and not self.menu.background.active:
				self.desired_vel = (self.menu.base_vel + self.menu.base_bias) * 2
			if self.skill_active and active:
				self.skill_active = False
				self.menu.SpriteSheet.__init__(self, self.menu, self.x, self.y, self.w // self.scale, self.h // self.scale,
					self.menu.game.deadline_runners_assets['Triet'].image, self.vel, self.step_num, self.cooldown, self.w_or_h, self.scale)


		def hoang(self, active, in_effect=False):
			if not self.skill_active and not active and not in_effect:
				self.skill_active = True
				self.menu.SpriteSheet.__init__(self, self.menu, self.x, self.y - self.w // self.scale // 75, self.w // self.scale, self.h // self.scale,
					self.menu.game.deadline_runners_assets['HoangSkill'].image, self.vel, self.step_num, self.cooldown, self.w_or_h, self.scale)
				for i in range(2, 5):
					heapq.heappush(self.menu.event_queue, self.menu.Event(pygame.time.get_ticks() + self.menu.base_acceleration_cooldown // i, self.hoang, (False, True)))
				heapq.heappush(self.menu.event_queue, self.menu.Event(pygame.time.get_ticks() + self.menu.base_acceleration_cooldown, self.hoang, (True, True)))
			if self.skill_active and in_effect and not self.menu.background.active:
				self.desired_vel = (self.menu.base_vel + self.menu.base_bias) // 2
				self.vel = (self.menu.base_vel + self.menu.base_bias) // 2
			if self.skill_active and active:
				self.skill_active = False
				self.menu.SpriteSheet.__init__(self, self.menu, self.x, self.y + self.w // self.scale // 75, self.w // self.scale, self.h // self.scale,
					self.menu.game.deadline_runners_assets['Hoang'].image, self.vel, self.step_num, self.cooldown, self.w_or_h, self.scale)


		def dat(self, active, in_effect=False):
			if not self.skill_active and not active and not in_effect:
				self.skill_active = True
				self.menu.SpriteSheet.__init__(self, self.menu, self.x, self.y, self.w // self.scale, self.h // self.scale,
					self.menu.game.deadline_runners_assets['DatSkill'].image, self.vel, self.step_num, self.cooldown, self.w_or_h, self.scale)
				heapq.heappush(self.menu.event_queue, self.menu.Event(pygame.time.get_ticks() + self.cooldown, self.dat_init, (True,)))
				for i in range(12):
					heapq.heappush(self.menu.event_queue, self.menu.Event(pygame.time.get_ticks() + i * self.cooldown, self.dat, (False, True)))
				heapq.heappush(self.menu.event_queue, self.menu.Event(pygame.time.get_ticks() + 12 * self.cooldown, self.dat_init, (False,)))
				heapq.heappush(self.menu.event_queue, self.menu.Event(pygame.time.get_ticks() + 13 * self.cooldown, self.dat, (True, True)))
			if self.skill_active and in_effect and not self.menu.background.active:
				for v in self.menu.cars:
					if v.title != self.title:
						v.desired_vel = 0
			if self.skill_active and active:
				self.skill_active = False
				self.menu.SpriteSheet.__init__(self, self.menu, self.x, self.y, self.w // self.scale, self.h // self.scale,
					self.menu.game.deadline_runners_assets['Dat'].image, self.vel, self.step_num, self.cooldown, self.w_or_h, self.scale)


		def dat_init(self, in_effect):
			if in_effect:
				self.menu.SpriteSheet.__init__(self, self.menu, self.x, self.y, self.w // self.scale, self.h // self.scale,
					self.menu.game.deadline_runners_assets['DatSkill1'].image, self.vel, self.step_num, self.cooldown, self.w_or_h, self.scale)
			else:
				self.menu.SpriteSheet.__init__(self, self.menu, self.x, self.y, self.w // self.scale, self.h // self.scale,
					self.menu.game.deadline_runners_assets['DatSkill'].image, self.vel, self.step_num, self.cooldown, self.w_or_h, self.scale)


		def alchemist(self, active, in_effect=False):
			if not self.skill_active and not active and not in_effect:
				self.skill_active = True
				self.menu.SpriteSheet.__init__(self, self.menu, self.x, self.y + 4, self.w // self.scale, self.h // self.scale,
					self.menu.game.deadline_runners_assets['AlchemistSkill2'].image, self.vel, self.step_num, self.main_cooldown / 2, self.w_or_h, self.scale * 0.9)
				self.play_sheet = True
				heapq.heappush(self.menu.event_queue, self.menu.Event(pygame.time.get_ticks() + 3 * self.main_cooldown / 2, self.init_alchemist, ()))
				for i in range(0, 5):
					heapq.heappush(self.menu.event_queue, self.menu.Event(pygame.time.get_ticks() + i * self.main_cooldown / 2, self.stop_alchemist, ()))
				for i in range(5, 9):
					heapq.heappush(self.menu.event_queue, self.menu.Event(pygame.time.get_ticks() + i * self.main_cooldown / 2, self.alchemist, (False, True)))
				heapq.heappush(self.menu.event_queue, self.menu.Event(pygame.time.get_ticks() + 9 * self.main_cooldown / 2, self.alchemist, (True, True)))
			if self.skill_active and in_effect and not self.menu.background.active:
				self.play_sheet = False
				self.desired_vel = (self.menu.base_vel + self.menu.base_bias) * 1.5
				self.vel = (self.menu.base_vel + self.menu.base_bias) * 1.5
			if self.skill_active and active:
				self.skill_active = False
				self.play_sheet = False
				self.desired_vel = (self.menu.base_vel + self.menu.base_bias // 2)
				self.vel = (self.menu.base_vel + self.menu.base_bias // 2)


		def init_alchemist(self):
			self.menu.SpriteSheet.__init__(self, self.menu, self.x, self.y - 4, self.w // self.scale, self.h // self.scale,
				self.menu.game.deadline_runners_assets['Alchemist'].image, self.vel, self.step_num, self.main_cooldown * 2, self.w_or_h, self.scale / 0.9)


		def stop_alchemist(self):
			self.desired_vel = self.menu.background.background[0].desired_vel
			self.vel = self.menu.background.background[0].vel


		def archer(self, active, in_effect=False):
			if not self.skill_active and not active and not in_effect:
				self.skill_active = True
				self.menu.SpriteSheet.__init__(self, self.menu, self.x, self.y + 8, self.w // self.scale, self.h // self.scale,
					self.menu.game.deadline_runners_assets['ArcherSkill2'].image, self.vel, self.step_num, self.cooldown, self.w_or_h, self.scale * 0.9)
				for i in range(4, 24):
					heapq.heappush(self.menu.event_queue, self.menu.Event(pygame.time.get_ticks() + i * self.cooldown, self.archer, (False, True)))
				heapq.heappush(self.menu.event_queue, self.menu.Event(pygame.time.get_ticks() + 24 * self.cooldown, self.archer, (True, True)))
			if self.skill_active and in_effect and not self.menu.background.active:
				self.active = False
				self.desired_vel = (self.menu.base_vel + self.menu.base_bias) // 2
				self.vel = (self.menu.base_vel + self.menu.base_bias) // 2
			if self.skill_active and active:
				self.active = True
				self.skill_active = False
				self.menu.SpriteSheet.__init__(self, self.menu, self.x, self.y - 8, self.w // self.scale, self.h // self.scale,
					self.menu.game.deadline_runners_assets['Archer'].image, self.vel, self.step_num, self.cooldown, self.w_or_h, self.scale / 0.9)


		def knight(self, active, in_effect=False):
			if not self.skill_active and not active and not in_effect:
				self.skill_active = True
				self.menu.SpriteSheet.__init__(self, self.menu, self.x, self.y + 12, self.w // self.scale, self.h // self.scale,
					self.menu.game.deadline_runners_assets['KnightSkill'].image, self.vel, self.step_num, self.main_cooldown / 2, self.w_or_h, self.scale * 0.9)
				self.play_sheet = True
				heapq.heappush(self.menu.event_queue, self.menu.Event(pygame.time.get_ticks() + 4 * self.main_cooldown / 2, self.init_knight, ()))
				for i in range(0, 4):
					heapq.heappush(self.menu.event_queue, self.menu.Event(pygame.time.get_ticks() + i * self.main_cooldown / 2, self.stop_knight, ()))
				heapq.heappush(self.menu.event_queue, self.menu.Event(pygame.time.get_ticks() + 4 * self.main_cooldown / 2, self.knight, (False, True)))
				heapq.heappush(self.menu.event_queue, self.menu.Event(pygame.time.get_ticks() + 4 * self.main_cooldown / 2, self.knight, (True, True)))
			if self.skill_active and in_effect and not self.menu.background.active:
				self.play_sheet = False
				self.menu.skills = [
					self.menu.Obstacle(
						self.menu, x,
						self.menu.game.W, self.menu.cars[x].y + self.menu.cars[x].h // 2 - 90 // 2,
						110, 90,
						pygame.transform.flip(self.menu.game.deadline_runners_assets['KnightEffect'].image, True, False), 0, -10
					) for x in range(0, len(self.menu.cars)) if self.menu.cars[x].title != self.title
				]
				for v in self.menu.skills:
					v.active = True
			if self.skill_active and active:
				self.skill_active = False
				self.play_sheet = False
				self.desired_vel = (self.menu.base_vel + self.menu.base_bias // 2)
				self.vel = (self.menu.base_vel + self.menu.base_bias // 2)


		def init_knight(self):
			self.menu.SpriteSheet.__init__(self, self.menu, self.x, self.y - 12, self.w // self.scale, self.h // self.scale,
				self.menu.game.deadline_runners_assets['Knight'].image, self.vel, self.step_num, self.main_cooldown * 2, self.w_or_h, self.scale / 0.9)


		def stop_knight(self):
			self.desired_vel = self.menu.background.background[0].desired_vel
			self.vel = self.menu.background.background[0].vel


		def thief(self, active, in_effect=False):
			if not self.skill_active and not active and not in_effect:
				self.skill_active = True
				self.menu.SpriteSheet.__init__(self, self.menu, self.x, self.y - 20, self.w // self.scale, self.h // self.scale,
					self.menu.game.deadline_runners_assets['ThiefSkill'].image, self.vel, self.step_num, self.main_cooldown / 2, self.w_or_h, self.scale * 1.2)
				self.play_sheet = True
				heapq.heappush(self.menu.event_queue, self.menu.Event(pygame.time.get_ticks() + 3 * self.main_cooldown / 2, self.init_thief, ()))
				for i in range(0, 3):
					heapq.heappush(self.menu.event_queue, self.menu.Event(pygame.time.get_ticks() + i * self.main_cooldown / 2, self.stop_thief, ()))

				heapq.heappush(self.menu.event_queue, self.menu.Event(pygame.time.get_ticks() + 3 * self.main_cooldown / 2, self.thief, (True, True)))
			if self.skill_active and in_effect and not self.menu.background.active:
				pass
			if self.skill_active and active:
				self.x += 100
				self.skill_active = False
				self.play_sheet = False
				self.desired_vel = (self.menu.base_vel + self.menu.base_bias // 2)
				self.vel = (self.menu.base_vel + self.menu.base_bias // 2)


		def init_thief(self):
			self.menu.SpriteSheet.__init__(self, self.menu, self.x, self.y + 20, self.w // self.scale, self.h // self.scale,
				self.menu.game.deadline_runners_assets['Thief'].image, self.vel, self.step_num, self.main_cooldown * 2, self.w_or_h, self.scale / 1.2)


		def stop_thief(self):
			self.desired_vel = self.menu.background.background[0].desired_vel
			self.vel = self.menu.background.background[0].vel


		def warrior(self, active, in_effect=False):
			if not self.skill_active and not active and not in_effect:
				self.skill_active = True
				self.menu.SpriteSheet.__init__(self, self.menu, self.x, self.y - 5, self.w // self.scale, self.h // self.scale,
					self.menu.game.deadline_runners_assets['WarriorSkill2'].image, self.vel, self.step_num, self.main_cooldown / 2, self.w_or_h, self.scale * 1.1)
				self.play_sheet = True
				heapq.heappush(self.menu.event_queue, self.menu.Event(pygame.time.get_ticks() + 4 * self.main_cooldown / 2, self.init_warrior, ()))
				for i in range(0, 4):
					heapq.heappush(self.menu.event_queue, self.menu.Event(pygame.time.get_ticks() + i * self.main_cooldown / 2, self.stop_warrior, ()))
				heapq.heappush(self.menu.event_queue, self.menu.Event(pygame.time.get_ticks() + 4 * self.main_cooldown / 2, self.warrior, (False, True)))
				heapq.heappush(self.menu.event_queue, self.menu.Event(pygame.time.get_ticks() + 4 * self.main_cooldown / 2, self.warrior, (True, True)))
			if self.skill_active and in_effect and not self.menu.background.active:
				self.play_sheet = False
				self.menu.skills = [
					self.menu.Obstacle(
						self.menu, x,
						self.menu.game.W, self.menu.cars[x].y + self.menu.cars[x].h // 2 - 90 // 2,
						180, 120,
						self.menu.game.deadline_runners_assets['WarriorEffect'].image, 0, -2.5
					) for x in range(0, len(self.menu.cars)) if self.menu.cars[x].title != self.title
				]
				for v in self.menu.skills:
					v.active = True
			if self.skill_active and active:
				self.skill_active = False
				self.play_sheet = False
				self.desired_vel = (self.menu.base_vel + self.menu.base_bias // 2)
				self.vel = (self.menu.base_vel + self.menu.base_bias // 2)


		def init_warrior(self):
			self.menu.SpriteSheet.__init__(self, self.menu, self.x, self.y + 5, self.w // self.scale, self.h // self.scale,
				self.menu.game.deadline_runners_assets['Warrior'].image, self.vel, self.step_num, self.main_cooldown * 2, self.w_or_h, self.scale / 1.1)


		def stop_warrior(self):
			self.desired_vel = self.menu.background.background[0].desired_vel
			self.vel = self.menu.background.background[0].vel


		def speed(self, active, in_effect=False):
			if not self.skill_active and not active and not in_effect:
				self.skill_active = True
				for i in range(2, 5):
					heapq.heappush(self.menu.event_queue, self.menu.Event(pygame.time.get_ticks() + self.menu.base_acceleration_cooldown // i, self.speed, (False, True)))
				heapq.heappush(self.menu.event_queue, self.menu.Event(pygame.time.get_ticks() + self.menu.base_acceleration_cooldown, self.speed, (True, True)))
			if self.skill_active and in_effect and not self.menu.background.active:
				self.desired_vel = (self.menu.base_vel + self.menu.base_bias) * 2
			if self.skill_active and active:
				self.skill_active = False


	class Car(SpriteSheet, Skill):
		def __init__(self, menu, x, y, w, h, title, vel, step_num, vic_step_num, cooldown, w_or_h, skill_arguments, bet, scale=1):
			menu.SpriteSheet.__init__(self, menu, x, y, w, h, menu.game.deadline_runners_assets[title].image, vel, step_num, cooldown, w_or_h, scale)
			menu.Skill.__init__(self, menu, self)

			self.w_or_h = w_or_h
			self.scale = scale

			self.title = title
			self.skill_arguments = skill_arguments
			self.bet = bet
			self.main_cooldown = cooldown

			self.active = True
			self.play_sheet = False

			self.has_label = False
			self.label_right = self.menu.game.W

			self.vic_step_num = vic_step_num
			self.finish_place = -1
			self.final_bet = 0
			self.final_label = ''


		def accelerate(self, desired_vel):
			self.desired_vel = desired_vel


		def update(self):
			if not self.play_sheet:
				self.cooldown = max(self.main_cooldown - (self.vel - self.menu.background.background[0].vel) * 50, 50)

			super().update()

			self.x = min(self.x, self.menu.game.W - self.w)
			self.x = max(self.x, 0)

			if self.finish_place == -1:
				if self.menu.background.active and self.desired_vel < 4:
					self.desired_vel = 4
					self.vel = 4

				if self.x >= self.menu.background.finish_line.x - self.w:
					self.desired_vel = 0.5
					self.menu.cars_finished.append(self)

					self.finish_place = len(self.menu.cars_finished)

					if self.finish_place <= 3:
						self.menu.score += self.bet * 2 // (2 ** (self.finish_place - 1))
						self.final_bet = self.bet * 2 // (2 ** (self.finish_place - 1))

						self.menu.SpriteSheet.__init__(self, self.menu, self.x, self.y, self.w // self.scale, self.h // self.scale,
							self.menu.game.deadline_runners_assets[self.title + 'Victory'].image,
							self.vel, self.vic_step_num, self.cooldown, self.w_or_h, self.scale)

						self.menu.game.ACCOUNT['Races'][0] = \
							'At ' \
							+ str((datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")) \
							+ (' Earned ' if self.menu.score >= 0 else ' Lost ') \
							+ str(abs(self.menu.score))

					place = ['0th', '1st', '2nd', '3rd', '4th', '5th']
					self.final_label = f'Earned {self.final_bet}    {place[self.finish_place]}'
				if self.active:
					if not self.has_label and self.label_right > self.x - 20:
						self.label_right = self.menu.game.draw_text(
							str(self.bet), 35, self.menu.game.WHITE,
							255 + self.menu.max_w + self.menu.max_text_w + self.menu.background.background[0].x,
							self.image.rect.centery
						).right
					else:
						self.has_label = True
						self.menu.game.draw_text(
							str(self.bet), 35, self.menu.game.WHITE,
							self.x - 20,
							self.image.rect.centery, right=True
						)
			else:
				if self.x >= self.menu.background.finish_line.x:
					self.desired_vel = 0.25

				self.menu.game.draw_text(
					self.final_label, 35, self.menu.game.GREEN if self.final_bet > 0 else self.menu.game.RED,
					self.x - 20,
					self.image.rect.centery, right=True, outline=False
				)


	class Event:
		def __init__(self, time, method, arguments):
			self.time = time
			self.method = method
			self.arguments = arguments


		def __lt__(self, next):
			return self.time < next.time


	def __init__(self, game, title):
		GameScene.__init__(self, game, title)

		self.CHARACTERS = {
			'Deadliners' : [
				self.Car(self, 25, self.game.H * 0.305, 800, 400,
					'Dang', 1, 2, 2, 500, 'w', (False,), 0, 0.4
				),
				self.Car(self, 25, self.game.H * 0.42, 800, 400,
					'Khanh', 1, 2, 2, 500, 'w', (False,), 0, 0.4
				),
				self.Car(self, 25, self.game.H * 0.535, 800, 400,
					'Triet', 1, 2, 2, 500, 'w', (False,), 0, 0.4
				),
				self.Car(self, 25, self.game.H * 0.66, 800, 400,
					'Hoang', 1, 2, 2, 500, 'w', (False,), 0, 0.4
				),
				self.Car(self, 25, self.game.H * 0.785, 800, 400,
					'Dat', 1, 2, 2, 500, 'w', (False,), 0, 0.4
				),
			],
			'Chivalry' : [
				self.Car(self, 25, self.game.H * 0.26, 600, 800,
					'Alchemist', 1, 4, 3, 400, 'w', (False,), 0, 0.25
				),
				self.Car(self, 25, self.game.H * 0.38, 600, 800,
					'Archer', 1, 4, 4, 400, 'w', (False,), 0, 0.25
				),
				self.Car(self, 25, self.game.H * 0.49, 600, 800,
					'Knight', 1, 4, 2, 400, 'w', (False,), 0, 0.25
				),
				self.Car(self, 25, self.game.H * 0.6, 600, 800,
					'Thief', 1, 4, 2, 400, 'w', (False,), 0, 0.25
				),
				self.Car(self, 25, self.game.H * 0.7, 600, 800,
					'Warrior', 1, 4, 2, 400, 'w', (False,), 0, 0.25
				),
			],
			'Aquatica' : [
				self.Car(self, 25, self.game.H * 0.125, 600, 800,
					'Pufferfish', 1, 2, 2, 600, 'w', (False,), 0, 0.35
				),
				self.Car(self, 25, self.game.H * 0.25, 600, 800,
					'Electriceel', 1, 2, 2, 600, 'w', (False,), 0, 0.35
				),
				self.Car(self, 25, self.game.H * 0.45, 800, 600,
					'Squid', 1, 2, 2, 600, 'h', (False,), 0, 0.35
				),
				self.Car(self, 25, self.game.H * 0.55, 800, 800,
					'Starfish', 1, 1, 1, 600, 'w', (False,), 0, 0.35
				),
				self.Car(self, 25, self.game.H * 0.75, 800, 600,
					'Jellyfish', 1, 2, 2, 600, 'h', (False,), 0, 0.3
				),
			],
		}

		self.qualities = {
			'Character set' : ['Chivalry', 'Deadliners', 'Aquatica'],
			'Track length' : ['Short', 'Medium', 'Long'],
		}

		self.advantages = {
			'Strength' : Surface(self.game.thumbnails_assets['Strength'].image),
			'Swiftness' : Surface(self.game.thumbnails_assets['Swiftness'].image),
			'Amulet' : Surface(self.game.thumbnails_assets['Amulet'].image),
			'Endurance' : Surface(self.game.thumbnails_assets['Endurance'].image),
		}

		count = 0
		for i, v in self.advantages.items():
			if self.game.ACCOUNT['Items'][i] > 0:
				v.resize(150, 150)
				v.position(self.game.W // 2 - 150 - 100 + 200 * (count - 1), self.game.H // 2 + 20 - 75)
				count += 1
			else:
				v.resize(0, 0)

		self.character_set = self.qualities['Character set'][self.game.ACCOUNT['Character set']]
		self.track_length = self.game.ACCOUNT['Track length']

		self.background = -1

		if self.character_set == 'Deadliners':
			self.background = self.Background(self, self.game.H * 0.36, self.game.H * 0.59)
		elif self.character_set == 'Aquatica':
			self.background = self.Background(self, 0, self.game.H)
		elif self.character_set == 'Chivalry':
			self.background = self.Background(self, self.game.H * 0.37, self.game.H * 0.557)

		self.cars = self.CHARACTERS[self.character_set][:]
		self.cars_finished = []
		self.max_w = self.cars[0].w
		self.max_text_w = 0

		for v in self.cars:
			self.max_w = max(self.max_w, v.w)
			self.max_text_w = max(self.max_text_w, self.game.draw_text(
				v.title, 35, self.game.WHITE, v.x + self.max_w + 25, v.y, centerx=False, centery=False, no_draw=True
			).w)

		for i, v in enumerate(self.cars):
			self.buttons[str(i) + 'Left'] \
				= Button(Surface(self.buttons_assets['ArrowBottom'].image), Surface(self.buttons_assets['ArrowLeft'].image))
			self.buttons[str(i) + 'Right'] \
				= Button(Surface(self.buttons_assets['ArrowBottom'].image), Surface(self.buttons_assets['ArrowRight'].image))

			self.buttons[str(i) + 'Left'].position(v.x + self.max_w + 25 + self.max_text_w + 15, v.y + v.h // 2 - 40)
			self.buttons[str(i) + 'Right'].position(v.x + self.max_w + 25 + self.max_text_w + 300, v.y + v.h // 2 - 40)

		self.buttons['Start Race'] = Button(
			Surface(self.buttons_assets['Bottom'].image), Surface(self.buttons_assets['DeadlineRunners'].image)
		)

		self.buttons['Start Race'].resize(self.game.W // 5, self.game.H // 6)
		self.buttons['Start Race'].position(self.game.W - 250 - self.game.W // 10, self.game.H // 2 - self.game.H // 12 + 20)

		self.object_sizes = []
		if self.character_set == 'Deadliners':
			self.objects = [
				'DeadlinersObstacle', 'DeadlinersMovingObstacle', 'DeadlinersPoint'
			]
			self.object_sizes = [
				(self.cars[0].w * 3, self.cars[0].h * 3), (self.cars[0].w, self.cars[0].h), (100, 100)
			]
		elif self.character_set == 'Aquatica':
			self.objects = ['AquaticaObstacle', 'AquaticaMovingObstacle', 'AquaticaPoint']
			self.object_sizes = [
				(self.cars[0].w * 6, self.cars[0].h * 2), (self.cars[0].w, self.cars[0].h), (50, 50)
			]
		elif self.character_set == 'Chivalry':
			self.objects = ['ChivalryObstacle', 'ChivalryMovingObstacle', 'ChivalryPoint']
			self.object_sizes = [
				(self.cars[0].w * 6, self.cars[0].h * 3), (self.cars[0].w, self.cars[0].h), (100, 100)
			]

		self.obstacles = [
			self.Obstacle(
				self, x,
				self.game.W, self.cars[x].y + self.cars[x].h // 2 - self.object_sizes[0][1] // 2,
				*self.object_sizes[0],
				self.game.deadline_runners_assets[self.objects[0]].image, 0, 0
			) for x in range(0, len(self.cars))
		]
		self.obstacles.extend([
			self.Obstacle(
				self, x,
				self.game.W, self.cars[x].y + self.cars[x].h // 2 - self.object_sizes[1][1] // 2,
				*self.object_sizes[1],
				self.game.deadline_runners_assets[self.objects[1]].image, 0, self.background.background[0].vel
			) for x in range(0, len(self.cars))
		])
		self.points = [
			self.Point(
				self, x,
				self.game.W, self.cars[x].y + self.cars[x].h // 2 - self.object_sizes[2][1] // 2,
				*self.object_sizes[2],
				self.game.deadline_runners_assets[self.objects[2]].image, 0
			) for x in range(0, len(self.cars))
		]
		self.skills = []

		self.event_queue = []
		heapq.heapify(self.event_queue)

		self.base_background_vel = -5
		self.base_vel = 1
		self.base_bias = 1
		self.base_acceleration_cooldown = 1000

		if self.track_length == 0:
			self.base_background_vel = 0
			self.base_vel = 3
			self.base_bias = 6
			self.base_acceleration_cooldown = 500
			self.background.finish_line.x = self.game.W - self.background.finish_line.image.rect.w
			self.background.finish_line.image.rect.x = self.game.W - self.background.finish_line.image.rect.w
		if self.track_length == 2:
			self.base_background_vel = -6
			self.base_vel = 0
			self.base_bias = 3
			self.base_acceleration_cooldown = 1000

		self.background.background[0].desired_vel = self.base_background_vel
		self.background.background[0].vel = self.base_background_vel
		self.background.background[1].desired_vel = self.base_background_vel
		self.background.background[1].vel = self.base_background_vel

		for v in self.cars:
			v.desired_vel = self.base_vel
			v.vel = self.base_vel

		self.starting = True
		self.starting_phase = 0
		self.race_finished = False
		self.temp_money = self.game.ACCOUNT["Money"]

		self.chosen_advantage = ''
		self.hover_advantage = ''


	def check_advantage(self):
		count = 0
		for i, v in self.advantages.items():
			if self.game.ACCOUNT['Items'][i] > 0:
				v.resize(150, 150)
				v.position(self.game.W // 2 - 150 - 100 + 200 * (count - 1), self.game.H // 2 + 20 - 75)
				count += 1
			else:
				v.resize(0, 0)

		for i, v in self.advantages.items():
			if self.game.ACCOUNT['Items'][i] > 0 and (i == self.chosen_advantage or v.rect.collidepoint(pygame.mouse.get_pos())):
				if v.rect.collidepoint(pygame.mouse.get_pos()):
					self.hover_advantage = i
				v.resize(v.rect.w + 50, v.rect.h + 50)
				v.position(v.rect.x - 25, v.rect.y - 25)

		if self.game.M_DOWN and self.hover_advantage != '' and self.game.ACCOUNT['Items'][self.hover_advantage] > 0:
			self.chosen_advantage = self.hover_advantage


	def start_gamble(self):
		if self.starting_phase == 0:
			self.game.draw_text('Place your bets', 45, self.game.GREEN, self.game.W // 2, 0, centery=False)
			self.game.draw_text('Start Race', 35, self.game.WHITE, self.game.W - 250, self.game.H // 2 - self.game.H // 12 - 30, centery=False)
			self.game.draw_text(
				f'Your money {self.temp_money}', 25, self.game.WHITE,
				self.cars[0].x + self.max_w + 25 + self.max_text_w + 205, self.cars[0].y - 25
			)

			for v in self.cars:
				self.game.draw_text(
					v.title, 35, self.game.WHITE, v.x + self.max_w + 25, v.y + v.h // 2, centerx=False
				)
				self.game.draw_text(
					str(v.bet), 35, self.game.WHITE, v.x + self.max_w + 25 + self.max_text_w + 205, v.y + v.h // 2
				)
		elif self.starting_phase == 1:
			self.check_advantage()

			self.game.draw_text('Choose your Advantage', 45, self.game.GREEN, self.game.W // 2, 0, centery=False)
			self.game.draw_text('Start Race', 35, self.game.WHITE, self.game.W - 250, self.game.H // 2 - self.game.H // 12 - 30, centery=False)

			for i, v in self.advantages.items():
				if self.game.ACCOUNT['Items'][i] > 0:
					self.game.draw_surface(v)


	def finish_gamble(self):
		self.race_finished = True
		heapq.heappush(self.event_queue, self.Event(pygame.time.get_ticks() + 6000, self.reset_game, ()))


	def use_amulet(self):
		for i, v in enumerate(self.cars):
			if v.bet > 0:
				for u in self.points:
					if u.car_id == i:
						u.active = True


	def use_swiftness(self):
		for v in self.cars:
			if v.bet > 0:
				v.vel = self.base_vel * 2


	def use_strength(self):
		for v in self.cars:
			if v.bet > 0:
				v.desired_vel = max(v.desired_vel, 1)
		heapq.heappush(self.event_queue, self.Event(pygame.time.get_ticks() + self.base_acceleration_cooldown, self.use_strength, ()))


	def use_endurance(self):
		for v in self.cars:
			if v.bet > 0:
				v.desired_vel = max(v.desired_vel, 0)
				v.vel = max(v.vel, 0)
		heapq.heappush(self.event_queue, self.Event(pygame.time.get_ticks() + self.base_acceleration_cooldown, self.use_endurance, ()))


	def check_button_input(self):
		super().check_button_input()

		if self.down_button_name in self.buttons.keys() and self.game.M_DOWN:
			true_down_button_name = self.down_button_name.replace('Left', '').replace('Right', '')

			if self.down_button_name == 'Start Race' and self.starting_phase == 0:
				self.starting_phase = 1

				self.buttons = {
					'Back' : Button(Surface(self.buttons_assets['ArrowBottom'].image), Surface(self.buttons_assets['ArrowLeft'].image))
				}
				self.buttons['Back'].resize(55, 55)
				self.buttons['Back'].position(0, 0)

				self.buttons['Start Race'] = Button(
					Surface(self.buttons_assets['Bottom'].image), Surface(self.buttons_assets['DeadlineRunners'].image)
				)

				self.buttons['Start Race'].resize(self.game.W // 5, self.game.H // 6)
				self.buttons['Start Race'].position(self.game.W - 250 - self.game.W // 10, self.game.H // 2 - self.game.H // 12 + 20)
			elif self.down_button_name == 'Start Race' and self.starting_phase == 1:
				self.score = self.temp_money - self.game.ACCOUNT["Money"]
				if self.chosen_advantage in self.game.ACCOUNT['Items'].keys():
					self.game.ACCOUNT['Items'][self.chosen_advantage] -= 1
				self.starting = False
				self.buttons = {
					'Back' : Button(Surface(self.buttons_assets['ArrowBottom'].image), Surface(self.buttons_assets['ArrowLeft'].image))
				}
				self.buttons['Back'].resize(55, 55)
				self.buttons['Back'].position(0, 0)

				self.accelerate_cars()

				if self.chosen_advantage == 'Amulet':
					self.use_amulet()
				if self.chosen_advantage == 'Swiftness':
					self.use_swiftness()
				if self.chosen_advantage == 'Strength':
					self.use_strength()
				if self.chosen_advantage == 'Endurance':
					self.use_endurance()

				self.game.ACCOUNT['Race Number'] += 1
				self.game.ACCOUNT['Races'].insert(
					0, 'At ' \
					+ str((datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")) \
					+ (' Earned ' if self.score >= 0 else ' Lost ') \
					+ str(abs(self.score))
				)
				if self.game.ACCOUNT['Race Number'] > 10:
					self.game.ACCOUNT['Race Number'] -= 1
					self.game.ACCOUNT['Races'].pop(-1)
				return

			if 'Left' in self.down_button_name:
				prev_bet = self.cars[int(true_down_button_name)].bet
				self.cars[int(true_down_button_name)].bet = (self.cars[int(true_down_button_name)].bet - 2000) % 22000
				if self.temp_money + prev_bet - self.cars[int(true_down_button_name)].bet >= 0:
					self.temp_money += prev_bet - self.cars[int(true_down_button_name)].bet
				else:
					self.cars[int(true_down_button_name)].bet = prev_bet
			elif 'Right' in self.down_button_name:
				prev_bet = self.cars[int(true_down_button_name)].bet
				self.cars[int(true_down_button_name)].bet = (self.cars[int(true_down_button_name)].bet + 2000) % 22000
				if self.temp_money + prev_bet - self.cars[int(true_down_button_name)].bet >= 0:
					self.temp_money += prev_bet - self.cars[int(true_down_button_name)].bet
				else:
					self.cars[int(true_down_button_name)].bet = prev_bet


	def accelerate_cars(self):
		min_x = self.cars[0].x
		max_x = self.cars[0].x

		for v in self.cars:
			min_x = min(min_x, v.x)
			max_x = max(max_x, v.x)

		if max_x > self.game.W - 600:
			self.background.active = True

			for v in self.cars:
				v.desired_vel -= self.background.background[1].vel
		else:
			heapq.heappush(self.event_queue, self.Event(pygame.time.get_ticks() + 2 * self.base_acceleration_cooldown, self.accelerate_cars, ()))

			for v in self.cars:
				bias = self.base_bias
				bias = bias + 1 if v.x <= min_x else bias
				bias = bias - 1 if v.x >= max_x else bias

				heapq.heappush(
					self.event_queue,
					self.Event(pygame.time.get_ticks(), v.accelerate, (max(v.desired_vel, random.random() * bias + self.base_vel),))
				)
				heapq.heappush(
					self.event_queue,
					self.Event(pygame.time.get_ticks() + self.base_acceleration_cooldown, v.accelerate, (self.base_vel,))
				)


	def process_event_queue(self):
		while len(self.event_queue) > 0 and self.event_queue[0].time <= pygame.time.get_ticks():
			self.event_queue[0].method(*(self.event_queue[0].arguments))
			heapq.heappop(self.event_queue)


	def process_obstacle(self):
		for v in self.obstacles:
			if not self.starting and not v.active and randint(0, 1000) == 0:
				v.x = self.game.W
				v.active = True


	def process_point(self):
		for v in self.points:
			if not self.starting and not v.active and randint(0, 1000) == 0:
				v.x = self.game.W
				v.active = True


	def draw_options(self):
		self.process_event_queue()
		if not self.background.active and not self.race_finished:
			self.process_obstacle()
			self.process_point()

		if not self.race_finished and len(self.cars_finished) == len(self.cars):
			self.race_finished = True
			heapq.heappush(self.event_queue, self.Event(pygame.time.get_ticks() + 4000, self.finish_gamble, ()))

		self.background.draw()

		for v in self.skills:
			v.draw()

		for i in range(len(self.cars)):
			if self.cars[i].active:
				self.cars[i].draw()
			if not self.race_finished:
				self.obstacles[i].draw()
				self.obstacles[len(self.cars) + i].draw()
				self.points[i].draw()

		if self.lives <= 0:
			self.reset_game()
			return

		if self.starting:
			self.start_gamble()
			self.draw_buttons()
			return

		self.background.update()

		for v in self.obstacles:
			v.update()

		for v in self.points:
			v.update()

		for v in self.cars:
			v.update()

		for v in self.skills:
			v.update()

		self.draw_buttons()