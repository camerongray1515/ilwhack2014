import simplejson as json

from django.shortcuts import render
from django.http import HttpResponse
from data.models import *

def get_tweet_meta(request):
    # Todo: Add tweet limit
    raw_data = HappinessScore.objects.all()

    geo_json_tweets = {
        'type': 'FeatureCollection',
        'features': []
    }
    for x in raw_data:
        geo_json_tweet = {
            'type': 'Feature',
            'properties': {
                'id': x.tweet.id,
                'happiness': x.polarity
            },
            'geometry': {
                'type': 'Point',
                'coordinates': [x.tweet.longitude, x.tweet.latitude]
            }
        }

        geo_json_tweets['features'].append(geo_json_tweet)

    return HttpResponse(json.dumps(geo_json_tweets, use_decimal=True), mimetype='application/json')