import pandas as pd
import spacy
from collections import defaultdict
import re
import os
import sys
import glob


# nlp = spacy.load("en_core_web_sm")
common_event_terms = [
    # Football-related events
    "football game", "offseason", "Transfer", "scrimmage", "spring game", "home game", "away game", 
    "rivalry game", "SEC Championship", "bowl game", "Texas Bowl", "Orange Bowl", "Cotton Bowl",
    "practice", "training camp", "team practice", "two-a-days", "kickoff", "overtime", "tailgate",
    "touchdown", "field goal", "punt return", "halftime show", "post-game", "pre-game", "playoffs",
    
    # Texas A&M Football Opponents (2024 Season)
    "Alabama", "Arkansas", "Auburn", "Florida", "Georgia", "LSU", "Mississippi State", 
    "Ole Miss", "South Carolina", "Tennessee", "Vanderbilt", "Miami", "New Mexico", 
    "Louisiana-Monroe", "Abilene Christian",
    
    # Traditions and rituals
    "Midnight Yell", "12th Man", "Aggie Muster", "Silver Taps", "Aggie Ring Day", "Fish Camp", 
    "Elephant Walk", "Maroon Out", "Reveille", "Bonfire", "Aggie Ring Dunk", "Howdy Week", 
    "Ring Dance", "Aggie War Hymn", "Wildcat", "Big Event", "Reunion Weekend", "Aggie Family Weekend",
    "Century Tree", "Aggie Ring", "Aggie Code of Honor", "MSC Open House", "Kyle Field Day", 
    "Yell Leaders", "Gig 'em", "Aggie Gameday", "March-In", "Corps of Cadets March-In", "Aggie Band",
    
    # Other Texas A&M sports events
    "basketball game", "baseball game", "softball game", "volleyball game", "soccer match", 
    "swim meet", "track and field meet", "cross country race", "equestrian meet", "tennis match",
    "golf tournament", "SEC Tournament", "tournament", "gymnastics meet", "rowing regatta", 
    "Aggie Classic", "Maroon & White Game", "NCAA Championship", "Rodeo", "3-on-3 tournament",
    "fight song"
    
    # Campus activities and events
    "graduation", "commencement", "study abroad", "study night", "campus tour", "New Student Conference", 
    "MSC Town Hall", "class reunion", "homecoming", "career fair", "job fair", "club meeting", 
    "club fair", "Greek Life event", "Intramural sports", "campus party", "engineering expo", 
    "campus concert", "student organization meeting", "lecture", "seminar", "workshop", "open mic night",
    
    # Notable speakers and events
    "guest speaker", "distinguished lecture series", "motivational speaker", "keynote address", 
    "leadership summit", "TedxTAMU", "research symposium", "career symposium", "alumni event",
    
    # Social events and celebrations
    "Ring Dance", "barn dance", "homecoming dance", "Spring Fest", "Howdy Week", "Chili Cook-off",
    "Tailgate Cook-off", "Halloween Bash", "Thanksgiving Dinner", "Valentine's Day Dance", 
    "Christmas at TAMU", "Winter Wonderland", "Game Night", "Aggie Ice Cream Social", "barbecue",
    
    # Competitions and exhibitions
    "Hackathon", "Case Competition", "coding competition", "Robotics Competition", "Research Expo", 
    "Science Fair", "Business Plan Competition", "pitch competition", "poster presentation", 
    "Art Exhibition", "Photography Contest", "Film Screening", "Talent Show", "Trivia Night",
    
    # Academic events
    "midterm exams", "final exams", "study session", "study group", "review session", "Capstone Presentation",
    "Thesis Defense", "Dissertation Defense", "Research Day", "Poster Presentation", "Lab Open House",
    
    # Corps of Cadets events
    "March to the Brazos", "Cadet Picnic", "Cadet Initiation", "Final Review", "Corps BBQ", 
    "Boot Dance", "Aggie Review", "Military Ball", "Pass in Review", "Field Training Exercise",
    
    # Organizations and Greek Life
    "fraternity party", "sorority social", "chapter meeting", "philanthropy event", 
    "fundraiser", "pledge ceremony", "initiation ceremony", "charity drive", "Greek Week", 
    "recruitment event", "sisterhood retreat", "brotherhood retreat", "volunteer event",
    
    # Special dates and campus services
    "Freshman Orientation", "Campus Tour", "Aggieland Market", "Ring Ceremony", 
    "MSC Open House", "MSC Film Series", "MSC Fliers", "Health and Wellness Fair", 
    "Blood Drive", "Stress Relief Week", "Finals Week", "Aggie Replant Day",
    
    # Recreational and other social events
    "movie night", "Aggie Cinema", "Outdoor Adventure", "camping trip", "hiking trip", 
    "kayaking trip", "Aggie Climbing Club", "dance workshop", "cooking class", 
    "Potluck Dinner", "game night", "poker tournament", "Ping Pong Tournament", "Board Game Night",
    
    # Athletics Facilities Events
    "Kyle Field Event", "Reed Arena Event", "Blue Bell Park Event", "Davis Diamond Event", 
    "Olsen Field Event", "Aggie Soccer Complex", "Nash Indoor Arena", "Aggie Tennis Center",
    
    # Others
    "t-shirt giveaway", "spirit rally", "pep rally", "ring day", "class ring ceremony", 
    "class gift dedication", "class of 2024", "Howdy", "Kyle Field", "Gameday Tailgate", 
    "Aggieland Saturday", "Aggie Trivia", "football season opener", "closing ceremony"
]




def update_event_dictionary(text, event_dict):
    """
    Updates a dictionary with events occurring in the given text.

    This function uses spaCy's Named Entity Recognition (NER) to identify events
    mentioned in the text and updates a dictionary that keeps track of all events 
    and their occurrence counts.

    Args:
        text (str): The input text from which to identify events.
        event_dict (defaultdict): A dictionary to store and count occurrences of events.

    Returns:
        None
    """
    for term in common_event_terms:
        if term.lower() in str(text).lower(): # used str() to convert numberical vals to string
            event_dict[term] += 1


# Function to process a batch of data and build the event dictionary
def build_event_dictionary(data):
    """
    Builds a dictionary of events from a batch of data.

    Args:
        data (list of str): A list of text entries representing data from online sources.

    Returns:
        dict: A dictionary containing identified events and their occurrence counts.
    """
    event_dict = defaultdict(int)
    for text in data['text']:
        update_event_dictionary(text, event_dict)
    
    return dict(event_dict)





def identify_event(text):
    """
    Identifies the event mentioned in the given text by checking the predefined list
    Our list is extensive enough that there is no need for other things

    Args:
        text (str): The input text in which to identify events.

    Returns:
        str: The name of the identified event if found, otherwise "Other".
    """    
    # Fallback keyword search for known events
    for event in events.keys():
<<<<<<< HEAD
        if event.lower() in str(text).lower(): # used str() to convert numberical vals to string
=======
        if event.lower() in text.lower():
>>>>>>> Zanir_Examples
            return event
        
    return "Other / Unknown"
        
        
def preprocess_text(text):
    """
    Preprocesses a single piece of text by cleaning and removing unnecessary elements,
    including mentions (@username), URLs, special characters, and extra spaces.
    
    Args:
        text (str): The input text to preprocess.
    
    Returns:
        str: The cleaned and preprocessed text.
    """
    # Convert text to lowercase
    text = str(text).lower() # used str() to convert numberical vals to string
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove @mentions along with the username
    text = re.sub(r'@\w+', '', text)
    
    # Remove special characters, numbers, and punctuations
    text = re.sub(r'[^a-z\s]', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

    

def group_and_preprocess(df):
    """
    Groups the DataFrame by 'event' and preprocesses the 'text' for each group.
    
    Args:
        df (pd.DataFrame): The input DataFrame containing 'text' and 'event' columns.
    
    Returns:
        df (pd.DataFrame): A DataFrame with 'event' and 'preprocessed_text' columns.
    """
    # Create an empty list to store the results
    processed_data = []

    # Group the DataFrame by 'event'
    grouped_df = df.groupby("event")
    
    # Iterate over each group
    for event, group in grouped_df:
        # Preprocess all texts in the current group
        group['preprocessed_text'] = group['text'].apply(preprocess_text)
        
        # Append the preprocessed data to the list
        processed_data.append(group[['event', 'preprocessed_text']])
    
    # Combine all the processed data back into a single DataFrame
    processed_df = pd.concat(processed_data, ignore_index=True)
    
    return processed_df

def get_concat_data_frame_from_data_dir (data_dir):
    """
    Get a concatenated data frame from all the csv files in the data_dir
    
    Args:
        data_dir (str): The directory containing the csv files
    
    Returns:
        df (pd.DataFrame): A DataFrame with all the data from the csv files
    """
    files = glob.glob(os.path.join(data_dir, "*.csv"))
    df_list = [pd.read_csv(file_path) for file_path in files]
    df = pd.concat(df_list, ignore_index=True)
    
    return df

def preprocess_on_data(data_dir, output_dir_path, ignore_nan = True):
    """
    Preprocess the data in the hasnat_data_dir and save it to the output_file_path
    
    Args:
        hasnat_data_dir (str): The directory containing the csv files
        output_file_path (str): The file path to save the preprocessed data
    
    Returns:
        None
    """
    output_file_path = os.path.join(output_dir_path, "data_preprocessed.csv")
    
    # Get all CSV files in the data_dir and its subdirectories
    files = glob.glob(os.path.join(data_dir, '**', '*.csv'), recursive=True)
    
    df_list = [pd.read_csv(file_path) for file_path in files]
    df = pd.concat(df_list, ignore_index=True)
    
    global events
    events = build_event_dictionary(df)
    df['event'] = df['text'].apply(identify_event)
    
    grouped_and_preprocessed_df = group_and_preprocess(df)

    if ignore_nan:
        grouped_and_preprocessed_df = grouped_and_preprocessed_df[~grouped_and_preprocessed_df['preprocessed_text'].str.contains("nan")]
        output_file_path = output_file_path.replace(".csv", "_without_nan.csv")
    
    grouped_and_preprocessed_df.to_csv(output_file_path)



        
if __name__ == "__main__":
    output_dir_path = "/data/processed-data/"
    ## DATA
    data_dir = "/data/raw-data/"
    preprocess_on_data(data_dir, output_dir_path, ignore_nan = True)
    


    
    
    