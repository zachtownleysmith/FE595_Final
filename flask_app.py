from flask import Flask, redirect, url_for, render_template, request
from get_news import bing_api_search

app = Flask(__name__)


#@app.route("/output", methods=["POST","GET"])
#def served_articles(data):
    #return render_template("TB_Senti.html", data=data)


@app.route("/getSentiment", methods=["POST", "GET"])
def splash():
    if request.method == "POST":
        company = request.form["company_test"]
        sentiment = request.form["sentiment_test"]
        data = bing_api_search(company)
        if sentiment == "Aggregated":
            return render_template("Multiple_Senti.html", data=data, sentiment=sentiment)
        elif sentiment == "TextBlob":
            return render_template("TB_Senti.html", data=data, sentiment=sentiment)
        else:
            return render_template("NLTK_Senti.html", data=data, sentiment=sentiment)
    else:
        return render_template("splash.html")


if __name__ == "__main__":
    app.run()
