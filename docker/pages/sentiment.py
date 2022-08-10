import boto3
import json
import nltk
import numpy as np
import pandas as pd
import plotly.express as px
import re
import streamlit as st

from configuration import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob

st.title("Sentiment Analysis")

nltk.download("vader_lexicon")

option = st.selectbox(
    "Select the Company Stock you want to see:",
    (SYMBOLS.keys()),
)

s3 = boto3.client("s3")
if option == "Apple":
    option = option + " Inc"
elif option == "Meta":
    option = "Facebook"
response = s3.get_object(Bucket=BUCKET_NAME, Key="tweet_" + option + ".json")

tweets = json.loads(response['Body'].read())

tweet_list = [tweet["text"] for tweet in tweets if tweet["lang"] == "en"]

tweet_df = pd.DataFrame(tweet_list, columns=["text"])

tweet_df.drop_duplicates(inplace=True)

remove_backslah = lambda x: re.sub("(\n)+", " ", x)
remove_retweet = lambda x: re.sub("RT @\w+:", " ", x)
remove_tag = lambda x: re.sub("@\w+", " ", x)
remove_link = lambda x: re.sub("https.+", " ", x)
remove_hashtag = lambda x: re.sub("#\w+", " ", x)
remove_punctuation = lambda x: re.sub("[^\w\s]", " ", x)
remove_multiple_whitespaces = lambda x: re.sub(" +", " ", x)

tweet_df["text"] = (
    tweet_df["text"]
    .map(remove_backslah)
    .map(remove_retweet)
    .map(remove_tag)
    .map(remove_link)
    .map(remove_hashtag)
    .map(remove_punctuation)
    .map(remove_multiple_whitespaces)
)

tweet_df[["polarity", "subjectivity"]] = tweet_df["text"].apply(
    lambda Text: pd.Series(TextBlob(Text).sentiment)
)

for index, row in tweet_df["text"].iteritems():
    score = SentimentIntensityAnalyzer().polarity_scores(row)
    negative = score["neg"]
    neutral = score["neu"]
    positive = score["pos"]
    compound = score["compound"]

    if negative > positive:
        tweet_df.loc[index, "sentiment"] = "negative"
    elif negative < positive:
        tweet_df.loc[index, "sentiment"] = "positive"
    else:
        tweet_df.loc[index, "sentiment"] = "neutral"

    tweet_df.loc[index, "negative"] = negative
    tweet_df.loc[index, "neutral"] = neutral
    tweet_df.loc[index, "positive"] = positive
    tweet_df.loc[index, "compound"] = compound

fig = px.pie(tweet_df, names="sentiment", values=np.ones(tweet_df.shape[0]))
st.plotly_chart(fig)