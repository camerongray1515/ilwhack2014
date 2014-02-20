from data_zone import *

class DataZones():

	def __init__(self,data_zones):
		self.data_zones = data_zones

	def sortDataZones(self, point):
		for z in self.data_zones:
			z.distance = z.getDistanceToPoint(point)

		sorted_zones = sorted(self.data_zones, key = lambda x : x.distance)

		return sorted_zones