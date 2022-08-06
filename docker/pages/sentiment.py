import pandas as pd
import re
import streamlit as st

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
from utils import *

st.title("Sentiment Analysis")

# Read from the bucket
bucket = get_bucket()
df = get_df(bucket, "news")

#------------TO-DO------------------

for tweet in tweets[:]:
    if tweet['lang'] != 'en':
        tweets.remove(tweet)

tweet_list = []

for tweet in tweets[:]:
    tweet_list.append(tweet['text'])

tweet_df = pd.DataFrame(tweet_list)

tweet_df.drop_duplicates(inplace = True)

tweet_df['text'] = tweet_df[0]

tweet_df = tweet_df.reset_index()

tweet_df = tweet_df.drop('index', axis = 1)

remove_backslah = lambda x : re.sub('(\n)+', ' ', x)
remove_retweet = lambda x : re.sub('RT @\w+:', ' ', x)
remove_tag = lambda x : re.sub('@\w+', ' ', x)
remove_link = lambda x : re.sub('https.+', ' ', x)
remove_hashtag = lambda x : re.sub('#\w+', ' ', x)
remove_punctuation = lambda x : re.sub('[^\w\s]', ' ', x)
remove_multiple_whitespaces = lambda x : re.sub(' +', ' ', x)

tweet_df['text'] = tweet_df['text'].map(remove_backslah).map(remove_retweet).map(remove_tag).map(remove_link).map(remove_hashtag).map(remove_punctuation).map(remove_multiple_whitespaces)

tweet_df[['polarity', 'subjectivity']] = tweet_df['text'].apply(lambda Text: pd.Series(TextBlob(Text).sentiment))

for index, row in tweet_df['text'].iteritems():
    score = SentimentIntensityAnalyzer().polarity_scores(row)
    negative = score['neg']
    neutral = score['neu']
    positive = score['pos']
    compound = score['compound']

    if negative > positive: tweet_df.loc[index, 'sentiment'] = 'negative'
    elif negative < positive: tweet_df.loc[index, 'sentiment'] = 'positive'
    else: tweet_df.loc[index, 'sentiment'] = 'neutral'

    tweet_df.loc[index, 'negative'] = negative
    tweet_df.loc[index, 'neutral'] = neutral
    tweet_df.loc[index, 'positive'] = positive
    tweet_df.loc[index, 'compound'] = compound