from flask import Flask, redirect, url_for, render_template, request
from get_news import bing_api_search
import yfinance as yf

app = Flask(__name__)


@app.route("/getSentiment", methods=["POST", "GET"])
def splash():
    if request.method == "POST":
        ticker = request.form["ticker_input"]
        sentiment = request.form["sentiment_input"]

        # Add Error Check for non-integer article number POST, default 5
        try:
            article_count = int(request.form["article_cnt"])
            bad_count = None
            proper_count = True
        except ValueError:
            article_count = 5
            bad_count = request.form["article_cnt"]
            proper_count = False

        # Add Error Check to see if submitted ticker is actually a ticker
        try:
            company = yf.Ticker(ticker).info['longName']
            proper_ticker = True
        except KeyError:
            company = ticker
            proper_ticker = False

        data = bing_api_search(search_term=company, search_num=article_count)
        if sentiment == "Aggregated":
            return render_template("Multiple_Senti.html", data=data, sentiment=sentiment,
                                   article_count=article_count, proper_count=proper_count, bad_count=bad_count,
                                   ticker=ticker, proper_ticker=proper_ticker, company=company)
        elif sentiment == "TextBlob":
            return render_template("TB_Senti.html", data=data, sentiment=sentiment,
                                   article_count=article_count, proper_count=proper_count, bad_count=bad_count,
                                   ticker=ticker, proper_ticker=proper_ticker, company=company)
        else:
            return render_template("NLTK_Senti.html", data=data, sentiment=sentiment,
                                   article_count=article_count, proper_count=proper_count, bad_count=bad_count,
                                   ticker=ticker, proper_ticker=proper_ticker, company=company)
    else:
        return render_template("splash.html")


if __name__ == "__main__":
    app.run()
