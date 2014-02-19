from sympy import *
from sympy.geomoetry import *

class Location():

	def __init__ (self, point):
		self.point = point

	def sortDataZones(self, zones, i, j):
		if (i < j):
			mid = ((i + j) / 2)
			sortDataZones(zones, i, mid)
			sortDataZones(zones, (mid + 1), j)
			merge(zones, i, mid, j)

	def merge(zones, i, mid, j):
		B = []
		k = i
		l = mid
		m = 0

		while (k <= mid && l <= j):
			if (self.point.distance(centroid(zones[k])) <= self.point.distance(centroid(zones[l]))):
				B[m] = zones[k]
				k = k + 1
			else:
				B[m] = zones[l]
				l = l + 1
			m = m + 1

		while (k <= mid):
			B[m] = A[k]
			k = k + 1
			m = m + 1

		while (l <= j) do:
			B[m] = A[l]
			l = l + 1
			m = m + 1

		for m in xrange(0, j - 1):
			zones[m + i] = B[m]
