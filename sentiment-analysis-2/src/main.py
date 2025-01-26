from functions.initialize_directories import initialize_directories
from functions.pre_process_raw_data import pre_process_raw_data
from functions.determine_journey_steps import extract_sample_reviews, analyze_journey_steps

def main():
    try:
        # Initialize directories first
        initialize_directories()
        
        # Process the data
        output_file = pre_process_raw_data()
        print(f"Successfully pre-processed and saved reviews.")
        
        # Extract sample reviews
        sample_file = extract_sample_reviews()
        print(f"Successfully extracted sample reviews.")
        
        # Analyze journey steps
        journey_file = analyze_journey_steps()
        print(f"Journey steps saved to: {journey_file}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()