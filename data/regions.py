from sympy import *
from sympy.geometry import *

class DataZones():

    def __init__ (self, polygons):
        self.polygons = polygons

    def sortDataZones(self, point):
        return DataZones(sorted(self.polygons, key = point.distance(polygon.centroid)))