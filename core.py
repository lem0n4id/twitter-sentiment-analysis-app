"""
Core functions for fetching tweets, news, and stock data and performing sentiment analysis.
"""
from datetime import datetime, timedelta
import pandas as pd
import yfinance as yf
from sentiment_analysis import perform_sentiment_analysis

def get_tweets(stock_name:str='TSLA')->pd.DataFrame:
    """
    This function will read the Stock Tweets for 
    dataset and return the dataframe.
    """
    # make sure the dataframe has the columns "Tweet" and "Date"
    stock_name=stock_name.upper()

    # TODO: optimize the API - web scraping
    # API call takes a long time
    # response = requests.get(f'http://127.0.0.1:8000/tweets/?ticker={stock_name}').json()
    # news: pd.DataFrame = pd.json_normalize(response)

    tweets = pd.read_csv("data/tsla_tweets.csv")
    tweets['Date'] = pd.to_datetime(tweets['Date'])

    return tweets

def tweets_within_hours(df:pd.DataFrame, datetime:str='2021-09-30 00:13:26+00:00', next_x_hours:int=24) -> pd.DataFrame:
    """
    This function will filter the tweets for the specified stock 
    and within the next x hours from the given datetime.
    """
    # Convert datetime string to datetime object
    datetime = pd.to_datetime(datetime)

    # Filter dataframe for the specified stock and within the next x hours from the given datetime
    # filtered_df = df[(df['Stock Name'] == stock_name) &
    #                  (df['Date'] >= datetime) &
    #                  (df['Date'] <= datetime + pd.Timedelta(hours=next_x_hours))]
    
    # filtered_df = df[(df['Date'] >= datetime) &
    #                  (df['Date'] <= datetime + pd.Timedelta(hours=next_x_hours))]
    
    filtered_df = df

    return filtered_df

def filter_unwanted_tweets(df: pd.DataFrame, ticker: str) -> pd.DataFrame:
    """
    This function will filter the tweets that contain the specified stock ticker.
    """
    keywords = ['$' + ticker.capitalize(), '$' + ticker.lower(), '$' + ticker.upper(),
                '#' + ticker.capitalize(), '#' + ticker.lower(), '#' + ticker.upper()]

    filtered_tweets = []

    for _, row in df.iterrows():
        tweet = row['Tweet']
        for keyword in keywords:
            if keyword in tweet:
                filtered_tweets.append(row)
                break  # Once a keyword is found, move to the next tweet
                # If you want to include multiple occurrences of the keyword in the same tweet, remove the break statement

    return pd.DataFrame(filtered_tweets)

def get_tweets_df(datetime:str='2021-09-30 00:13:26+00:00',stock:str='TSLA',next_x_hours:int=24)->pd.DataFrame:
    """
    This function will return the dataframe containing the tweets for the specified stock.
    """
    try:
        df=get_tweets(stock_name=stock)
        tweets_specified=tweets_within_hours(df, datetime=datetime, next_x_hours=next_x_hours)
        tweets_filtered=filter_unwanted_tweets(tweets_specified, ticker=stock)
        tweets_sentiments=perform_sentiment_analysis(tweets_filtered, "Tweet")
        print("Sentiment analysis of tweets success")
        return tweets_sentiments
    except Exception as e:
        # if loading the model fails
        print("Sentiment analysis of tweets failed")
        print(e)
        tweet_sentiments = pd.read_csv(r"data\TSLA tweets score.csv",parse_dates=['Date'], index_col=['Date'])
        return tweet_sentiments

def get_news(stock_name:str='TSLA')->pd.DataFrame:
    """
    This function will get news headlines for 
    given ticker and return the dataframe.
    """
    # make sure the dataframe has the columns "headlines", "datetime" and "link"
    stock_name=stock_name.lower()

    # TODO: optimize the API - web scraping
    # API call takes a long time
    # response = requests.get(f'http://127.0.0.1:8000/news/?ticker={stock_name}').json()
    # news: pd.DataFrame = pd.json_normalize(response)

    news: pd.DataFrame = pd.read_csv("data/tsla_headlines.csv")

    # TODO: write function to process the datetime column
    # news['datetime'] = pd.to_datetime(news['datetime'])

    return news

def news_within_hours(df:pd.DataFrame, datetime:str='2021-09-30 00:13:26+00:00', next_x_hours:int=24) -> pd.DataFrame:
    """
    This function will filter the news for the specified stock 
    and within the next x hours from the given datetime.
    """
    # Convert datetime string to datetime object
    # datetime = pd.to_datetime(datetime)

    # TODO: Filter dataframe for the specified stock and within the next x hours from the given datetime
    # filtered_df = df[(df['Stock Name'] == stock_name) &
    #                  (df['Date'] >= datetime) &
    #                  (df['Date'] <= datetime + pd.Timedelta(hours=next_x_hours))]
    
    # filtered_df = df[(df['Date'] >= datetime) &
    #                  (df['Date'] <= datetime + pd.Timedelta(hours=next_x_hours))]
    
    filtered_df = df

    return filtered_df

def get_news_df(datetime:str='2021-09-30 00:13:26+00:00',stock:str='TSLA',next_x_hours:int=24)->pd.DataFrame:
    """
    This function will return the dataframe containing the tweets for the specified stock.
    """
    try:
        df=get_news(stock_name=stock)
        news_specified=news_within_hours(df, datetime=datetime, next_x_hours=next_x_hours)
        news_sentiments=perform_sentiment_analysis(news_specified, "headlines")
        print("Sentiment analysis of news success")
        return news_sentiments
    except Exception as e:
        # if loading the model fails
        print("Sentiment analysis of news failed")
        print(e)
        # TODO: make a csv of already scored headlines
        news_sentiments = pd.read_csv(r"data\TSLA tweets score.csv",parse_dates=['Date'], index_col=['Date'])
        return news_sentiments

def get_stock_data(ticker:str, date:str="2021-09-30", days_around:int=7) -> pd.DataFrame:
    """
    This function will download the stock data for the specified ticker and date.
    """
    # make sure ticker is in upper case
    ticker=ticker.upper()

    # TODO: make sure the ticker is valid

    # Define the date
    date_obj = datetime.strptime(date, '%Y-%m-%d') # format of the date- yyyy-mm-dd

    # Calculate start and end dates
    start_date = (date_obj - timedelta(days=days_around)).strftime('%Y-%m-%d')
    end_date = (date_obj + timedelta(days=days_around)).strftime('%Y-%m-%d')

    try:
        # Download stock data for given ticker
        ticker_stock_data = yf.download(ticker, start=start_date, end=end_date, interval="1d")
        return ticker_stock_data
    except Exception as e:
        print("Error downloading the data from yfinance. Details: ")
        print(e)
        stock_prices = pd.read_csv(r"data\TSLA 14 days stock price.csv")
        return stock_prices
