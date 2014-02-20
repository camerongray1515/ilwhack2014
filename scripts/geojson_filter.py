""" This script takes in a GeoJSON file and a set of 4 coordinates.  It will then return a GeoJSON file with only the
 polygons that lie entirely inside the box made by the 4 coordinates given """

import sys
import string
import json

if len(sys.argv) != 6:
    print "Usage: geojson_filter.py [path to GeoJSON file] [top] [bottom] [right] [left]"
    exit()

def main():
    box = {
            'top': float(sys.argv[2]),
            'bottom': float(sys.argv[3]),
            'right': float(sys.argv[4]),
            'left': float(sys.argv[5])
        }

    # print box

    # print "Opening file..."
    json_string = open(sys.argv[1], 'r').read()

    # print "Decoding JSON..."
    data_full = json.loads(json_string)
    data = data_full['features']
    num_polygons = len(data)

    polygons_in_area = []

    # print "Found {0} polygons".format(num_polygons)

    n = 1
    for polygon in data:
        # print "Checking polygon {0}/{1}".format(n, num_polygons)
        n += 1

        loop_variable = polygon['geometry']['coordinates']

        while type(loop_variable[0]) is list and len(loop_variable[0]) != 2:
            loop_variable = loop_variable[0]

        for coordinate in loop_variable:
            if is_point_inside_box(coordinate, box):
                polygons_in_area.append(polygon)
                break

    # print "{0} polygons left".format(len(polygons_in_area))

    data_full['features'] = polygons_in_area
    filtered_json = json.dumps(data_full)

    print filtered_json

def is_point_inside_box(point, box):
    # Check if it is above or below box
    if point[1] > box['top'] or point[1] < box['bottom']:
        return False

    # Check if it is to right of
    if point[0] < box['right'] or point[0] > box['left']:
        return False

    return True

if __name__ == "__main__":
    main()