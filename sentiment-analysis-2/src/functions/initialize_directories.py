import shutil
from datetime import datetime
import os

def initialize_directories():
    """Initialize working directories by removing and recreating them"""
    
    # Get absolute path to project root
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    
    # Define base data directory - updated to include 'src'
    data_dir = os.path.join(project_root, 'src', 'data')
    
    # List of directory names to create in data folder
    directories = [
        'pre-processed-raw-data',
        'sample_for_journey_determination',
        'journey-steps'
    ]
    
    # Create full paths
    directory_paths = [os.path.join(data_dir, dir_name) for dir_name in directories]
    
    print(f"\nInitializing directories at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    for directory in directory_paths:
        try:
            
            if os.path.exists(directory):
                shutil.rmtree(directory)

            os.makedirs(directory, exist_ok=True)

        except Exception as e:
            print(f"Error processing directory {directory}: {str(e)}")
            raise