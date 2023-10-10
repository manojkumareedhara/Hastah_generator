import pandas as pd
from googleapiclient.discovery import build
import sqlite3
# Load the dataframe
ddf = pd.read_csv("Webscraping/sports-1m-dataset/original/train_partition.txt", sep=" ", header=None, names=["URL", "Category"])

# Set up the YouTube API client
DEVELOPER_KEY = "AIzaSyCIFBvf1nKbFQJywQuv1wL12B2mZMSRTKk"  # Replace with your API key
#DEVELOPER_KEY = "AIzaSyB8IIaNhAhzWFMTN3VjT8WJ5_i9Pu7Rxm8"
#DEVELOPER_KEY = "AIzaSyAincf7sE-FEYfFsW07wq0rl5Inzy44AJk"
#DEVELOPER_KEY='AIzaSyCIFBvf1nKbFQJywQuv1wL12B2mZMSRTKk'
#DEVELOPER_KEY='AIzaSyCGYwGbWjoH_-lu9M0afNNL9PGUiC5YYFI'
#DEVELOPER_KEY='AIzaSyCSE3Me5wdY01do8CblzsZYQUfVBz-F-9w'

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
def init_db():
    conn = sqlite3.connect('video_details.db')
    cursor = conn.cursor()

    # Create the table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS videos (
        video_url TEXT PRIMARY KEY,
        title TEXT,
        description TEXT,
        tags TEXT,
        category_id INTEGER
    )
    ''')

    conn.commit()
    conn.close()

init_db() 
def save_to_db(video_url, details):
    conn = sqlite3.connect('video_details.db')
    cursor = conn.cursor()

    # Convert tags list to a string
    tags_str = ','.join(details['tags']) if details['tags'] else ''

    # Insert or update the record
    cursor.execute('''
    INSERT OR REPLACE INTO videos (video_url, title, description, tags, category_id)
    VALUES (?, ?, ?, ?, ?)
    ''', (video_url, details['title'], details['description'], tags_str, details['category_id']))

    conn.commit()
    conn.close()


# Function to get video details
# ... (your previous code)

def get_video_details(video_url):
    video_id = video_url.split("v=")[1]
    
    try:
        response = youtube.videos().list(part="snippet", id=video_id).execute()
    except Exception as e:
        print(f"Error fetching details for video: {video_url}. Error: {e}")
        return None  # Return None to indicate an error fetching details
    
    if 'items' in response and len(response['items']) > 0:
        video_details = {
            'title': response['items'][0]['snippet']['title'],
            'description': response['items'][0]['snippet']['description'],
            'tags': response['items'][0]['snippet'].get('tags', []),
            'category_id': response['items'][0]['snippet']['categoryId']
        }
        print('video fetched')
        return video_details
    else:
        print(f"Couldn't fetch details for video: {video_url} (it might be unavailable or private)")
        return None  # Return None to indicate the video is unavailable or private

# ...

# ...



# Extract details for each video in the dataframe
video_details_list = []
num=0
# This loop gets details for each video and saves them to the database
try:
    for video_url in range(100000,110000):# searched until 20000 
        print('Searcheed these many sites',video_url)
        details = get_video_details(ddf['URL'][video_url])
        num+=1
    
        if details:  # Only proceed if details were successfully fetched
            video_details_list.append(details)
            save_to_db(video_url, details)
            
 # Save individual video details to the database
except Exception as e:
    print(e)
finally:
    print(num)

# Convert video details list to DataFrame
details_df = pd.DataFrame(video_details_list)
print(details_df)
