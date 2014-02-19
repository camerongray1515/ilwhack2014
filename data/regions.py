from sympy import *
from sympy.geometry import *

class Region():

	def __init__ (self, points):
		self.points = points

	def getPoints(self):
		return self.points

	def getLines(self):
		lines = []
		n = 0

		for p in self.points:
			if (n < (len(self.points) - 2)):
				l = Line(Point(self.points[n]),Point(self.points[n + 1]))
				lines = lines + [l]
			else:
				l = Line(Point(self.points[n]),Point(self.points[0]))
				lines = lines + [l]
				return lines
			n = n + 1