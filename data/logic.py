import simplejson as json
import re
import math

from tweepy import *
from textblob import TextBlob
from time import sleep

from models import *

class TwitterAPI():

    def __init__(self):
        self.auth = OAuthHandler("To98JTvaCHrH1g2R4JtOg","D8sYsHmdvybnxCFNjJ32g0epoiIJmhLzwetkUUW0")
        self.api = API(self.auth)

    def getTweets(self, since_id=0):
        # Retrieves all tweets for the Edinburgh area
        return self.api.search(geocode='55.9507217407,-3.1923000813,20km', count=100, since_id=since_id)

    def tweetsToArray(self, tweets):
        # Converts tweepy objects into readable data
        tweet_dic = []

        max_id = 0

        for t in tweets:
            if (t.coordinates != None):
                tweet_dic.append({'user': t.user.screen_name, 'text': t.text, 'timestamp': t.created_at,
                                  'point': (t.coordinates['coordinates'][1], t.coordinates['coordinates'][0]),
                                  'id': int(t.id_str)})

                # If the ID of the tweet is greater than the current maximum ID, assign this ID to be the new
                # maximum ID
                if int(t.id_str) > max_id:
                    max_id = int(t.id_str)

        return {'max_id': max_id, 'tweets': tweet_dic}

    def get_tweets_array(self, since_id=0):
        tweets = self.getTweets(since_id)
        return self.tweetsToArray(tweets)

class SentimentAnalysis():

    def get_score(self, text):
        textblob = TextBlob(text)

        score = {
            'polarity': textblob.sentiment.polarity,
            'subjectivity': textblob.sentiment.subjectivity
        }

        return score

class DataCollection():

    def collect_tweets_loop(self, delay=30):
        if delay <= 5:
            print "Delay is too short, this is not safe as it will run over Twitter's API limit"
            return

        max_id = 0
        while True:
            max_id = self.collect_tweets(max_id)
            print "All current tweets pulled, sleeping for " + str(delay) + " seconds before pulling more"
            sleep(delay)

    def collect_tweets(self, start_from=0):
        # First we get some tweets
        t = TwitterAPI()
        s = SentimentAnalysis()

        print "Fetching tweets starting from ID: " + str(start_from)

        api_response = t.get_tweets_array(start_from)

        tweets = api_response['tweets']
        max_id = api_response['max_id']

        print "- Got " + str(len(tweets)) + " tweets"

        for x in tweets:
            print "-- Using tweet from user: " + x['user']
            # Add tweet to the database
            tweet = Tweet()
            tweet.sender = x['user']
            tweet.body = x['text']
            tweet.timestamp = x['timestamp']
            tweet.latitude = x['point'][0]
            tweet.longitude = x['point'][1]

            print "--- Performing Sentiment Analysis"
            y = s.get_score(x['text'])

            if y['polarity'] == 0:
                print "---- Sentiment Polarity was 0, Ignoring"
            else:
                print "--- Saving to Database"
                tweet.save()

                score = HappinessScore()
                score.tweet = tweet
                score.subjectivity = y['subjectivity']
                score.polarity = y['polarity']
                score.save()

        num_tweets = Tweet.objects.count()
        print "There are currently " + str(num_tweets) + " tweets in the database"

        return max_id


class DataZones():

    def import_data_zones(self):
        zone_json_path = raw_input("Enter path to GeoJSON file containing data zones followed by [Enter]: ")

        json_string = open(zone_json_path).read()

        geojson = json.loads(json_string)

        data_zones = geojson['features']

        for x in data_zones:
            print "Importing zone: {0}".format(x['properties']['DZ_CODE'])

            polygon = x['geometry']['coordinates']
            polygon_json = json.dumps(polygon)

            zone = DataZone()
            zone.code = x['properties']['DZ_CODE']
            zone.name = x['properties']['DZ_NAME']
            zone.polygon = polygon_json
            zone.save()

    def point_in_poly(self, point, poly):
        x = float(point[0])
        y = float(point[1])

        n = len(poly)
        inside = False

        while len(poly[0]) != 2:
            poly[0] = poly[0][0]

        p1x,p1y = poly[0]
        for i in range(n+1):
            p2x,p2y = poly[i % n]
            if y > min(p1y,p2y):
                if y <= max(p1y,p2y):
                    if x <= max(p1x,p2x):
                        if p1y != p2y:
                            xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                        if p1x == p2x or x <= xints:
                            inside = not inside
            p1x,p1y = p2x,p2y

        return inside

    def find_tweet_zones(self):
        print "Loading all tweets..."
        tweets = Tweet.objects.all()

        print "Loading all zones..."
        zones = DataZone.objects.all()

        num_tweets = len(tweets)
        num_zones = len(zones)

        print "There are {0} tweets and {1} zones".format(num_tweets, num_zones)

        tweet_counter = 0
        for tweet in tweets:
            tweet_counter += 1

            print "Checking tweet {0}/{1}...".format(tweet_counter, num_tweets)

            zone_counter = 0
            for zone in zones:
                zone_counter += 1

                polygon = json.loads(zone.polygon)[0]

                if self.point_in_poly([tweet.longitude, tweet.latitude], polygon):                    
                    # Insert the location into the database
                    x = TweetLocation()
                    x.zone = zone
                    x.tweet = tweet
                    x.save()

                    break

class TagCloud():
    def filter_body(self, body):      
        # Remove @ mentions
        body = re.sub(r'@(([A-z]|[0-9])*)', '', body)

        # Remove URLs
        body = re.sub(r'https?://\w*.\w*/\w*', '', body)

        # Remove non-alphanumeric characters
        body = re.sub(r"[^\w\s'#]*", '', body)

        return body

class CronGenerators():
    def generate_average_tweet_meta(self):
        """ Pull in all tweets and their regions and calculate the average happiness per region """
        data_zones = DataZone.objects.all()

        geo_json_tweets = {
            'type': 'FeatureCollection',
            'features': []
        }


        for data_zone in data_zones:
            # Get all tweets in this zone
            locations = TweetLocation.objects.filter(zone=data_zone)

            if len(locations) > 0:
                zone_code = data_zone.code

                average_score = 0
                for location in locations:
                    tweet = location.tweet
                    polarity = HappinessScore.objects.get(tweet=tweet).polarity
                    average_score += polarity

                    center = [tweet.longitude, tweet.latitude]

                average_score = average_score / len(locations)

                geo_json_tweet = {
                    'type': 'Feature',
                    'properties': {
                        'code': zone_code,
                        'happiness': average_score
                    },
                    'geometry': {
                        'type': 'Point',
                        'coordinates': center
                    }
                }

                geo_json_tweets['features'].append(geo_json_tweet)

        json_string = json.dumps(geo_json_tweets)

        cache_entry = Cache.objects.get(name='average_tweet_meta')
        cache_entry.content = json_string
        cache_entry.save()