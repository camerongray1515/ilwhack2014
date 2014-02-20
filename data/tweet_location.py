from sympy import *
from sympy.geometry import *
from data_zones import *

class Location():

    def __init__ (self, point):
        self.point = point

    def pointDataZone(self, zones):
        sorted_zones = zones.sortDataZones(self.point)
        
        for z in sorted_zones:
            if z.polygon.encloses_point(self.point):
                return z.code