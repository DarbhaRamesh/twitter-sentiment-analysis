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


def get_tweets(keyword='Joe Biden'):
    client = tweepy.Client(Bearer_Token, API_Key, API_Key_Secret, ACCESS_KEY, ACCESS_KEY_SECRET)
    query = '"{}" lang:en'.format(keyword)
    tweets = client.search_recent_tweets(query=query, max_results=100)
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


def sentiment_dataframe(keyword='Joe Biden'):
    response = get_tweets(keyword)
    df = pd.DataFrame([tweet.text for tweet in response.data], columns=['tweets'])
    df['tweets'] = df['tweets'].apply(clean_tweet)
    df.drop_duplicates(subset="tweets", keep=False, inplace=True)
    df['polarity'] = df['tweets'].apply(get_polaity)
    df['sentiment'] = df['polarity'].apply(get_sentiments)
    display_df = df[['tweets', 'sentiment']]
    return display_df.values.tolist()
