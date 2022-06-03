import tweepy
import os
import pandas as pd
import re
from textblob import TextBlob

Bearer_Token = os.getenv("Bearer_Token")
API_Key = os.getenv("API_Key")
API_Key_Secret = os.getenv("API_Key_Secret")
ACCESS_KEY = os.getenv("Access_Key")
ACCESS_KEY_SECRET = os.getenv("Access_Key_Secret")


def get_tweets(token=None):
    client = tweepy.Client(Bearer_Token, API_Key, API_Key_Secret, ACCESS_KEY, ACCESS_KEY_SECRET)
    query = '"Joe Biden" lang:en'
    tweets = client.search_recent_tweets(query=query, max_results=100, next_token=token)
    return tweets


def clean_tweet(tweet):
    tweet = re.sub(r'@[A-Za-z0-9]+', '', tweet)
    tweet = re.sub(r'#', '', tweet)
    tweet = re.sub(r':[\s]+', '', tweet)
    tweet = re.sub(r'RT[\s]+', '', tweet)
    tweet = re.sub(r'https?:\/\/\S+', '', tweet)
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)
    tweet = emoji_pattern.sub(r'', tweet)  # no emoji
    tweet = re.sub(r"^[^A-Za-z0-9]+", "", tweet)
    return tweet


def get_polaity(tweet):
    return TextBlob(tweet).polarity


def get_sentiments(polarity):
    if polarity > 0:
        return 'Positive'
    elif polarity == 0:
        return 'Neutral'
    else:
        return 'Negative'


def sentiment_dataframe(next_token=None):
    response = get_tweets(next_token)
    next_token = response.meta['next_token']
    df = pd.DataFrame([tweet.text for tweet in response.data], columns=['tweets'])
    df['tweets'] = df['tweets'].apply(clean_tweet)
    df.drop_duplicates(subset="tweets", keep=False, inplace=True)
    df['polarity'] = df['tweets'].apply(get_polaity)
    df['sentiment'] = df['polarity'].apply(get_sentiments)
    return df, next_token


def positive_tweets(df):
    p_df = df[df['sentiment'] == 'Positive'][['tweets']].copy()
    return p_df.to_dict('dict')


def negative_tweets(df):
    n_df = df[df['sentiment'] == 'Negative'][['tweets']].copy()
    return n_df.to_dict('dict')


def neutral_tweets(df):
    nu_df = df[df['sentiment'] == 'Neutral'][['tweets']].copy()
    return nu_df.to_dict('dict')
