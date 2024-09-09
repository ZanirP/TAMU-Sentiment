from twikit import Client
import twikit
import json
import pandas as pd
from configparser import ConfigParser
import asyncio  # Added for async operations

async def scrape_tweets(username, password):
    client = Client('en-US')

    try:
        # Login using your Twitter credentials
        await client.login(auth_info_1=username, password=password)
        
        print("TIME TO SCRAPE")

        timeline = await client.search_tweet('Texas A&M', 'Latest')
        
        print("GOT TIMELINE")
        
        tweets = []
        for tweet in timeline:
            tweets.append({
                "text": tweet.text,
                "timestamp": tweet.created_at,
                "likes": tweet.favorite_count,
                "retweets": tweet.retweet_count,
                # Add other fields as needed
            })
            print(tweet)
            
        print("GOT Tweets")

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

# Save tweets to a csv file
df = pd.DataFrame(tweets)
df.to_csv('tweets.csv', index=False)

'''
from bs4 import BeautifulSoup
from selenium import webdriver
import time



PATH = 'C:\Program Files (x86)\chromedriver.exe'



target_url = "https://twitter.com/scrapingdog"


driver=webdriver.Chrome(PATH)

driver.get(target_url)
time.sleep(5)



resp = driver.page_source
driver.close()

print(resp)
'''

'''
# Import necessary libraries
import requests
from bs4 import BeautifulSoup

# Define the URL of the Twitter page you want to scrape
url = "https://twitter.com/elonmusk"

# Make a request to the website
response = requests.get(url)

# Check for successful response (optional)
if response.status_code == 200:
    print("Successfully retrieved the page content.")
else:
    print(f"Error retrieving the page: {response.status_code}")
    exit()  # Exit the script if there's an error

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find all elements with the class 'tweet' (assuming tweets are wrapped in this element)
tweets = soup.find_all('div', class_='tweet')

# Loop through each tweet element
for tweet in tweets:
    # Find the element containing the tweet text
    text = tweet.find('p', class_='tweet-text').text
    # Extract the text content of that element
    text = text.strip()  # Remove any leading/trailing whitespace

    # Find the element containing the timestamp
    timestamp = tweet.find('span', class_='timestamp').text
    # Extract the text content of the timestamp element

    # Print the extracted information
    print(f"Text: {text}")
    print(f"Timestamp: {timestamp}")


'''





'''

from twikit import Client, TooManyRequests
import time
from datetime import datetime
import csv
from configparser import ConfigParser
from random import randint
import asyncio


MINIMUM_TWEETS = 10
QUERY = '(from:elonmusk) lang:en until:2020-01-01 since:2018-01-01'


def get_tweets(tweets):
    if tweets is None:
        #* get tweets
        print(f'{datetime.now()} - Getting tweets...')
        tweets = client.search_tweet(QUERY, product='Top')
    else:
        wait_time = randint(5, 10)
        print(f'{datetime.now()} - Getting next tweets after {wait_time} seconds ...')
        time.sleep(wait_time)
        tweets = tweets.next()

    return tweets


#* login credentials
config = ConfigParser()
config.read('config.ini')
username = config['X']['username']
email = config['X']['email']
password = config['X']['password']

#* create a csv file
with open('tweets.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Tweet_count', 'Username', 'Text', 'Created At', 'Retweets', 'Likes'])
    

#* authenticate to X.com
#! 1) use the login credentials. 2) use cookies.
client = Client(
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",
    )

async def main():
    try:
        client.load_cookies('cookies.json')
        print("Loaded cookies successfully")
    except Exception as e:
        print(f'Error loading cookies: {e}')
        try:
            await client.login(auth_info_1=username, auth_info_2=email, password=password)
            client.save_cookies('cookies.json')
            print("Login successful")
        except Exception as e:
            print(f'Login failed: {e}')
            
            
if __name__ == "__main__":
    asyncio.run(main())


client.load_cookies('cookies.json')

tweet_count = 0
tweets = None

while tweet_count < MINIMUM_TWEETS:

    try:
        tweets = get_tweets(tweets)
    except TooManyRequests as e:
        rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
        print(f'{datetime.now()} - Rate limit reached. Waiting until {rate_limit_reset}')
        wait_time = rate_limit_reset - datetime.now()
        time.sleep(wait_time.total_seconds())
        continue

    if not tweets:
        print(f'{datetime.now()} - No more tweets found')
        break

    for tweet in tweets:
        tweet_count += 1
        tweet_data = [tweet_count, tweet.user.name, tweet.text, tweet.created_at, tweet.retweet_count, tweet.favorite_count]
        
        with open('tweets.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(tweet_data)

    print(f'{datetime.now()} - Got {tweet_count} tweets')


print(f'{datetime.now()} - Done! Got {tweet_count} tweets found')
'''

