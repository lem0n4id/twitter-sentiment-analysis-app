"""
This script contrains the main code for the streamlit app. 

Run python -m streamlit run main.py to run the app.
"""
import time
import streamlit as st
import pandas as pd
import plotly.express as px
from utils import get_sentiment_score
from core import get_tweets_df, get_news_df, get_stock_data
from sentiment_analysis import perform_sentiment_analysis

# Page title
st.set_page_config(page_title='Sentimental Analysis', page_icon='🤖')
st.title('📈 Sentimental Analysis')

option = st.selectbox(
    'Choose the required stock',
    ('TSLA', 'XYZ'), index=None, placeholder="Select...",)

st.write('You selected:', option)


if option=='TSLA':

    with st.spinner('Performing Sentiment Analysis...'):
        TSLA_tweet_sentiments = get_tweets_df(
            datetime='2024-04-22 00:00:00+00:00',stock='TSLA',next_x_hours=24
        )
        TSLA_news_sentiments = get_news_df(
            datetime='2024-04-22 00:00:00+00:00',stock='TSLA',next_x_hours=24
        )
        time.sleep(2)
    st.success('Done!')

    # sentiment of tweets
    
    # TODO: date hould be dynamic
    st.header("Tweets of TSLA stock on 21st April 2024")

    # show the tweets
    TSLA_tweet_sentiments_output=TSLA_tweet_sentiments[['Tweet','Sentiment']]
    st.markdown(f"{len(TSLA_tweet_sentiments_output)} Tweets found")
    TSLA_tweet_sentiments_output

    # sentiment score of tweets
    tweet_sentiment_score, tweet_total_positive, tweet_total_neutral, tweet_total_negative=get_sentiment_score(TSLA_tweet_sentiments)
    st.header(f"Sentiment score of tweets: {round(tweet_sentiment_score,2)}")
    st.write("Scale: -1 to 1")

    # number of positive, negative and neutral tweets
    st.markdown(f"Number of positive tweets: _**{tweet_total_positive}**_")
    st.markdown(f"Number of neutral tweets: _**{tweet_total_neutral}**_")
    st.markdown(f"Number of negative tweets: _**{tweet_total_negative}**_")

    # box - positive, negative, neutral
    if tweet_sentiment_score>0.2:
        st.success("The sentiment score is positive")
    elif tweet_sentiment_score<-0.2:
        st.error("The sentiment score is negative")
    else:
        st.warning("The sentiment score is neutral")
    
    # sentiment of news
    
    # TODO: date hould be dynamic
    st.header("News Headlines of TSLA stock on 21st April 2024")

    # show the news
    TSLA_news_sentiments_output=TSLA_news_sentiments[['headlines','Sentiment']]
    st.markdown(f"{len(TSLA_news_sentiments_output)} News Headlines found")
    TSLA_news_sentiments_output

    
    # sentiment score of news
    news_sentiment_score, news_total_positive, news_total_neutral, news_total_negative=get_sentiment_score(TSLA_news_sentiments)
    st.header(f"Sentiment score of news: {round(news_sentiment_score,2)}")
    st.write("Scale: -1 to 1")

    # add number of positive, negative and neutral news
    st.markdown(f"Number of positive news: _**{news_total_positive}**_")
    st.markdown(f"Number of neutral news: _**{news_total_neutral}**_")
    st.markdown(f"Number of negative news: _**{news_total_negative}**_")

    # box - positive, negative, neutral
    if news_sentiment_score>0.2:
        st.success("The sentiment score is positive")
    elif news_sentiment_score<-0.2:
        st.error("The sentiment score is negative")
    else:
        st.warning("The sentiment score is neutral")


    # Create a DataFrame combining tweet and news sentiments
    sentiment_comparison = pd.DataFrame({
        'Sentiment': ['Positive', 'Neutral', 'Negative'],
        'Tweets': [tweet_total_positive, tweet_total_neutral, tweet_total_negative],
        'News': [news_total_positive, news_total_neutral, news_total_negative]
    })

    # Melt the DataFrame to long format for Plotly Express
    sentiment_comparison_melted = sentiment_comparison.melt(id_vars=['Sentiment'], var_name='Source', value_name='Count')

    # Plotting
    fig = px.bar(sentiment_comparison_melted, x='Sentiment', y='Count', color='Source',
                barmode='group', labels={'Sentiment': 'Sentiment', 'Count': 'Count'},
                title='Sentiment Distribution of News and Tweets')
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)


    # stock price graph
    days = st.selectbox(
    'Choose the days',
    ('7d', '14d', '28d', '60d', '90d', '180d'), index=5, placeholder="Select...",)
    
    days=int(days[:-1])
    st.header(f"Price of TSLA stock {days} days around 21-04-2024")

    st.markdown("Interval: 1d")
    st.markdown("Source: Yahoo Finance")
    try:
        TSLA_stock_prices = get_stock_data("TSLA",date="2024-04-21",days_around=days)
        fig=px.line(TSLA_stock_prices,y="Close")
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    except Exception as e:
        print("error w yfinance")
        print(e)
        TSLA_stock_prices = pd.read_csv(r"data\TSLA 14 days stock price.csv")
        fig=px.line(TSLA_stock_prices,x="Date",y="Close")
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
        
    

else:
    st.markdown("Choose the required stock")