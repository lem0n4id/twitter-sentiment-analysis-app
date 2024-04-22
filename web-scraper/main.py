import pandas as pd
from fastapi import FastAPI, HTTPException, Query, Response
from scraper_nasdaq import get_nasdaq_headlines_df
from scraper_twitter import get_tweets_df

app = FastAPI(
    title="Web Scraper API",
    description="API to scrap news headlines and tweets of a stock",
    version="0.1",
)


@app.get("/")
def index()-> dict[str,str]:
    return {"message": "Web Scraper API is running!!"}

df = pd.read_csv(r"..\data\tsla_tweets.csv")

@app.get("/tweets-example/")
def retrive_sample_tweets_for_ticker():
    return Response(df.to_json(orient="records"), media_type="application/json")

@app.get("/tweets/")
def retrive_tweets_for_ticker(ticker: str | None = Query(default=None, min_length=1, max_length=10)):
    if ticker is None:
        raise HTTPException(status_code=400, detail="Ticker is required")
    try:
        tweets_df=get_tweets_df(ticker)
    except Exception:
        return HTTPException(status_code=500, detail="Retrival of tweets failed")
    return Response(tweets_df.to_json(orient="records"), media_type="application/json")

@app.get("/news/")
def retrive_news_for_ticker(ticker: str | None = Query(default=None, min_length=1, max_length=10)):
    if ticker is None:
        raise HTTPException(status_code=400, detail="Ticker is required")
    try:
        news_df=get_nasdaq_headlines_df(ticker)
    except Exception:
        return HTTPException(status_code=500, detail="Retrival of news failed")
    return Response(news_df.to_json(orient="records"), media_type="application/json")
