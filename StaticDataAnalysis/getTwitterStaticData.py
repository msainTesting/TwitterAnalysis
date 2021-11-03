from StaticDataAnalysis.accessAuthAPI import getAuth
import warnings

import tweepy as tw

from StaticDataAnalysis.accessAuthAPI import getAuth
from StaticDataAnalysis.data import pushDataIntoFile as saveDatafile

warnings.filterwarnings("ignore")

global all_tweets
global word_in_tweet


def getTweets():
    n_tweets = 100

    # set the hashtag to be streamed
    search_term = "#cop26 -filter=retweets"
    tweets = tw.Cursor(getAuth().search,
                       q=search_term,
                       lang="en",
                       until='2021-11-03').items(n_tweets)

    all_tweets = [tweet.text for tweet in tweets]

    saveDatafile.saveDataIntoFile(all_tweets)
