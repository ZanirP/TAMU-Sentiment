import asyncio
import json
import pandas as pd
import os
from configparser import ConfigParser
import twikit
from twikit import Client


async def scrape_tweets(username, password):
    client = Client('en-US')

    try:
        # Login using your Twitter credentials
        await client.login(auth_info_1=username, password=password)

        print("TIME TO SCRAPE")

        timeline = await client.search_tweet('Texas A&M', 'Top')

        print("GOT TIMELINE")

        tweets = []
        for tweet in timeline:
            tweets.append({
                'text': tweet.text,
                'timestamp': tweet.created_at,
                'likes': tweet.favorite_count,
                'retweets': tweet.retweet_count,
                # Add other fields as needed
            })
            print(tweet)

        print("GOT TWEETS")

        return tweets

        # Logout (optional)
        await client.logout()

    except twikit.TooManyRequests as e:
        print(f"Rate limit reached: {e}")
        # Implement your rate limit handling strategy here

    except Exception as e:
        print(f"An error occurred: {e}")

# Read credentials from config file
config = ConfigParser()
config.read('config.ini')
username = config['X']['username']
email = config['X']['email']
password = config['X']['password']  # Replace with your actual password

# Run the scraper asynchronously
tweets = asyncio.run(scrape_tweets(username, password))
print("scrapper ran")

# Add tweets to a CSV file
# Define the file path
file_path = 'tweets.csv'

# Create a DataFrame from the tweets
df = pd.DataFrame(tweets)

# Check if the file already exists
if os.path.exists(file_path):
    # Append mode if the file exists
    df.to_csv(file_path, mode='a', header=False, index=False)
else:
    # Write mode if the file does not exist
    df.to_csv(file_path, mode='w', header=True, index=False)