import asyncio
import collections
from itertools import combinations

import nltk
import pandas as pd
from nltk import bigrams, word_tokenize

from nltk.corpus import stopwords, webtext
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from StreamingDataAnalysis.data import readDataFile, cleanData
from StreamingDataAnalysis.getTwitterStreamData import TwitterStreamListener
# get full text of data in dataset form
full_text_tweets = readDataFile.readDataWithPandas('data/streamingDataAnalysis.json')
new_full_text_tweets = pd.DataFrame.from_dict(full_text_tweets['text'])

# cleaning the data

# 1- remove Duplicates
df_dropped = new_full_text_tweets.drop_duplicates()
# print(df_dropped)

# # 2- remove URLS
no_url_tweet_data = cleanData.removeURLS(df_dropped)
# print(no_url_tweet_data)

# 3- remove emojis

no_emoji_tweet_data = cleanData.removeEmojis(no_url_tweet_data)
# print(no_emoji_tweet_data)

# 4- addressing case issues
data_to_lower_case = no_emoji_tweet_data.lower().split()
# print(data_to_lower_case)

# 5- using stopwords
all_stopwords = set(stopwords.words('english','zh'))

all_stopwords.update([str('\n'), str('\n\n'), ',', '...', 'ส่วนตัวคิดว่าการที่พูดภาษาอังกฤษไม่ได้แล้วพูดไทยแทนในที่ประชุมระดับโลกยังไม่น่าอายเท่าพูดภาษาไทยแล้วยังก้มหน้าอ่านโพยเกือบ'])

word_tokens = word_tokenize(str(data_to_lower_case).rstrip())

tokens_without_sw = [word for word in data_to_lower_case if not word in all_stopwords]


# Create collection/counter of the words
counts_no_urls = collections.Counter(tokens_without_sw)

# creating data table for
clean_tweets_table = pd.DataFrame(counts_no_urls.items(), columns=['Words', 'WordCount'])
# print(clean_tweets_table)

# Task: Perform analysis of streaming data from the selected hashtag feed: #cop26

# a. A list of hashtags most used with selected hashtag:

most_used_mentions = clean_tweets_table[clean_tweets_table['Words'].str.contains('#')].sort_values(by=['WordCount'],
                                                                                                   ascending=False).head(
    5)

print("\nDisplaying most used top # mentions:")
print(most_used_mentions)

# b. Most occurring terms

get_most_common_terms = counts_no_urls.most_common(10)
most_common_term_table = pd.DataFrame(get_most_common_terms, columns=['Words', 'WordCount']).sort_values(
    by=['WordCount'], ascending=False).head(10)

#removing redundant terms
new_most_common_term_table = most_common_term_table[most_common_term_table["Words"].str.contains('#|de|rt|el|en|la|que|para|les|-|\n|&|@|ส่')==False]

print('\nMost occuring terms are: ')
print(new_most_common_term_table)

# c. Terms that may frequently occur together in the feed (bigrams terms)

by_bigram = nltk.bigrams(counts_no_urls)

ngram_grouped = [" ".join([i for i in x]) for x in by_bigram]

#creating table of bigram terms
ngram_term_table = pd.DataFrame(ngram_grouped, columns=['Bigram_Term']).sort_values(by=['Bigram_Term'], ascending = False).head(10)
new_ngram_term_table = ngram_term_table[ngram_term_table["Bigram_Term"].str.contains('#|de|rt|el|en|la|que|para|les|-|\n|&|@|ส่|“|今')==False]

#adding to count frequency to terms
new_ngram_term_table['count']=new_ngram_term_table.groupby('Bigram_Term')['Bigram_Term'].transform('count')

print("\nFrequent terms in bigram")
print(ngram_term_table)


