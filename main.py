from flask import Flask, render_template, session, request
from tweets import sentiment_dataframe, positive_tweets, negative_tweets, neutral_tweets

app = Flask(__name__)
app.secret_key = 'oEBXwDLiqtmNtZ42u3GY'


@app.route('/', methods=('GET', 'POST'))
def home_page():
    return render_template('index.html')


@app.route('/tweets', methods=("POST", "GET"))
def get_tweets():
    if request.method == 'POST':
        keyword = request.form['tweet_keyword'].strip()
        try:
            next_token = session['next_token']
        except KeyError:
            next_token = None
        df, next_token = sentiment_dataframe(next_token, keyword)
        session['next_token'] = next_token
        p_tweets = positive_tweets(df)
        n_tweets = negative_tweets(df)
        nu_tweets = neutral_tweets(df)
        return render_template('tweets.html', tweets=[p_tweets['tweets'], n_tweets['tweets'], nu_tweets['tweets']])


# if __name__ == "__main__":
#     app.run()
