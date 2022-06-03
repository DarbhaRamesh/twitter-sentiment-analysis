from flask import Flask, render_template, session
from tweets import sentiment_dataframe, positive_tweets, negative_tweets, neutral_tweets

app = Flask(__name__)
app.secret_key = 'oEBXwDLiqtmNtZ42u3GY'


@app.route('/', methods=("POST", "GET"))
def get_tweets():
    try:
        next_token = session['next_token']
    except KeyError:
        next_token = None
    df, next_token = sentiment_dataframe(next_token)
    session['next_token'] = next_token
    p_tweets = positive_tweets(df)
    n_tweets = negative_tweets(df)
    nu_tweets = neutral_tweets(df)
    return render_template('index.html', tweets=[p_tweets['tweets'], n_tweets['tweets'], nu_tweets['tweets']])
