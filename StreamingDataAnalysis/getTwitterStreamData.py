import json
import warnings
import seaborn as sns
import tweepy

from StreamingDataAnalysis.accessAuthAPI import getStreamingAuth
from StreamingDataAnalysis.data import readDataFile, cleanData
from StreamingDataAnalysis.data.pushDataIntoFile import saveDataIntoFile

warnings.filterwarnings("ignore")

sns.set(font_scale=1.5)
sns.set_style("whitegrid")


# both variables are used to automatically end the stream after 10,000 tweets. Tweet_count is the count variable and n_tweets is the limiter.
tweet_count = 0
n_tweets = 40

# the list, where the streamed tweets need to be collected and stored in, is generated
tweets_list = []


# Twitter Stream Listener
class TwitterStreamListener(tweepy.StreamListener):
    def on_data(self, status):

        # global variables made accessible within the on_data method
        global tweet_count
        global n_tweets
        global tweets_list
        global myStream

        # list is appended to json until n_tweets amount is reached.
        if tweet_count < n_tweets:
            tweets_list.append(json.loads(status))
            tweet_count += 1  # count variable is extended by one, until limiter is reached
            print(tweet_count)  # tweet count is printed out for visual representation

            all_tweets = [tweet for tweet in tweets_list]
            saveDataIntoFile(all_tweets)
            return True
        # as soon as limiter variable is reached, the stream disconnects itself automatically
        else:
            myStream.disconnect()

    # error handling is initiated, in case stream is erroneous
    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_error disconnects the stream
            return False


myStreamListener = TwitterStreamListener()
myStream = tweepy.Stream(getStreamingAuth(), listener=myStreamListener, tweet_mode='extended')

# set the hashtag to be streamed
myStream.filter(track=['#cop26'], is_async=False)

