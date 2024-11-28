import streamlit as st
import threading
import pandas as pd
import schedule
import src.scraping.twitter as twitter
from src.preprocessing_data.events import common_event_terms
import random
import time
import asyncio
from configparser import ConfigParser
from src.event_labeling.event_labeler import TweetEventLabeler
from src.event_labeling.utils import LightweightTimeExtractor
import os
from src.modeling.demo_model import get_sentiment_score
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from fuzzywuzzy import fuzz, process

import nltk
nltk.download('vader_lexicon', download_dir='nltk_data')

print("Hello World")
model_path = os.path.expanduser("~/.cache/huggingface/transformers/microsoft/phi-2")
if os.path.exists(model_path):
    print("Model 'microsoft/phi-2' is already downloaded.")
else:
    print("Model 'microsoft/phi-2' is not downloaded. Proceeding to run code.")

llm_labeler = LightweightTimeExtractor()

print("This is the model path: ", model_path)

predefined_events = [
        
    ]
custom_instruction = """
Analyze the following tweet and classify it into one of these predefined events: {events}.
If no predefined event matches, create a new event category that is concise and descriptive.

Tweet: {tweet}

Respond in JSON format:
{{"event": "event_name", "confidence": 0.0-1.0, "reasoning": "why you chose this category"}}
    """
    
print("Starting to label tweets")

try:
    nltk.data.find("vader_lexicon.zip")
    analyzer = SentimentIntensityAnalyzer()
except LookupError:
    nltk.download("vader_lexicon")

    analyzer = SentimentIntensityAnalyzer()
    
labeler = TweetEventLabeler(
        predefined_events=predefined_events,
        instruction_template=custom_instruction
)

# Set the page configuration
st.set_page_config(page_title="TAMU Sentiment Analysis", page_icon="📊")

def process_tweet(tweet):
    result = labeler.label_event(tweet, llm_labeler=llm_labeler)
    return {
        "tweet": tweet,
        "event": result["event"],
        "confidence": result["confidence"],
        "reasoning": result["reasoning"],
        "sentiment_score": get_sentiment_score(tweet)
    }



tracker = 0
# Define Data Scraping Job
def scheduled_job():
    """Scheduled job to scrape Twitter data."""
    global tracker
    # Get the data needed to gather Twitter data
    config = ConfigParser()
    with open('config.ini', 'r') as config_file:
        config.read_file(config_file)
    
    username = st.secrets['X']["username"]
    email = st.secrets['X']['email'] 
    password = st.secrets['X']['password'] 
    tracker = tracker + 1
    # Scrape Twitter data
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tweets = loop.run_until_complete(twitter.scrape_tweets(username=username,
                                                           password=password,
                                                           search_query="Texas A&M University",
                                                            filepath = 'data/raw-data/raw_tweets.csv'
                                                           ))
    print(f"Tracker: {tracker}")
    
    tweets = pd.read_csv('data/raw-data/raw_tweets.csv')
    print(tweets.head())
    print("Gotten Scraped Tweets")
    

    
    
    # Now I want to group these tweets by event
    # This is where the new code comes in!
    # Group tweets by event
    tweets = tweets.drop_duplicates(subset=['text'], keep='first').reset_index(drop=True)
    print(tweets.size)
    output_file = 'data/labeled_tweets.csv'
    batch_size = 100
    
    
    try:
        labeled_tweets_df = pd.read_csv(output_file)
        print(f"Loaded {len(labeled_tweets_df)} processed tweets from checkpoint.")
    except FileNotFoundError:
        labeled_tweets_df = pd.DataFrame(columns=["tweet", "event", "confidence", "reasoning", "sentiment_score"])
        print("No checkpoint found. Starting from scratch.")
        
    start_index = len(labeled_tweets_df)
    remaining_tweets = tweets.iloc[start_index:]
    
    for i in range(0, len(remaining_tweets), batch_size):
        batch = remaining_tweets.iloc[i:i + batch_size]
        
        print(f"Processing tweets {i} to {i + batch_size}...")
        
        batch_results = [process_tweet(tweet) for tweet in batch["text"]]
        batch_df = pd.DataFrame(batch_results)
        labeled_tweets_df = pd.concat([labeled_tweets_df, batch_df], ignore_index=True)
        
        labeled_tweets_df.to_csv(output_file, index=False)
        
        print(f"Batch {i // batch_size + 1} completed. Checkpoint saved.")
    
    print("All tweets processed and saved")
    # now we check if the labeled_tweets_df is more than 20000 rows, 
    # if it is erase the first rows till only 20000 rows are left
    if len(labeled_tweets_df) > 20000:
        labeled_tweets_df = labeled_tweets_df.iloc[-20000:]
    
    print("size has been checked")
    
    unique_events = data["event"].unique()

    # Create a dictionary for grouping similar events
    event_groups = {}
    for event in unique_events:
        if event_groups:  # Ensure event_groups is not empty
            # Find the closest match in existing groups
            result = process.extractOne(event, event_groups.keys(), scorer=fuzz.token_sort_ratio)
            if result is not None:  # Ensure a match was found
                closest_match, score = result
                if score > 35:  # Threshold for similarity (adjust as needed)
                    event_groups[closest_match].append(event)
                    continue
        # Add new group if no match or event_groups is empty
        event_groups[event] = [event]

    # Create a mapping dictionary for events to their group
    event_mapping = {event: group for group, events in event_groups.items() for event in events}
    labeled_tweets_df["event"] = labeled_tweets_df["event"].map(event_mapping)
    
    labeled_tweets_df.to_csv('data/labeled_tweets.csv', index=False)


def run_scheduler():
    schedule.every(30).seconds.do(scheduled_job)
    
    while True:
        schedule.run_pending()
        time.sleep(1)
        
# Start the scheduler thread
scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()

# Title and Introduction
st.title("Welcome to TAMU Sentiment Analysis")
st.write("Your go-to app for analyzing the sentiment of Texas A&M University-related content.")

# Brief description of the app's purpose
st.subheader("About This App")
st.write(
    """
    This application uses natural language processing to gauge the overall sentiment of 
    online discussions, news, and social media posts about Texas A&M University. The goal 
    is to provide insights into how people feel about TAMU, whether positive, negative, or neutral.
    
    Through data scraping and real-time analysis, we bring you a dashboard that reflects the current 
    public sentiment, helping TAMU students, faculty, and fans stay informed and engaged.
    """
)

# Overview of future features
st.subheader("Features")
st.write(
    """
    - **Sentiment Dashboard**: See real-time sentiment trends across various sources.
    - **Top Keywords**: Understand popular topics in discussions around TAMU.
    - **Interactive Visualizations**: Explore sentiment trends over time.
    """
)

# Navigation prompt
st.write("---")
st.write("Navigate to the **Dashboard** page to explore real-time data and insights!")

# Footer
st.write("Using Streamlit for TAMU Sentiment Analysis")
