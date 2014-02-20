import sys
import simplejson as json

if len(sys.argv) != 3:
    print "Usage: geojson_inject_scores.py [path to GeoJSON file] [path to JSON file containing scores]"
    exit()


def main():
    # Load geoJSON file
    geoJSON = open(sys.argv[1], 'r').read()
    geoJSON_data = json.loads(geoJSON)

    # Load score JSON file
    score_JSON = open(sys.argv[2], 'r').read()
    score_data = json.loads(score_JSON)

    # Go through the score JSON file and get the data into a nicer format
    simd_scores = {}
    for x in score_data:
        zone_id = x['Data Zone']

        try:
            simd_scores[zone_id] = x['Overall SIMD 2012 Rank']
        except KeyError:
            pass

    # Now go through the GeoJSON file and insert the scores
    n = 0
    for x in geoJSON_data['features']:
        code = x['properties']['DZ_CODE']

        try:
            x['properties']['SIMD_RANK'] = simd_scores[code]
        except KeyError:
            x['properties']['SIMD_RANK'] = -1

        geoJSON_data['features'][n] = x

        n += 1

    injected_geoJSON = json.dumps(geoJSON_data)

    print injected_geoJSON

if __name__ == "__main__":
    main()