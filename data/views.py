import simplejson as json

from django.shortcuts import render, render_to_response
from django.http import HttpResponse

from data.models import *
from data.logic import *

from pytagcloud import create_html_data, make_tags, LAYOUT_HORIZONTAL, LAYOUTS
from pytagcloud.lang.counter import get_tag_counts
from pytagcloud.colors import COLOR_SCHEMES


def get_tweet_meta(request):
    raw_data = HappinessScore.objects.all()

    geo_json_tweets = {
        'type': 'FeatureCollection',
        'features': []
    }

    n = 0
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
            }
        }

        geo_json_tweets['features'].append(geo_json_tweet)

        if n == 50:
            break

        n += 1

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

def get_tag_cloud(request, region_code):
    # Get all tweets in the region
    data_zone = DataZone.objects.get(code=region_code)
    tweet_locations = TweetLocation.objects.filter(zone=data_zone)

    body_text = ''

    for x in tweet_locations:
        body_text += x.tweet.body + ' '

    tc = TagCloud()
    body_text = tc.filter_body(body_text)

    if body_text.strip() == '':
        body_text = "Region Empty"

    tags = make_tags(get_tag_counts(body_text)[:50], maxsize=50, colors=COLOR_SCHEMES['audacity'])
    data = create_html_data(tags, (700,350), layout=LAYOUT_HORIZONTAL, fontname='PT Sans Regular')

    context = {}
        
    tags_template = '<li class="cnt" style="top: %(top)dpx; left: %(left)dpx; height: %(height)dpx;"><a class="tag %(cls)s" href="#%(tag)s" style="top: %(top)dpx;\
    left: %(left)dpx; font-size: %(size)dpx; height: %(height)dpx; line-height:%(lh)dpx;">%(tag)s</a></li>'
    
    context['tags'] = ''.join([tags_template % link for link in data['links']])
    context['width'] = data['size'][0]
    context['height'] = data['size'][1]
    context['css'] = "".join("a.%(cname)s{color:%(normal)s;}a.%(cname)s:hover{color:%(hover)s;}" % {'cname':k, 'normal': v[0], 'hover': v[1]} for k,v in data['css'].items())

    return render_to_response('tag_cloud.html', {'tags': context['tags'], 'css': context['css']})
