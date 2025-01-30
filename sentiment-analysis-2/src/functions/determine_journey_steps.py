import json
import os
import random
from glob import glob
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
from openai import AsyncOpenAI
from typing import Dict, List

# Reviews per sample
REVIEWS_PER_SAMPLE = 50

# Define prompts as constants
JOURNEY_ANALYSIS_PROMPT = """
Analyze these customer reviews and identify a minimum of 12 customer journey steps.
Ensure steps include the customer using the service or product until their journey is complete
The steps should be chronological and represent the typical customer journey.
Return ONLY a list of journey step titles in a JSON array format.
DO NOT include 'feedback' as a step.
DO NOT start steps with 'the customer' or 'customer'.
DO NOT include ',','('.')', 'eg.', 'e.g.', 'for example', 'such as', 'like', 'e.g.,' or 'i.e.'.
"""

# Load environment variables
load_dotenv()

# Initialize AsyncOpenAI client
client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def extract_sample_reviews() -> str:
    """Extract random sample of reviews for journey determination"""
    try:
        # Setup paths
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        
        input_dir = os.path.join(project_root, 'src', 'data', 'pre-processed-raw-data')
        output_dir = os.path.join(project_root, 'src', 'data', 'sample_for_journey_determination')
        os.makedirs(output_dir, exist_ok=True)
        
        # Get latest processed reviews file
        json_files = glob(os.path.join(input_dir, 'processed_reviews_*.json'))
        if not json_files:
            raise FileNotFoundError("No processed review files found")
        
        latest_file = max(json_files, key=os.path.getctime)
        print(f"Reading from: {latest_file}")
        
        # Read and sample reviews
        with open(latest_file, 'r') as file:
            reviews = json.load(file)
        
        sample_size = min(REVIEWS_PER_SAMPLE, len(reviews))
        sample = random.sample(reviews, sample_size)
        
        # Extract only reviewDescription
        descriptions = [{"reviewDescription": review["reviewDescription"]} for review in sample]
        
        # Generate timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        
        # Save sample with timestamp
        output_filename = f'sample_for_journey_determination_{timestamp}.json'
        output_file = os.path.join(output_dir, output_filename)
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(descriptions, file, indent=2)
        
        print(f"Extracted {sample_size} reviews for journey determination")
        return output_file
        
    except Exception as e:
        print(f"Error extracting sample reviews: {str(e)}")
        raise

def analyze_journey_steps() -> str:
    """Send sample reviews file to OpenAI and get journey steps"""
    try:
        # Check for API key
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        # Setup paths
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        sample_dir = os.path.join(project_root, 'src', 'data', 'sample_for_journey_determination')
        
        # Find latest sample file
        sample_files = glob(os.path.join(sample_dir, 'sample_for_journey_determination_*.json'))
        if not sample_files:
            raise FileNotFoundError(f"No sample files found in {sample_dir}")
        
        input_file = max(sample_files, key=os.path.getctime)
        print(f"Using sample file: {input_file}")
        
        # Initialize OpenAI with explicit API key
        client = OpenAI(api_key=api_key)
        
        # Read file content
        with open(input_file, 'r') as f:
            file_content = f.read()
        
        # Create API request
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a customer journey expert. Return only a JSON array of journey steps."},
                {"role": "user", "content": f"{JOURNEY_ANALYSIS_PROMPT}\n\nReviews:\n{file_content}"}
            ],
            response_format={"type": "json_object"}
        )
        
        # Process response
        journey_steps = json.loads(response.choices[0].message.content)
        
        # Save journey steps with timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        output_dir = os.path.join(project_root, 'src', 'data', 'journey-steps')
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f'customer_journey_steps_{timestamp}.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(journey_steps, f, indent=2)
        
        print(f"Journey steps saved")
        return output_file
        
    except Exception as e:
        print(f"Error analyzing journey steps: {str(e)}")
        raise