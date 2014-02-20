""" This script takes in a GeoJSON file and a CSV file that maps region IDs to their names.  It then returns a GeoJSON
    file with the names inserted.  Names that already exist in the GeoJSON file will be overwritten """

import sys
import json
import csv

if len(sys.argv) != 3:
    print "Usage: geojson_names.py [path to GeoJSON file] [path to names CSV file]"
    exit()

def main():
    # print "Opening GeoJSON file..."
    json_string = open(sys.argv[1], 'r').read()

    # print "Decoding GeoJSON file..."
    data = json.loads(json_string)

    region_names = {}

    # print "Reading CSV file..."
    with open(sys.argv[2], 'rb') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            components = row[1].split('-')
            name = components[-1].strip()
            region_names[row[0]] = name

    num_polygons = len(data['features'])
    idx=0
    for polygon in data['features']:
        # print "Processing region: {0}/{1}".format(idx+1, num_polygons)
        try:
            polygon['properties']['DZ_NAME'] = region_names[polygon['properties']['DZ_CODE']]
        except IndexError:
            polygon['properties']['DZ_NAME'] = "Not available"

        data['features'][idx] = polygon

        idx += 1

    new_json = json.dumps(data)

    print new_json


if __name__ == "__main__":
    main()