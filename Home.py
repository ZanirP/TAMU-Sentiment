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

print("Hello World")

# Set the page configuration
st.set_page_config(page_title="TAMU Sentiment Analysis", page_icon="📊")

tracker = 0
# Define Data Scraping Job
def scheduled_job():
    """Scheduled job to scrape Twitter data."""
    global tracker
    # Get the data needed to gather Twitter data
    config = ConfigParser()
    with open('config.ini', 'r') as config_file:
        config.read_file(config_file)
    
    username = config['X']['username']  # "ShiityGujju"
    email = config['X']['email']  # "zanirandzishan@gmail.com"
    password = config['X']['password']  # Replace with your actual password
    tracker = tracker + 1
    # Scrape Twitter data
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tweets = loop.run_until_complete(twitter.scrape_tweets(username=username, password=password, word="Texas A&M University"))
    print(f"Scraped {len(tweets)} tweets.")
    print(f"Tracker: {tracker}")


def run_scheduler():
    schedule.every(5).minutes.do(scheduled_job)
    
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
