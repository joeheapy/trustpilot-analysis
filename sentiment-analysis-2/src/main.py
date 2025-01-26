from functions.initialize_directories import initialize_directories
from functions.pre_process_raw_data import pre_process_raw_data
from functions.determine_journey_steps import extract_sample_reviews, analyze_journey_steps
from functions.summarize_review import summarize_review

def main():
    try:
        # Initialize directories first
        initialize_directories()
        
        # Process the data
        output_file = pre_process_raw_data()
        
        # Extract sample reviews
        sample_file = extract_sample_reviews()
        
        # Analyze journey steps
        journey_file = analyze_journey_steps()

        # Summarize review
        summary_file = summarize_review()
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()