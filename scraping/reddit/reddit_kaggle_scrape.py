import pandas as pd
import os
import json
from datetime import datetime

# Define the directory and file names
directory = "kaggle_data"
file_names = [
    "reddit_opinion_climate_change.csv",
    "reddit_opinion_democrats.csv",
    "reddit_opinion_PSE_ISR.csv",
    "reddit_opinion_republican.csv"
]

# Total number of comments to sample
total_samples = 5000
before_samples = 1000
after_samples = 1000
recent_samples = 3000

# Function to check if comment has at least 100 words
def is_long_enough(comment):
    if isinstance(comment, str):
        return len(comment.split()) >= 100
    return False

# Collect all comments into a single DataFrame
all_comments = pd.DataFrame()

for file_name in file_names:
    file_path = os.path.join(directory, file_name)
    try:
        df = pd.read_csv(file_path, parse_dates=['created_time'], dtype={'self_text': str})
        df = df.dropna(subset=['self_text'])  # Drop rows where 'self_text' is NaN
        df = df[df['self_text'].apply(is_long_enough)]  # Keep only long comments
        df['source'] = file_name  # Add a source column
        all_comments = pd.concat([all_comments, df], ignore_index=True)
    except Exception as e:
        print(f"Could not process {file_name}: {e}")

# Define boundary dates
boundary_date_before = datetime(2022, 12, 31)
boundary_date_recent = datetime(2023, 6, 1)

# Filter comments into categories
before_comments = all_comments[all_comments['created_time'] <= boundary_date_before]
after_comments = all_comments[(all_comments['created_time'] > boundary_date_before) & (all_comments['created_time'] < boundary_date_recent)]
recent_comments = all_comments[all_comments['created_time'] >= boundary_date_recent]

# Sample comments
before_sampled = before_comments.sample(n=min(before_samples, len(before_comments)), random_state=1)
after_sampled = after_comments.sample(n=min(after_samples, len(after_comments)), random_state=1)
recent_sampled = recent_comments.sample(n=min(recent_samples, len(recent_comments)), random_state=1)

# Combine all samples into one DataFrame
all_sampled = pd.concat([before_sampled, after_sampled, recent_sampled], ignore_index=True)

# Create list of dictionaries for JSON output
comments_list = all_sampled[['created_time', 'self_text', 'source']].to_dict(orient='records')

# Define output file name
output_file_name = 'sampled_comments.json'
output_file_path = os.path.join(directory, output_file_name)

# Write to JSON file
with open(output_file_path, 'w') as json_file:
    json.dump(comments_list, json_file, indent=4, default=str)

print(f"Sampled comments saved to {output_file_path}")
