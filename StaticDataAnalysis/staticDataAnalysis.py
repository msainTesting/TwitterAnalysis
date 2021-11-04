import collections
import time

import pandas as pd
import seaborn as sns
from nltk import word_tokenize

from StaticDataAnalysis import (getTwitterStaticData)
from StaticDataAnalysis.Data import (cleanData, getDataFile)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

from nltk.corpus import stopwords

import warnings

warnings.filterwarnings("ignore")

sns.set(font_scale=1.5)
sns.set_style("whitegrid")

# running script for searching twitter hashtag and dumps into Json file named "staticDataAnalysis.json"
getTwitterStaticData.getTweets()

# get full text of Data in dataset form
full_text_tweets = getDataFile.readDataWithPandas('Data/staticDataAnalysis.json')

time.sleep(5)

# cleaning the Data

# 1- remove Duplicates
df_dropped = full_text_tweets.drop_duplicates(keep='first')

# 2- remove URLS
no_url_tweet_data = cleanData.removeURLS(df_dropped)

# 3- remove emojis
no_emoji_tweet_data = cleanData.removeEmojis(no_url_tweet_data)

# 4- addressing case issues
data_to_lower_case = no_emoji_tweet_data.lower().split()

# 5- using stopWords
all_stopwords = set(stopwords.words('english', 'zh'))

all_stopwords.update([str('\n'), str('\n\n'), ',', '...',
                      'ส่วนตัวคิดว่าการที่พูดภาษาอังกฤษไม่ได้แล้วพูดไทยแทนในที่ประชุมระดับโลกยังไม่น่าอายเท่าพูดภาษาไทยแล้วยังก้มหน้าอ่านโพยเกือบ'])

word_tokens = word_tokenize(str(data_to_lower_case).rstrip())

tokens_without_sw = [word for word in data_to_lower_case if not word in stopwords.words('english')]

# Create counter
counts_no_urls = collections.Counter(tokens_without_sw)
# to make count common Words - a collection will be used to count each word in the list and create a dataset
# most_common_word = counts_no_urls.items()

# creating Data table for
clean_tweets = pd.DataFrame(counts_no_urls.items(), columns=['Words', 'wordCount'])

# Task: Perform the following Data analysis:

# Frequency mentions of an organisation: "government"
organisation_frequency = clean_tweets[clean_tweets['Words'].isin(["government", "government's"])]
organisation_frequency_Values = str(organisation_frequency.values)

print("\n Frequency for organisations mentioned: \n" + organisation_frequency_Values)

# Frequency of selected meaningful text term:  "climate", "action", "change", "emissions"

meaningful_term_frequency = clean_tweets[clean_tweets['Words'].isin(["climate", "action", "change", "emissions"])]
meaningful_term_frequency_Values = str(meaningful_term_frequency.values)

print("\nFrequency for selected meaningful terms: \n" + meaningful_term_frequency_Values)

# Most used @ mentions

"""
First lets get all the Words with @ mentions
Then we sort them in ascending order to get the most mentions
We use .head and call top 5 rows from table
"""

most_used_mentions = clean_tweets[clean_tweets['Words'].str.contains('@')].sort_values(by=['wordCount'],
                                                                                       ascending=False).head(5)
print("\nDisplaying most used top 5 @ mentions:")
print(str(most_used_mentions))

# Send result output to text file

# creating path for each file that relevant data will be sent to
filePath = "GetStaticResultsOutput/resultOutputQuestion.txt"
removeURLFilePath = "GetStaticResultsOutput/removeURLData.txt"
removeDuplicateFilePath = "GetStaticResultsOutput/removeDuplicateData.txt"
removeEmojisFilePath = "GetStaticResultsOutput/removeEmojiData.txt"
removeUpperCaseFilePath = "GetStaticResultsOutput/removeUpperCaseData.txt"
removeStopWordsFilePath = "GetStaticResultsOutput/removeStopWordsData.txt"

# Send json twitter data to txt file
tweetDataPath = "GetStaticResultsOutput/tweetDataSavedOnRun.txt"

with open(tweetDataPath, "w", encoding='utf-8', errors='replace') as myfile:
    myfile.write("\nTweet Text Data \n\n")
    myfile.write(str(full_text_tweets))


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
    myfile.write(str(clean_tweets.head(50)))

# Output for checking frequency analysis

with open(filePath, "w") as myfile:
    "\n\n Table of results for Frequency: \n\n"

    myfile.write("\n\n- Frequency of mentions of organisation\n\n")
    myfile.write(str(organisation_frequency_Values))
    myfile.write("\n\n- Frequency of selected selected meaningful terms\n\n")
    myfile.write(str(meaningful_term_frequency_Values))
    myfile.write("\n\n- Most used @ mentions\n\n")
    myfile.write(str(most_used_mentions))


