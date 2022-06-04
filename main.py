from flask import Flask, render_template, session, request
from tweets import sentiment_dataframe

app = Flask(__name__)
app.secret_key = 'oEBXwDLiqtmNtZ42u3GY'


@app.route('/', methods=('GET', 'POST'))
def home_page():
    return render_template('index.html')


@app.route('/tweets', methods=("POST", "GET"))
def get_tweets():
    if request.method == 'POST':
        keyword = request.form['tweet_keyword'].strip()
        df = sentiment_dataframe(keyword)
        return render_template('tweets.html', tweets_sentiments=df)


# if __name__ == "__main__":
#     app.run()
