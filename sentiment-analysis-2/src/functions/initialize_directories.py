import shutil
from datetime import datetime
import os

# Constants for directory structure
DIRECTORIES_TO_CLEAN = [
    'pre-processed-raw-data',
    'sample_for_journey_determination',
    'journey-steps'
]

DIRECTORIES_TO_PRESERVE = [
    'raw-trustpilot-data'
]

def initialize_directories():
    """Initialize working directories by removing and recreating them"""
    
    # Get absolute path to project root
    current_dir = os.path.dirname(os.path.abspath(__file__))  # /functions
    src_dir = os.path.dirname(current_dir)  # /src
    data_dir = os.path.join(src_dir, 'data')  # /src/data
    
    print(f"Current directory: {current_dir}")
    print(f"Source directory: {src_dir}")
    print(f"Data directory: {data_dir}")
    
    # Ensure base data directory exists
    os.makedirs(data_dir, exist_ok=True)
    
    print(f"\nInitializing directories at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Process directories to clean
    for dir_name in DIRECTORIES_TO_CLEAN:
        try:
            full_path = os.path.join(data_dir, dir_name)
            print(f"Processing directory: {full_path}")
            
            if os.path.exists(full_path):
                shutil.rmtree(full_path)
                print(f"Removed existing directory: {full_path}")
            
            os.makedirs(full_path)
            print(f"Created directory: {full_path}")
            
        except Exception as e:
            print(f"Error processing directory {dir_name}: {str(e)}")
            raise
    
    # Ensure preserved directories exist
    for dir_name in DIRECTORIES_TO_PRESERVE:
        try:
            full_path = os.path.join(data_dir, dir_name)
            print(f"Ensuring directory exists: {full_path}")
            os.makedirs(full_path, exist_ok=True)
            
        except Exception as e:
            print(f"Error ensuring directory {dir_name}: {str(e)}")
            raise