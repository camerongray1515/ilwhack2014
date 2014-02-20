from sympy import *
from sympy.geometry import *

class DataZone():

    def __init__ (self, code, name, polygon):
    	self.code = code
    	self.name = name
        self.polygon = polygon
        self.distance = 0

    def getCode(self):
    	# returns area code
    	return self.code

    def getName(self):
    	# returns area name
    	return self.name

    def getDistanceToPoint(self,point):
    	# calculates distance between the centre of a data zone and a point
        self.distance = point.distance(self.polygon.centroid)
        return self.distance
        
    def getPolygon(self):
    	# returns the corresponding polygon
        return self.polygon