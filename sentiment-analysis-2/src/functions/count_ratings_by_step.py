import json
import os
from glob import glob
from datetime import datetime
from collections import OrderedDict

def get_journey_steps() -> list:
    """Get ordered list of journey steps"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    journey_dir = os.path.join(os.path.dirname(current_dir), 'data', 'journey-steps')
    journey_files = glob(os.path.join(journey_dir, 'customer_journey_steps_*.json'))
    
    if not journey_files:
        raise FileNotFoundError("No journey steps file found")
    
    latest_file = max(journey_files, key=os.path.getctime)
    with open(latest_file, 'r') as f:
        data = json.load(f)
        return data.get("journeySteps", [])

def count_ratings_by_step() -> str:
    """Count ratings for each journey step and save results"""
    try:
        journey_steps = get_journey_steps()
        print(f"Found {len(journey_steps)} journey steps")
        
        # Load latest reviews
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(os.path.dirname(current_dir), 'data')
        input_dir = os.path.join(data_dir, 'summarized-reviews')
        latest_file = max(glob(os.path.join(input_dir, 'summarized_reviews_*.json')), key=os.path.getctime)
        
        with open(latest_file, 'r') as f:
            reviews = json.load(f)
        print(f"Processing {len(reviews)} reviews")
        
        # Initialize ordered ratings
        ratings = OrderedDict()
        for step in journey_steps:
            ratings[step] = OrderedDict()
        
        # Count ratings maintaining order
        for review in reviews:
            step = review['journeyStep']
            score = review['reviewRatingScore']
            
            if step in journey_steps:
                if score not in ratings[step]:
                    ratings[step][score] = 0
                ratings[step][score] += 1
        
        # Save ordered results
        output_dir = os.path.join(data_dir, 'ratings-by-step')
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f'ratings_by_step_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({"journeySteps": ratings}, f, indent=2, ensure_ascii=False)
        
        print(f"Saved ordered ratings to: {output_file}")
        return output_file
        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise