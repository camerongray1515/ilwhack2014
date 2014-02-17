from tweepy import *

class TwitterAPI():

    def __init__ (self):
        self.auth = OAuthHandler("To98JTvaCHrH1g2R4JtOg","D8sYsHmdvybnxCFNjJ32g0epoiIJmhLzwetkUUW0")
        self.api = API(self.auth)

    def getTweets(self):
        "Retrieves all tweets for the Edinburgh area"
        return self.api.search(geocode = "55.9507217407,-3.1923000813,20km", rpp = "10000")

    def tweetsToArray(self, tweets):
        "Converts tweepy objects into readable data"
        tweet_dic = [] 

        for t in tweets:
            if (t.coordinates != None):
                tweet_dic.append({'user': t.user.screen_name, 'text': t.text, 'timestamp': t.created_at, 'coordinates': t.coordinates})
            else:
                pass

        return tweet_dic

    def get_tweets_array(self):
        tweets = self.getTweets()
        return self.tweetsToArray(tweets)