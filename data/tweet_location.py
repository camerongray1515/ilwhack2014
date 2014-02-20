from sympy import *
from sympy.geometry import *
from regions import *

class Location():

    def __init__ (self, point):
        self.point = point

    def pointDataZone(self, zones):
        sorted_zones = zones.sortDataZones(self.point)
        n = 0

        for z in sorted_zones.polygons:
            if sorted_zones.polygons[n].encloses_point(self.point):
                return sorted_zones.polygons[n]
            else:
                n = n + 1