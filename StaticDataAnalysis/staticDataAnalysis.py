import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import itertools
import collections
from StaticDataAnalysis import (accessAuthAPI, config, getTwitterStaticData)
from StaticDataAnalysis.data import (cleanData, getDataFile)

from nltk.corpus import stopwords

import warnings

warnings.filterwarnings("ignore")

sns.set(font_scale=1.5)
sns.set_style("whitegrid")

# running script for searching twitter hashtag and dumps into Json file named "staticDataAnalysis.json"
getTwitterStaticData.getTweets()

# get full text of data in dataset form
full_text_tweets = getDataFile.readDataWithPandas('data/staticDataAnalysis.json')

# cleaning the data

# 1- remove Duplicates
df_dropped = full_text_tweets.drop_duplicates(keep='first')

# 2- remove URLS
no_url_tweet_data = cleanData.removeURLS(df_dropped)

# 3- remove emojis
no_emoji_tweet_data = cleanData.removeEmojis(no_url_tweet_data)

# 4- addressing case issues
data_to_lower_case = no_emoji_tweet_data.lower().split()

# 5- using stopWords
tokens_without_sw = [word for word in data_to_lower_case if not word in stopwords.words('english')]

# Create counter
counts_no_urls = collections.Counter(tokens_without_sw)
# to make count common Words - a collection will be used to count each word in the list and create a dataset
# most_common_word = counts_no_urls.items()

# creating data table for
clean_tweets = pd.DataFrame(counts_no_urls.items(), columns=['Words', 'wordCount'])
print(clean_tweets)

# Task: Perform the following data analysis:

# Frequency mentions of an organisation: "government"
organisation_frequency = clean_tweets[clean_tweets['Words'].isin(["government", "Federal"])]

print("\n Frequency for organisations mentioned: \n" + str(organisation_frequency.values))

# Frequency of selected meaningful text term:  "climate", "action", "change", "emissions"

meaningful_term_frequency = clean_tweets[clean_tweets['Words'].isin(["climate", "action", "change", "emissions"])]
print("\nFrequency for selected meaningful terms: \n" + str(meaningful_term_frequency.values))

# Most used @ mentions

"""
First lets get all the Words with @ mentions
Then we sort them in ascending order to get the most mentions
We use .head and call top 5 rows from table
"""

most_used_mentions = clean_tweets[clean_tweets['Words'].str.contains('@')].sort_values(by=['wordCount'],
                                                                                       ascending=False).head(5)

print("Displaying most used top 5 @ mentions:")
print(most_used_mentions)

# search multiple terms that contains a specifc word etc:
# df[df['A'].astype(str).str.contains("Hello|Britain")]
