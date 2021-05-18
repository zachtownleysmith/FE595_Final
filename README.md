# FE595_Final

Our service is a "Sentiment Search Engine" which takes a stock ticker, sentiment package, and number of articles as an input, using an HTML render template form to pass the POST request. What is returned to the user is a listing of article titles, descriptions, the requested sentiment polarity on that description, the article URL, and the average sentiment for all articles.

The code uses yfinance to get the company name from the submitted ticker, and if the requested ticker is not found in yfinance than the search is completed on the submitted text. The article retrieval is handled using calls to Microsoft's Bing Search API. In the event that the user passes a request for an article count which is not an integer, the default is 5.

A get request to our endpoint takes the user back to the input page for completing another set of searches. This is also linked via a "new search" button that can be clicked on the results page.

The service is running detached at the following endpoint, if anyone wanted to take a look / test out our service.

http://18.191.148.88:8000/getSentiment
