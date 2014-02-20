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
        # Check the number of decimal places to see if we want the tweet or not
        num_decimal_places_latitude = len(str(x.tweet.latitude).split('.')[1])
        num_decimal_places_longitude = len(str(x.tweet.longitude).split('.')[1])

        if num_decimal_places_latitude < 7 or num_decimal_places_longitude < 7:
            continue

        geo_json_tweet = {
            'type': 'Feature',
            'properties': {
                'id': x.tweet.id,
                'happiness': x.polarity
            },
            'geometry': {
                'type': 'Point',
                'coordinates': [x.tweet.longitude, x.tweet.latitude]
            },
            'jobby': {
                'latlen': num_decimal_places_latitude,
                'lonlen': num_decimal_places_longitude
            }
        }

        geo_json_tweets['features'].append(geo_json_tweet)

    return HttpResponse(json.dumps(geo_json_tweets, use_decimal=True), content_type='application/json')


def get_tweet(request, tweet_id):
    tweet = Tweet.objects.get(id=tweet_id)

    tweet_dict = {
        'id': tweet.id,
        'user': tweet.sender,
        'body': tweet.body,
        'timestamp': tweet.timestamp.strftime("%Y-%m-%d %H:%M:%S")
    }

    return HttpResponse(json.dumps(tweet_dict), content_type='application/json')
