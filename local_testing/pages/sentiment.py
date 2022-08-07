import requests
import pandas as pd
import re
import json
import streamlit as st
import plotly.express as px
import numpy as np

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob

st.title("Sentiment Analysis")

#------------TO-DO------------------

endpoint = 'https://api.twitter.com/2/tweets/search/recent'
headers = {'Authorization' : 'Bearer AAAAAAAAAAAAAAAAAAAAAGaVfQEAAAAAw0NVD2QK7d%2Boe%2B1EyKFZpWs%2F0rA%3DlzUkkQ4W5Eirk1c9k97CyybihOe83XrUaqnPgkRd8T8M3YorMc'}
parameters = {'query' : 'tesla', 'max_results' : '100', 'tweet.fields' : 'lang'}

response = requests.get(endpoint, headers = headers, params = parameters)
tweets = response.json()['data']
next_token = response.json()['meta']['next_token']
parameters['next_token'] = next_token

response_page2 = requests.get(endpoint, headers = headers, params = parameters)
tweets += response_page2.json()['data']

#s3 = boto3.client('s3')
#s3_response = s3.put_object(Body = json.dumps(tweets), Bucket = 'casacloudbucket', Key = 'tesla' + '.json')

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

print(tweet_df)
fig = px.pie(tweet_df, names = 'sentiment', values = np.ones(tweet_df.shape[0]))
st.plotly_chart(fig)