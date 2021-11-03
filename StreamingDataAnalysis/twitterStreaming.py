import tweepy #import tweepy library
#import config #  the config file is imported, which contains the Twitter API keys and tokens
import json #import the json library
import warnings
import json
from StreamingDataAnalysis import config
from StreamingDataAnalysis.accessAuthAPI import getStreamingAuth
warnings.filterwarnings('ignore')

#both variables are used to automatically end the stream after 10,000 tweets. Tweet_count is the count variable and n_tweets is the limiter.
tweet_count = 0
n_tweets = 10

# the list, where the streamed tweets need to be collected and stored in, is generated
tweets_list = []

# overwriting the MyStreamListener class from the Tweepy library to adapt to the use case
class MyStreamListener(tweepy.StreamListener):
   # overwrite of on_data method
    def on_data(self,status):
        #global variables are defined so that they're accessible within the on_data method
        global tweet_count
        global n_tweets
        global tweets_list
        global myStream
        # as long as limiter variable is not reached, the tweets will be appended to a json list
        if tweet_count < n_tweets:
            tweets_list.append(json.loads(status))
            tweet_count += 1 # count variable is always extended by one, as long as limiter is not reached
            print(tweet_count) # to track the progress of the stream in the terminal, the tweet count is printed out
            with open('data/streaming_data_analysis.json', 'w') as outfile:
                json.dump(tweets_list,outfile) #tweets are dumped into the JSON file
            print(outfile)
            return True
        #as soon as limiter variable is reached, the stream disconnects itself automatically
        else:
            myStream.disconnect()

    # error handling is initiated, in case stream is erroneous
    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_error disconnects the stream
            return False



# the streamer is initalised and certain parameters are defined
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(getStreamingAuth(), listener=myStreamListener, tweet_mode='extended')

#the hashtag to be streamed for is set to #vegan
myStream.filter(track=['#pokemon'],is_async=True)


