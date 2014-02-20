from sympy import *
from sympy.geometry import *

class DataZone():

    def __init__ (self, code, name, polygon):
    	self.code = code
    	self.name = name
        self.polygon = polygon
        self.distance = 0

    def getCode(self):
    	return self.code

    def getName(self):
    	return self.name

    def getDistanceToPoint(self,point):
        self.distance = point.distance(self.polygon.centroid)
        return self.distance
        
    def getPolygon(self):
        return self.polygon