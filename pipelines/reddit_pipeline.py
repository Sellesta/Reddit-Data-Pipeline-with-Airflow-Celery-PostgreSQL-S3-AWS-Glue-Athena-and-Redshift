from utils.constants import OUTPUT_PATH, SECRET, CLIENT_ID
from etls.reddit_etl import connect_reddit, extract_post, load_data_to_csv, transform_data
import pandas as pd

def reddit_pipeline(file_name:str, subreddit: str, time_filter: 'day', limit: None):
    # connecting to reddit instance
    instance = connect_reddit(CLIENT_ID, SECRET, 'Airscholor Agent')
    
    #extraction of the data
    
    posts = extract_post(instance, subreddit, time_filter, limit)
    
    post_df = pd.DataFrame(posts)
    
    post_df = transform_data(post_df)
    
    FilePath = f'{OUTPUT_PATH}/{file_name}.csv'
    
    load_data_to_csv(post_df, FilePath)
    
    return FilePath
    