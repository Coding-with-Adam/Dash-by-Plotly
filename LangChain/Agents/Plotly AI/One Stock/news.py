# code was very slightly modified. But originally written by Troy Scribner -- https://github.com/troyscribner
# https://github.com/troyscribner/stocknews/blob/main/dataqueries/alphavantage_queries.py
import pandas as pd
import requests
from pandas.tseries.offsets import DateOffset

date = pd.Timestamp.today() - DateOffset(days=10)
date = date.strftime('%Y%m%d')


def query_news(symbol, alphavantage_apikey):

    if symbol is None:
        url = 'https://www.alphavantage.co/query' \
              '?function=NEWS_SENTIMENT' \
              '&sort=RELEVANCE' \
              '&time_from=%sT0000' \
              '&topics=financial_markets' \
              '&limit=20' \
              '&apikey=%s' % (date, alphavantage_apikey)

    else:
        url = 'https://www.alphavantage.co/query' \
              '?function=NEWS_SENTIMENT' \
              '&sort=RELEVANCE' \
              '&time_from=%sT0000' \
              '&limit=20' \
              '&tickers=%s' \
              '&apikey=%s' % (date, symbol, alphavantage_apikey)

    if alphavantage_apikey == "demo":
        url = 'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=AAPL&apikey=demo'
        symbol = "AAPL"

    r = requests.get(url)
    data = r.json()

    df = pd.DataFrame(data['feed'])
    df = df.drop_duplicates(subset=['title'])

    def sentiment_filter(sentiments):
      return [x for x in sentiments if x['ticker'] == symbol][0]

    def split_relevance(x):
        return x['relevance_score']

    def split_sentiment(x):
        return x['ticker_sentiment_score']

    if symbol:
        df["ticker_sentiment"] = df["ticker_sentiment"].apply(sentiment_filter)
        df["relevance"] = df["ticker_sentiment"].apply(split_relevance)
        df["sentiment"] = df["ticker_sentiment"].apply(split_sentiment)
    else:
        df["relevance"] = 0.0
        df["sentiment"] = 0.0

    del df['ticker_sentiment']

    news_df = df[['title', 'summary', 'url', 'relevance', 'sentiment']]

    return news_df
