import json
import os
from datetime import datetime
# import random

def parse_experience_date(date_string):
    try:
        return datetime.strptime(date_string, '%B %d, %Y').strftime('%Y-%m-%d')
    except ValueError as e:
        print(f"Warning: Could not parse experience date: {date_string}")
        return date_string

def pre_process_raw_data():
    """Pre-process raw data files"""
    # Get absolute path to project root
    current_dir = os.path.dirname(os.path.abspath(__file__))  # /functions
    src_dir = os.path.dirname(current_dir)  # /src
    data_dir = os.path.join(src_dir, 'data')  # /src/data
    
    # Setup directories using absolute paths
    output_dir = os.path.join(data_dir, 'pre-processed-raw-data')
    raw_data_dir = os.path.join(data_dir, 'raw-trustpilot-data')
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Get the first JSON file from raw-trustpilot-data directory
    json_files = [f for f in os.listdir(raw_data_dir) if f.endswith('.json')]
    
    if not json_files:
        raise FileNotFoundError("No JSON files found in raw-trustpilot-data directory")
    
    input_path = os.path.join(raw_data_dir, json_files[0])
    # print(f"Processing file: {json_files[0]}")
    
    with open(input_path, 'r') as file:
        data = json.load(file)
    
    # Add count of reviews
    review_count = len(data)
    print(f"Found {review_count} reviews in source file")
    
    # Extract required fields
    processed_data = []
    for review in data:
        processed_review = {
            'reviewDateOfExperience': parse_experience_date(review['reviewDateOfExperience']),
            'reviewTitle': review['reviewTitle'],
            'reviewDescription': review['reviewDescription'],
            'reviewRatingScore': review['reviewRatingScore']
        }
        processed_data.append(processed_review)

    # Randomize order of reviews
    # random.shuffle(processed_data)
    # print("Randomized review order")
    
    # Generate output filename with timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    output_filename = f'processed_reviews_{timestamp}.json'
    output_path = os.path.join(output_dir, output_filename)
    
    # Save processed data
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(processed_data, file, indent=2, ensure_ascii=False)
        
    print(f"Successfully pre-processed and saved reviews.")

    return output_path
