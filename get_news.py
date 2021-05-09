import requests
import pandas as pd
from textblob import TextBlob
from nltk.sentiment import SentimentIntensityAnalyzer
from bs4 import BeautifulSoup as bs
import nltk
nltk.download('vader_lexicon')


# Define Functions for computing sentiment score of article descriptions
def sentiment_summary_nltk(data_1):
    sia = SentimentIntensityAnalyzer()
    score = [round(sia.polarity_scores(article)["compound"], 4) for article in data_1]
    return score


def sentiment_summary_tb(data_1):
    score = [round(TextBlob(article).sentiment.polarity, 4) for article in data_1]
    return score

'''
def sentiment_summary_nltk(data_1):
    sia = SentimentIntensityAnalyzer()
    score = ["Positive" if sia.polarity_scores(article)["compound"] >= 0.1 else ("Negative" if sia.polarity_scores(article)["compound"] <= -0.1 else "Neutral") for article in data_1]
    return score


def sentiment_summary_tb(data_1):
    score = ["Positive" if TextBlob(article).sentiment.polarity >= 0.1
             else ("Negative" if TextBlob(article).sentiment.polarity <= -0.1 else "Neutral") for article in data_1]
    return score
'''


def bing_api_search(search_term):
    # Setup Request to Bing API and save JSON response
    subscription_key = "XXXXXXXXXXXXXXXXXXXXXXX"
    search_url = "https://api.bing.microsoft.com/v7.0/news/search"
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    params = {"category": "Business", "count": 5, "q": search_term, "textDecorations": True, "textFormat": "HTML"}
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    bing_resp = response.json()["value"]

    # Remove HTML from returned text and store as temp variable
    name = [bs(article["name"], "lxml").text for article in bing_resp]
    descriptions = [bs(article["description"], "lxml").text for article in bing_resp]
    url = [article["url"] for article in bing_resp]
    pubDate = [bs(article["datePublished"], "lxml").text for article in bing_resp]
    provider = [bs(article["provider"][0]["name"], "lxml").text for article in bing_resp]

    # Aggregate output into Pandas DF
    data = {"Title": name, "Description": descriptions,
            "Sentiment_NLTK": sentiment_summary_nltk(descriptions),
            "Sentiment_TB": sentiment_summary_tb(descriptions),
            "URL": url, "PubDate": pubDate, "Provider": provider}
    df = pd.DataFrame(data)

    df['Sentiment_AVG'] = round(df[['Sentiment_NLTK', 'Sentiment_TB']].mean(axis=1), 4)
    return df


if __name__ == "__main__":
    test=bing_api_search("exxon")
    print(test['Sentiment_NLTK'])
    print(test['Sentiment_TB'])
    print(test['Sentiment_AVG'])


