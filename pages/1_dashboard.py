import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

# Placeholder Data (To be replaced with actual scraped data)
# Creating dummy data to demonstrate visualizations
data = {
    "Sentiment": ["Positive", "Neutral", "Negative"],
    "Count": [120, 80, 45]
}
df = pd.DataFrame(data)

# Display sentiment distribution in a bar chart
st.subheader("Sentiment Distribution")
fig, ax = plt.subplots()
df.set_index("Sentiment").plot(kind="bar", legend=False, ax=ax)
plt.ylabel("Count")
st.pyplot(fig)

# Line chart for sentiment over time (Placeholder data)
time_data = {
    "Time": pd.date_range(start="2023-01-01", periods=10, freq="D"),
    "Positive": [100, 120, 130, 140, 135, 145, 150, 160, 155, 165],
    "Neutral": [70, 75, 78, 80, 85, 88, 85, 90, 92, 95],
    "Negative": [30, 35, 40, 38, 36, 34, 33, 32, 31, 30]
}
time_df = pd.DataFrame(time_data)

st.subheader("Sentiment Trend Over Time")
fig, ax = plt.subplots()
time_df.plot(x="Time", ax=ax)
plt.ylabel("Count")
st.pyplot(fig)

# Keyword frequency section (To be populated with actual data in the future)
st.subheader("Top Keywords in TAMU Discussions")
keywords = {
    "Keyword": ["Aggies", "Football", "Research", "Campus", "Professors"],
    "Frequency": [95, 80, 60, 50, 45]
}
keyword_df = pd.DataFrame(keywords)
st.write(keyword_df)

# Footer
st.write("---")
st.write("Data sourced in real-time from various online platforms. Stay tuned for more insights!")
