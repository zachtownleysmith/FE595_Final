from flask import Flask, redirect, url_for, render_template, request
from get_news import bing_api_search

app = Flask(__name__)


@app.route("/getSentiment", methods=["POST", "GET"])
def splash():
    if request.method == "POST":
        company = request.form["company_test"]
        sentiment = request.form["sentiment_test"]

        # Add Error Check for non-integer article number POST, default 5
        try:
            article_count = int(request.form["article_cnt"])
            bad_count = None
            proper_count = True
        except ValueError:
            article_count = 5
            bad_count = request.form["article_cnt"]
            proper_count = False

        data = bing_api_search(search_term=company, search_num=article_count)
        if sentiment == "Aggregated":
            return render_template("Multiple_Senti.html", data=data, sentiment=sentiment,
                                   article_count=article_count, proper_count=proper_count, bad_count=bad_count)
        elif sentiment == "TextBlob":
            return render_template("TB_Senti.html", data=data, sentiment=sentiment,
                                   article_count=article_count, proper_count=proper_count, bad_count=bad_count)
        else:
            return render_template("NLTK_Senti.html", data=data, sentiment=sentiment,
                                   article_count=article_count, proper_count=proper_count, bad_count=bad_count)
    else:
        return render_template("splash.html")


if __name__ == "__main__":
    app.run()
