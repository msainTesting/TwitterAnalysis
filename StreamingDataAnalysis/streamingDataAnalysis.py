import collections
import time

import nltk
import pandas as pd
from nltk import word_tokenize
from nltk.corpus import stopwords

from StreamingDataAnalysis.data import readDataFile, cleanData

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

"""
TwitterStreamListener() has been disabled as we have already attained data using hashtag #cop26. 
to run fresh data simply uncomment TwitterStreamListener(). Due to time-rates that Twitter impose, you will find that 
runs will stop thus failing the script.

In this scenario, data were attained by running the script repeatedly and then merging the data together

"""
# disabled - uncomment to enable and to get fresh data

# TwitterStreamListener()
# getting fresh live data from json file
# live_full_text_tweets = readDataFile.readDataWithPandas('Data/StreamingDataAnalysis.json')
# new_full_text_tweets = pd.DataFrame.from_dict(live_full_text_tweets['text'])


""" Disable following section if running TwitterStreamListener()"""
"""Section Start"""
# getting pre-existing data from multiple json file
full_text_tweets1 = readDataFile.readDataWithPandas('Data/data_stream03.json')
full_text_tweets2 = readDataFile.readDataWithPandas('Data/data_stream02.json')
full_text_tweets3 = readDataFile.readDataWithPandas('Data/data_stream01.json')

# getting the data from the Key: text

new_full_text_tweets1 = pd.DataFrame.from_dict(full_text_tweets1['text'])
new_full_text_tweets2 = pd.DataFrame.from_dict(full_text_tweets2['text'])
new_full_text_tweets3 = pd.DataFrame.from_dict(full_text_tweets3['text'])

# Merging the three json data in the form of text that has been retrieved together
new_full_text_tweets = new_full_text_tweets1 + new_full_text_tweets2 + new_full_text_tweets3
"""Section End"""

time.sleep(5)

# cleaning the Data

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

# 5- using stopwords to remove redundant words
all_stopwords = set(stopwords.words('english', 'zh'))

all_stopwords.update([str('\n'), str('\n\n'), ',', '...',
                      'ส่วนตัวคิดว่าการที่พูดภาษาอังกฤษไม่ได้แล้วพูดไทยแทนในที่ประชุมระดับโลกยังไม่น่าอายเท่าพูดภาษาไทยแล้วยังก้มหน้าอ่านโพยเกือบ'])

word_tokens = word_tokenize(str(data_to_lower_case).rstrip())

tokens_without_sw = [word for word in data_to_lower_case if not word in all_stopwords]

# Create collection/counter of the words
counts_no_urls = collections.Counter(tokens_without_sw)

# creating Data table for
clean_tweets_table = pd.DataFrame(counts_no_urls.items(), columns=['Words', 'WordCount'])

# Task: Perform analysis of streaming Data from the selected hashtag feed: #cop26

# a. A list of hashtags most used with selected hashtag:

# removing redundant terms

remove_unwanted_terms = clean_tweets_table[clean_tweets_table["Words"].str.contains(
    '#cop26|#cop26:|#cop26|\n|@cop26|de|rt|el|en|la|que|para|les|-|\n|&|@|ส่') == False]
most_used_mentions = remove_unwanted_terms[remove_unwanted_terms['Words'].str.contains('#')].sort_values(
    by=['WordCount'],
    ascending=False).head(5)
print("\nDisplaying most used top # mentions:")
print(most_used_mentions)

# b. Most occurring terms

# further cleaning required to remove redundant terms
remove_redundant_words = remove_unwanted_terms[
    remove_unwanted_terms["Words"].str.contains('#|&|es|los|un|se|le|con|al|et') == False]
most_common_term_table = pd.DataFrame(remove_redundant_words, columns=['Words', 'WordCount']).sort_values(
    by=['WordCount'], ascending=False).head(5)

# removing redundant terms
# new_most_common_term_table = most_common_term_table[most_common_term_table["Words"].str.contains('#|de|rt|el|en|la|que|para|les|-|\n|&|@|ส่')==False]

print('\nMost occuring terms are: ')
print(most_common_term_table)

# c. Terms that may frequently occur together in the feed (bigrams terms)

by_bigram = nltk.bigrams(counts_no_urls)

ngram_grouped = [" ".join([i for i in x]) for x in by_bigram]

# creating table of bigram terms
ngram_term_table = pd.DataFrame(ngram_grouped, columns=['Bigram_Term']).sort_values(by=['Bigram_Term'],
                                                                                    ascending=False).head(5)
new_ngram_term_table = ngram_term_table[
    ngram_term_table["Bigram_Term"].str.contains('#|de|rt|el|en|la|que|para|les|-|\n|&|@|ส่|“|今') == False]

# counting frequency terms
new_ngram_term_table['count'] = ngram_term_table.groupby('Bigram_Term')['Bigram_Term'].transform('count')

print("\nFrequent terms in bigram")
print(new_ngram_term_table)

# Sending result output to text file


# creating path for each file that relevant data will be sent to
filePath = "GetStreamingResultsOutput/resultOutputQuestions.txt"
removeURLFilePath = "GetStreamingResultsOutput/removeURLData.txt"
removeDuplicateFilePath = "GetStreamingResultsOutput/removeDuplicateData.txt"
removeEmojisFilePath = "GetStreamingResultsOutput/removeEmojiData.txt"
removeUpperCaseFilePath = "GetStreamingResultsOutput/removeUpperCaseData.txt"
removeStopWordsFilePath = "GetStreamingResultsOutput/removeStopWordsData.txt"

# Send json twitter data to txt file
tweetDataPath = "GetStreamingResultsOutput/tweetDataSavedOnRun.txt"

with open(tweetDataPath, "w", encoding='utf-8', errors='replace') as myfile:
    myfile.write("\nTweet Text Data \n\n")
    myfile.write(str(new_full_text_tweets))

""" open the file so that data can be written into it
#existing data in file is file removed on every run and new data is added by using "with open" """

# allow ability to write encoding='utf-8' charcters within the file
# Output returned from cleaning intial data

with open(removeDuplicateFilePath, "w", encoding='utf-8', errors='replace') as myfile:
    "\n\nTable of results for cleaning data: \n\n"

    myfile.write("\nremove Duplicates\n\n")
    myfile.write(str(df_dropped))

with open(removeURLFilePath, "w", encoding='utf-8', errors='replace') as myfile:
    myfile.write("\n Remove URLS \n\n")
    myfile.write(str(no_url_tweet_data))

with open(removeEmojisFilePath, "w", encoding='utf-8', errors='replace') as myfile:
    myfile.write("\n Remove emojis \n\n")
    myfile.write(str(no_emoji_tweet_data))

with open(removeUpperCaseFilePath, "w", encoding='utf-8', errors='replace') as myfile:
    myfile.write("\n Addressing case issues \n\n")
    myfile.write(str(data_to_lower_case))

with open(removeStopWordsFilePath, "w", encoding='utf-8', errors='replace') as myfile:
    myfile.write("\n Remove stopWords \n\n")
    myfile.write(str(clean_tweets_table.head(50)))

# Output for checking frequency analysis

with open(filePath, "w", encoding='utf-8', errors='replace') as myfile:
    "\n\n Table of results for Frequency: \n\n"

    myfile.write("\n- Most used hashtags with initially selected hashtag\n\n")
    myfile.write(str(most_used_mentions))
    myfile.write("\n\n- Most occurring terms \n\n")
    myfile.write(str(most_common_term_table))
    myfile.write("\n\n- Terms that frequently occur together (bigram) \n\n")
    myfile.write(str(new_ngram_term_table))

