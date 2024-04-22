"""
This script contains funtions to initialize model 
and perform sentiment analysis on given dataset.
"""
import csv
import urllib.request
from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer
import numpy as np
from scipy.special import softmax
import pandas as pd

from dotenv import load_dotenv
load_dotenv()

def preprocess(text):
    """
    This function will preprocess the text data.
    """
    new_text = []
    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    return " ".join(new_text)

def init_model():
    """
    This function will initialize the model, tokenizer, and labels.
    """
    task='sentiment'
    MODEL = f"cardiffnlp/twitter-roberta-base-{task}" # change to local path
    tokenizer: AutoTokenizer = AutoTokenizer.from_pretrained(MODEL)

    # download label mapping
    labels: list[str] = []
    mapping_link = f"https://raw.githubusercontent.com/cardiffnlp/tweeteval/main/datasets/{task}/mapping.txt"
    with urllib.request.urlopen(mapping_link) as f:
        html = f.read().decode('utf-8').split("\n")
        csvreader = csv.reader(html, delimiter='\t')
    labels = [row[1] for row in csvreader if len(row) > 1]

    # PT
    model: AutoModelForSequenceClassification = AutoModelForSequenceClassification.from_pretrained(MODEL)
    tokenizer.save_pretrained(MODEL)
    model.save_pretrained(MODEL)

    return model, tokenizer, labels

# Function to get sentiment label for an input
def get_sentiment_label(tweet:str, model=None, tokenizer=None, labels=None):
    """
    This function will take a string as input and return the sentiment label.
    """
    if model is None or tokenizer is None or labels is None:
        # Initialize the model, tokenizer, and labels if not provided
        model, tokenizer, labels = init_model()

    tweet = preprocess(tweet)
    encoded_input = tokenizer(tweet, return_tensors='pt')
    output = model(**encoded_input)
    scores = output.logits[0].detach().numpy()
    scores = softmax(scores)
    sentiment_index = np.argmax(scores)  # Get index of the highest score
    return labels[sentiment_index]

def apply_sentiment_labels(df:pd.DataFrame)->pd.DataFrame:
    """
    This function will take a dataframe as input and return a dataframe with the sentiment.
    """
    # Apply sentiment analysis to each tweet in df and add sentiment label to the DataFrame
    df['Sentiment'] = df['Tweet'].apply(get_sentiment_label)

    return df

def apply_sentiment_labels_new(df:pd.DataFrame, col:str, model=None, tokenizer=None, labels=None)->pd.DataFrame:
    """
    This function will take a dataframe as input and return a dataframe with the sentiment.
    """
    # Initialize lists to store sentiment 
    sentiments = []

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        tweet = row[col]
        sentiment = get_sentiment_label(tweet, model, tokenizer, labels)
        sentiments.append(sentiment)

    # Add sentiments to the DataFrame
    df['Sentiment'] = sentiments

    return df

def get_sentiment_scores(tweet, model=None, tokenizer=None, labels=None):
    """
    This function will take a string as input and return the sentiment scores.
    """
    if model is None or tokenizer is None or labels is None:
        # Initialize the model, tokenizer, and labels if not provided
        model, tokenizer, labels = init_model()

    tweet = preprocess(tweet)
    encoded_input = tokenizer(tweet, return_tensors='pt')
    output = model(**encoded_input)
    scores = output.logits[0].detach().numpy()
    scores = softmax(scores)
    return {'Negative': scores[labels.index('negative')],
            'Neutral': scores[labels.index('neutral')],
            'Positive': scores[labels.index('positive')]}

def apply_sentiment_scores(df:pd.DataFrame)->pd.DataFrame:
    """
    This function will take a dataframe as input and return a dataframe with the sentiment.
    """
    # Apply sentiment analysis to each tweet in df 
    # and add Negative, Neutral and Positive label to the DataFrame
    df[['Negative', 'Neutral', 'Positive']] = df['Tweet'].apply(get_sentiment_scores).apply(pd.Series)

    return df

def apply_sentiment_scores_new(df:pd.DataFrame, col:str, model=None, tokenizer=None, labels=None)->pd.DataFrame:
    """
    This function will take a dataframe as input and return a dataframe with the sentiment.
    """
    # Initialize lists to store sentiment scores
    negative_scores = []
    neutral_scores = []
    positive_scores = []

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        tweet = row[col]
        scores = get_sentiment_scores(tweet, model, tokenizer, labels)
        negative_scores.append(scores['Negative'])
        neutral_scores.append(scores['Neutral'])
        positive_scores.append(scores['Positive'])

    # Add sentiment scores to the DataFrame
    df['Negative'] = negative_scores
    df['Neutral'] = neutral_scores
    df['Positive'] = positive_scores

    return df

def perform_sentiment_analysis(df:pd.DataFrame, col:str)->pd.DataFrame:
    """
    This function will perform sentiment analysis on the tweets for the specified stock.
    """
    try:
        model, tokenizer, labels = init_model()
    except Exception as e:
        print("failed loading model")
        print(e)
        exit()
    try:
        df=apply_sentiment_labels_new(df, col, model, tokenizer, labels)
        df=apply_sentiment_scores_new(df, col, model, tokenizer, labels)
    except Exception as e:
        print("failed sentiment analysis")
        print(e)
    return df
