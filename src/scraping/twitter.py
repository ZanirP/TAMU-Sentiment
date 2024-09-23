import asyncio
import json
import pandas as pd
import os
from configparser import ConfigParser
import twikit
from twikit import Client

def save_tweets(tweets, file_path):
    """
    Save a list of tweets to a CSV file.
    This function takes a list of tweets and saves them to a specified CSV file.
    If the file already exists, the tweets are appended to the file. If the file
    does not exist, a new file is created.
    Parameters:
    tweets (list): A list of tweet dictionaries to be saved.
    file_path (str): The path to the CSV file where the tweets will be saved.
    Returns:
    None
    """

    # Create a DataFrame from the tweets
    df = pd.DataFrame(tweets)

    # Check if the file already exists
    if os.path.exists(file_path):
        # Append mode if the file exists
        df.to_csv(file_path, mode='a', header=False, index=False)
    else:
        # Write mode if the file does not exist
        df.to_csv(file_path, mode='w', header=True, index=False)

async def scrape_tweets(username, password, filepath):
    client = Client('en-US')

    try:
        # Login using your Twitter credentials
        await client.login(auth_info_1=username, password=password)
        tweets = []

        print("TIME TO SCRAPE")

        timeline = await client.search_tweet('#12thMan', 'Top')

        print("GOT TIMELINE")

        n_passes = 80 # Number of passes
        
        for i in range(n_passes):
            for tweet in timeline:
                tweets.append({
                    'text': tweet.text,
                    'timestamp': tweet.created_at,
                    'likes': tweet.favorite_count,
                    'retweets': tweet.retweet_count,
                    # Add other fields as needed
                })
            print(f"pass: {i}, total tweets: \t {len(tweets)}")
            if i == 40:
                save_tweets(tweets, filepath)
                tweets = []
                await asyncio.sleep(900)  # Wait for 15 minutes (900 seconds)

            timeline = await timeline.next()


        print("GOT TWEETS")

        # Logout (optional)
        await client.logout()

    except twikit.TooManyRequests as e:
        print(f"Rate limit reached: {e}")
        # Implement your rate limit handling strategy here


    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    

    # Read credentials from config file
    config = ConfigParser()
    config.read('TAMU-Sentiment/config.ini')
    username = config['X']['username']
    email = config['X']['email']
    password = config['X']['password']  # Replace with your actual password

    file_path = 'TAMU-Sentiment/data/raw-data/hs_tweets_12thman.csv'

    # Run the scraper asynchronously
    tweets = asyncio.run(scrape_tweets(username, password,file_path))
    print("scrapper ran")

    # Add tweets to a CSV file
    # Define the file path

    save_tweets(tweets, file_path)
    print("tweets saved")
