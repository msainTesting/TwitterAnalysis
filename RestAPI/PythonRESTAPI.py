import tweepy#import the tweepy library to be able to use it
import json #import the json library
#import config # the config file is imported, which contains the Twitter API keys and tokens 

API_KEY = 'ViPCPxiSa7IoB0aJmibSoVkBV'  # identifies the application
API_SECRET = 's1lgLWFvnPL3jMOgaM3OC6lzKUf5fLkxfqYZUdq4wPG95IkEjt'  # application password

TOKEN_KEY = '1453689246439591940-qGz4YpIZj5F00k4hqgtMza8PAE2BFI'  # identifies the user
TOKEN_SECRET = 'm6FDrQ1QYhj1Nj5RTKSgxmBop7goXgDSzJjUA0Vzzq1Pi'  # user password

#The OAuth handler is initialised to access the Twitter API, since it is necessary for developers to identify themselves. The access token are set for the initialised OAuth handler.
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(TOKEN_KEY, TOKEN_SECRET)


#to access the Twitter API, the tweepy method is used. The wait_on_rate_limit is set to true, so that Twitter's API rate limit is respected.
api = tweepy.API(auth, wait_on_rate_limit=True)

#hashtag, that is being searched for is defined; alternatively the following can be used to filter out retweets query = '#vegan -filter:retweets'
query = '#cop26'

#cursor method of Tweepy is used by utilising the search method. The count is set to 100 (max.limit) and the tweet_mode is extended, so that Tweets are not truncated. Pages is a set of 15 tweets
cursor = tweepy.Cursor(api.search_tweets, q=query, lang="en", count=10, tweet_mode='extended').pages()

# the for loop iterates through the pages and for each page the second for loop iterates through the items and saves them in a list
for page in cursor:
    tweets = []
    for item in page:
        tweets.append(item._json)

#tweets list is dumped into a new JSON file 
with open('DMMD.json', 'w') as outfile:
    json.dump(tweets,outfile)


