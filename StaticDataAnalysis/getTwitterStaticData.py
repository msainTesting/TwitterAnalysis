import warnings

import tweepy as tw

from StaticDataAnalysis.Data import pushDataIntoFile as saveDatafile
from StaticDataAnalysis.accessAuthAPI import getAuth

warnings.filterwarnings("ignore")

global all_tweets
global word_in_tweet


def getTweets():
    n_tweets = 200

    # set the hashtag to be streamed
    search_term = "#cop26 -filter=retweets"
    tweets = tw.Cursor(getAuth().search,
                       q=search_term,
                       lang="en",
                       until='2021-11-03').items(n_tweets)

    all_tweets = [tweet.text for tweet in tweets]

    saveDatafile.saveDataIntoFile(all_tweets)
