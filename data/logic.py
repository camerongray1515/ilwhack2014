from tweepy import *
from textblob import TextBlob
from time import sleep

from models import Tweet, HappinessScore

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