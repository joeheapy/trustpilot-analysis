import json
import os
from glob import glob
from datetime import datetime
from openai import OpenAI
from typing import List, Dict

# Constants
BATCH_SIZE = 5
MAX_BATCHES = 15  # Set maximum number of batches to process

print(f"Processing {BATCH_SIZE * MAX_BATCHES} reviews")

# Define prompt as constant
SUMMARY_PROMPT = """
Using the provided journey steps, analyze this review and:
1. Create a summary of the reviewDescription in maximum three sentances.
2. Assign the most relevant journey step to each reviewSummary.

Return ONLY this JSON structure:
{
    "reviewSummary": "<your generated summary>",
    "journeyStep": "<matching journey step from provided list>"
}

Rules:
- Keep emotional content in the summary if relevant.
- Each review MUST be assigned to exactly one journey step.
- Use original journey step text exactly as provided.

"""

def get_latest_journey_steps():
    """Get latest journey steps file content"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    journey_dir = os.path.join(os.path.dirname(os.path.dirname(current_dir)), 'src', 'data', 'journey-steps')
    journey_files = glob(os.path.join(journey_dir, 'customer_journey_steps_*.json'))
    
    if not journey_files:
        raise FileNotFoundError("No journey steps file found")
    
    latest_file = max(journey_files, key=os.path.getctime)
    with open(latest_file, 'r') as f:
        return json.load(f)


def chunk_reviews(reviews: list, batch_size: int = BATCH_SIZE) -> list:
    """Split reviews into chunks of specified size"""
    return [reviews[i:i + batch_size] for i in range(0, len(reviews), batch_size)]


def summarize_review() -> str:
    """Add AI-generated summaries and journey steps to reviews"""
    
    # Get journey steps
    journey_steps = get_latest_journey_steps()
    
    # Setup paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.dirname(current_dir)
    data_dir = os.path.join(src_dir, 'data')
    
    input_dir = os.path.join(data_dir, 'pre-processed-raw-data')
    output_dir = os.path.join(data_dir, 'summarized-reviews')
    os.makedirs(output_dir, exist_ok=True)
    
    # Get latest processed reviews file
    json_files = glob(os.path.join(input_dir, 'processed_reviews_*.json'))
    if not json_files:
        raise FileNotFoundError("No processed review files found")
    
    input_file = max(json_files, key=os.path.getctime)
    # print(f"Reading from: {input_file}")
    
    # Initialize OpenAI
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    # Read reviews
    with open(input_file, 'r') as f:
        reviews = json.load(f)
    
    # Setup output file with timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    output_filename = f'summarized_reviews_{timestamp}.json'
    output_path = os.path.join(output_dir, output_filename)
    
    # Process reviews in batches
    batches = chunk_reviews(reviews, BATCH_SIZE)
    total_batches = min(len(batches), MAX_BATCHES)
    summarized_reviews = []
    
    print(f"Processing {MAX_BATCHES * BATCH_SIZE} reviews in {total_batches} batches")
    # print("First batch content:")
    # print(json.dumps(batches[0], indent=2))
    print("Starting batch processing...\n")
    
    for batch_num in range(1, total_batches + 1):
        try:
            print(f"Processing batch {batch_num}/{total_batches}")
            batch_summaries = []
            
            for review in batches[batch_num - 1]:
                response = client.chat.completions.create(
                    model="gpt-4-turbo-preview",
                    messages=[
                        {"role": "system", "content": "You are a review analysis expert."},
                        {"role": "user", "content": f"Journey Steps:\n{json.dumps(journey_steps, indent=2)}\n\n{SUMMARY_PROMPT}\n\nReview: {review['reviewDescription']}"}
                    ],
                    response_format={"type": "json_object"}
                )
                
                # Get processed data from response
                result = json.loads(response.choices[0].message.content)
                
                # Update review with new fields
                review['reviewSummary'] = result['reviewSummary']
                review['journeyStep'] = result['journeyStep']
                del review['reviewDescription']
                
                batch_summaries.append(review)
            
            # Append batch to output file
            summarized_reviews.extend(batch_summaries)
            
            # Save progress after each batch
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(summarized_reviews, f, indent=2, ensure_ascii=False)
            
            print(f"Completed batch {batch_num}/{total_batches}")
            
        except Exception as e:
            print(f"Error processing batch {batch_num}: {str(e)}")
            continue
    
    print(f"Completed processing {len(summarized_reviews)} reviews")
    return output_path