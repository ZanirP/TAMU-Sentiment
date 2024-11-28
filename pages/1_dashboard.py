import streamlit as st
import pandas as pd
import os
import plotly.express as px

#variables
OUTPUT_FILE = "data/labeled_tweets.csv"
data = pd.read_csv(OUTPUT_FILE)


# Set page configuration
st.set_page_config(
    page_title="Dashboard",
    page_icon="📈",
)

# Title and Introduction
st.title("TAMU Sentiment Analysis Dashboard")
st.write("Explore real-time sentiment trends and insights about Texas A&M University.")

# Placeholder for scraped data
st.subheader("Current Sentiment Overview")
st.write("Sentiment data is being collected from various sources in real-time.")

event_counts = data["event"].value_counts()

# Sidebar - Event Selection
st.sidebar.title("Filter Events")
unique_events = data["event"].unique()
selected_events = []
st.sidebar.write("Select Events:")
for event in unique_events:
    default_value = event_counts[event] > 10
    if event == "event_name" or event == "If no predefined event matches":
        default_value = False
    if st.sidebar.checkbox(event, value=default_value):  
        selected_events.append(event)

if selected_events:
    filtered_data = data[data["event"].isin(selected_events)]
else:
    filtered_data = data  
    
st.subheader("Event Counts")
event_counts = filtered_data["event"].value_counts().reset_index()
event_counts.columns = ["event", "count"]

fig_event_counts = px.bar(
    event_counts,
    x = "event",
    y = "count",
    title = "The number of events",
    labels = {"event": "Event", "count": "Number of times mentioned"}
)
st.plotly_chart(fig_event_counts)


# Displaying Sentiment Score's by event
st.subheader("Average Sentiment Score by Event")
average_sentiment_by_event = filtered_data.groupby("event")["sentiment_score"].mean().reset_index()
fig_sentiment = px.bar(
    average_sentiment_by_event,
    x = "event",
    y = "sentiment_score",
    title = "Average Sentiment Score by Event",
    labels = {"event": "Event", "sentiment_score": "Average Sentiment Score"}
)
st.plotly_chart(fig_sentiment)


# Footer
st.write("---")
st.write("Data sourced in real-time from various online platforms. Stay tuned for more insights!")
