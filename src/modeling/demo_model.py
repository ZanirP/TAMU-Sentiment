# IMPORTS
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

import pandas as pd
import matplotlib.pyplot as plt
import os
import glob

# Initialize the VADER sentiment analyzer

def preprocess_text(text):
    """
    Preprocess the input text by tokenizing, removing stopwords, and lemmatizing.
    
    Parameters:
    text (str): The input text to preprocess.
    
    Returns:
    str: The preprocessed text.
    """

    # Tokenize the text
    tokens = word_tokenize(text.lower())
    
    # Remove stop words
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [token for token in tokens if token not in stop_words]
    
    # Lemmatize the tokens
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
    
    # Join the tokens back into a string
    processed_text = ' '.join(lemmatized_tokens)
    
    return processed_text


def get_sentiment_score(text):
    """
    Calculate the compound sentiment score for the given text using VADER.

    Parameters:
    text (str): The input text for which the sentiment score is to be calculated.

    Returns:
    float: The compound sentiment score, a value between -1 (most negative) 
           and 1 (most positive).
    """
    if not isinstance(text, str):
        return 0.0
    return analyzer.polarity_scores(text)['compound']

def get_average_sentiment_by_event(df, event_column, sentiment_column, output_file=None):
    """
    Calculate the average sentiment score for each event in the DataFrame.
    
    Parameters:
    df (pd.DataFrame): Input DataFrame containing events and sentiment scores.
    event_column (str): Column name for the event (grouping criteria).
    sentiment_column (str): Column name for the sentiment scores.
    output_file (str, optional): File path to save the results as a CSV. If None, the results are not saved.
    
    Returns:
    pd.DataFrame: DataFrame containing events and their average sentiment scores.
    """
    # Ensure the sentiment column contains numeric values and drop NaNs
    df_clean = df.dropna(subset=[sentiment_column])
    
    # Group by the event column and calculate the average sentiment for each group
    sentiment_averages = df_clean.groupby(event_column)[sentiment_column].mean().reset_index()

    # Optionally save the result to a CSV file
    if output_file:
        sentiment_averages.to_csv(output_file, index=False)
    
    return sentiment_averages

def organize_and_save_plot(xlabel, ylabel, title, save_directory, file_name, x_rotation=45):
    """
    Organize the plot by adding labels, title, and save the plot to a directory.
    
    Parameters:
    plot (matplotlib plot object): The plot object to modify and save.
    xlabel (str): The label for the x-axis.
    ylabel (str): The label for the y-axis.
    title (str): The title of the plot.
    save_directory (str): The directory where the plot should be saved.
    file_name (str): The name of the file (with extension) to save the plot.
    x_rotation (int): The rotation angle for the x-axis labels (default is 45 degrees).
    
    Returns:
    None
    """
    # Add labels and title
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    
    # Rotate x-axis labels
    plt.xticks(rotation=x_rotation, ha="right")
    
    # Adjust the figure size for better readability with more events
    plt.gcf().set_size_inches(12, 8)
    
    plt.tight_layout() # this is simply to make sure everything fits
    
    # Ensure the directory exists
    os.makedirs(save_directory, exist_ok=True)
    
    # Define the full path to save the plot
    save_path = os.path.join(save_directory, file_name)
    
    # Save the plot
    plt.savefig(save_path)
    
    
    print(f"Plot saved to {save_path}")
    # Clear the plot to free up memory
    plt.clf()
    


if __name__ == "__main__":
	# nltk.download('all') # If you don't like the rest of it!
	
    analyzer = SentimentIntensityAnalyzer()
    preprocessed_data_dir = 'data/processed-data'
    data_files = glob.glob(os.path.join(preprocessed_data_dir, "*.csv"))

    for file in data_files:
        df = pd.read_csv(file)
        df = df[df['preprocessed_text'].apply(lambda x: isinstance(x, str))]
        df['preprocessed_text'] = df['preprocessed_text'].apply(preprocess_text)
        nan_count = df['preprocessed_text'].isna().sum()
        print(f"Number of NaN values in 'preprocessed_text': {nan_count}")
        df['sentiment_score'] = df['preprocessed_text'].apply(get_sentiment_score)
        df1 = get_average_sentiment_by_event(df, 'event', 'sentiment_score')
        save_directory = "/home/hasnat79/TAMU-Sentiment/data/output_graphs/demo_graphs"
        file_name = file.split("/")[-1].replace(".csv", "_bar_plot.png")
        barplot1 = plt.bar(df1['event'], df1['sentiment_score'])
        organize_and_save_plot("Events", "Sentiment Scores", "Scores of Events", save_directory, file_name)



	# df = pd.read_csv("/home/hasnat79/TAMU-Sentiment/data/processed-data/tweets.csv")
	# df = df[df['preprocessed_text'].apply(lambda x: isinstance(x, str))]
	# df['preprocessed_text'] = df['preprocessed_text'].apply(preprocess_text)
	
    
	# nan_count = df['preprocessed_text'].isna().sum()
	# print(f"Number of NaN values in 'preprocessed_text': {nan_count}")


	# df['sentiment_score'] = df['preprocessed_text'].apply(get_sentiment_score)
	
	# df1 = get_average_sentiment_by_event(df, 'event', 'sentiment_score')
	# save_directory = "/home/hasnat79/TAMU-Sentiment/data/output_graphs/demo_graphs_wo_nan"
	# barplot1 = plt.bar(df1['event'], df1['sentiment_score'])

	
	# organize_and_save_plot("Events", "Sentiment Scores", "Scores of Events", save_directory, "barplot1.png")

	

