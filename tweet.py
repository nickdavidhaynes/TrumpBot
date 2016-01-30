import pickle
import tweepy
import tweetGenerator

tweet = tweetGenerator.make_tweet(size=100)

credentials_path = '/home/nick/side/twitter_api/credentials.pickle'
credentials = pickle.load(open(credentials_path, 'r'))

auth = tweepy.OAuthHandler(credentials['CONSUMER_KEY'], credentials['CONSUMER_SECRET'])
auth.set_access_token(credentials['ACCESS_KEY'], credentials['ACCESS_SECRET'])
api = tweepy.API(auth)

api.update_status(status=tweet)
