import pygame
from math import sqrt


class Vector:
	def __init__(self, x, y):
		self.x = x
		self.y = y


	def length(self):
		return sqrt(self.x ** 2 + self.y ** 2)


	def normalize(self):
		if self.length() > 0:
			self.x = round(self.x / self.length())
			self.y = round(self.y / self.length())

		return self


	def __add__(self, o):
		return Vector(self.x + o.x, self.y + o.y)


	def __sub__(self, o):
		return Vector(self.x - o.x, self.y - o.y)


	def __mul__(self, o):
		return self.x * o.y - self.y * o.x


	def __mul__(self, o):
		return Vector(self.x * o, self.y * o)


	def __truediv__(self, o):
		return self.x * o.x + self.y * o.y


class Surface:
	def __init__(self, image, rect=-1):
		if rect == -1:
			rect = image.get_rect(x=0, y=0)

		self.image = image
		self.rect = rect


	def position(self, x, y):
		self.rect.x = x
		self.rect.y = y


	def rotate(self, r):
		self.image = pygame.image.rotate(self.image, r)


	def resize(self, w, h):
		self.rect.w = w
		self.rect.h = h

		self.image = pygame.transform.scale(self.image, (self.rect.w, self.rect.h))


class Button:
	def __init__(self, bottom, top, text=''):
		self.bottom = bottom
		self.top = top
		self.text = text

		self.top_normal_y = self.top.rect.y


	def position(self, x, y):
		self.bottom.position(x, y)
		self.top.position(x, y)

		self.top_normal_y = self.top.rect.y


	def rotate(self, r):
		self.bottom.rotate(r)
		self.top.rotate(r)


	def resize(self, w, h):
		self.bottom.resize(w, h)
		self.top.resize(w, h)


	def normal(self):
		self.top.rect.y = self.top_normal_y


	def hover(self):
		self.top.rect.y = self.top_normal_y + self.top.rect.h * 0.04


	def up(self):
		self.top.rect.y = self.top_normal_y + self.top.rect.h * 0.08


	def down(self):
		self.top.rect.y = self.top_normal_y + self.top.rect.h * 0.11