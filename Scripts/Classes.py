from math import sqrt
from math import ceil


class Vector:
	def __init__(self, x=0, y=0, rect=-1):
		if rect != -1:
			x = rect.x
			y = rect.y

		self.x = x
		self.y = y


	def length(self):
		return sqrt(self.x ** 2 + self.y ** 2)


	def normalize(self):
		if self.length() > 1:
			self.x = ceil(self.x / self.length()) - (self.x < 0)
			self.y = ceil(self.y / self.length()) - (self.y < 0)

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
	def __init__(self, x, y, r, w, h, drawn=False):
		self.Image = -1
		self.Rect = -1

		self.x = x	# x coordinate
		self.y = y	# y coordinate
		self.r = r	# rotation
		self.w = w	# width
		self.h = h	# height
		self.drawn = drawn


	def init_Image(self, Image):
		self.Image = Image


	def init_Rect(self, Rect):
		self.Rect = Rect
