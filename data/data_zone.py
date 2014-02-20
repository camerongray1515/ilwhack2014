from sympy import *
from sympy.geometry import *

class DataZone():

    def __init__ (self, polygon):
        self.polygon = polygon
        self.distance = 0

    def getDistanceToPoint(self,point):
        self.distance = point.distance(self.polygon.centroid)
        return self.distance
        
    def getPolygon(self):
        return self.polygon