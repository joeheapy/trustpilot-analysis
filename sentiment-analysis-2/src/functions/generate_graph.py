import json
import os
from glob import glob
from datetime import datetime
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import webbrowser

# Constants
PLOT_CONSTANTS = {
    'HEIGHT': 1400,
    'WIDTH': 1200,
    'VERTICAL_SPACING': 0.21,
    'ROW_HEIGHTS': [0.25, 0.25, 0.25],
    'MARGINS': dict(l=80, r=80, t=100, b=80, pad=20)
}

def get_latest_ratings():
    """Get latest ratings file from ratings-by-step directory"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    ratings_dir = os.path.join(os.path.dirname(current_dir), 'data', 'ratings-by-step')
    json_files = glob(os.path.join(ratings_dir, 'ratings_by_step_*.json'))
    
    if not json_files:
        raise FileNotFoundError("No ratings files found")
    
    return max(json_files, key=os.path.getctime)

def generate_graph():
    """Generate and display interactive visualization"""
    try:
        # Setup directories
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(os.path.dirname(current_dir), 'data')
        vis_dir = os.path.join(data_dir, 'visualizations')  # Correct path
        os.makedirs(vis_dir, exist_ok=True)

        # Load data
        latest_file = get_latest_ratings()
        
        with open(latest_file, 'r') as f:
            data = json.load(f)
        # print("Data loaded successfully")
        
        journey_data = data['journeySteps']
        steps = list(journey_data.keys())
        # print(f"Found {len(steps)} journey steps")
        
        # Initialize data structures
        ratings = {i: [] for i in range(1, 6)}
        total_responses = []
        average_ratings = []
        
        # Process ratings
        for step in steps:
            step_data = journey_data[step]
            step_total = 0
            weighted_sum = 0.0  # Initialize as float
            
            for rating in range(1, 6):
                count = step_data.get(str(rating), 0)
                ratings[rating].append(count)
                step_total += count
                weighted_sum += float(rating) * count
            
            if step_total > 0:
                avg_rating = round(weighted_sum / step_total, 1)  # Round to 1 decimal
                normalized_rating = round((avg_rating - 3) / 2, 1)  # Round normalization
            else:
                normalized_rating = 0.0
            
            average_ratings.append(normalized_rating)
            total_responses.append(step_total)
            # print(f"Step: {step}, Total: {step_total}, Avg Rating: {normalized_rating:.2f}")
        
        # Create visualization
        fig = make_subplots(
            rows=3, cols=1,
            subplot_titles=(
                'Average Rating by Step',
                'Rating Distribution by Journey Step',
                'Total Responses by Step'
            ),
            row_heights=PLOT_CONSTANTS['ROW_HEIGHTS'],
            vertical_spacing=PLOT_CONSTANTS['VERTICAL_SPACING']
        )
        
        # Add average ratings trace
        fig.add_trace(
            go.Scatter(
                x=steps,
                y=average_ratings,
                name='Average Rating',
                line=dict(color='#FF0000', width=2),
                mode='lines+markers',
                hovertemplate="Step: %{x}<br>Average Rating: %{y:.2f}<extra></extra>"
            ),
            row=1, col=1
        )
        
        # Add rating distribution traces
        colors = ['#FF6B6B', '#FFD93D', '#95D5B2', '#74C0FC', '#38B000']
        for rating in range(1, 6):
            fig.add_trace(
                go.Bar(
                    name=f'{rating} Star{"s" if rating != 1 else ""}',
                    x=steps,
                    y=ratings[rating],
                    marker_color=colors[rating-1],
                    hovertemplate="Step: %{x}<br>Rating: " + str(rating) + "<br>Count: %{y}<extra></extra>"
                ),
                row=2, col=1
            )
        
        # Add total responses trace
        fig.add_trace(
            go.Bar(
                x=steps,
                y=total_responses,
                name='Total Responses',
                marker_color='#4A4E69',
                hovertemplate="Step: %{x}<br>Total: %{y}<extra></extra>"
            ),
            row=3, col=1
        )
        
        # Update layout
        fig.update_layout(
            barmode='stack',
            height=PLOT_CONSTANTS['HEIGHT'],
            width=PLOT_CONSTANTS['WIDTH'],
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            margin=PLOT_CONSTANTS['MARGINS'],
            autosize=True
        )
        
        # Update axes
        fig.update_yaxes(
            title_text="Average Rating",
            range=[-2, 2],
            tickmode='array',
            tickvals=[i/4 for i in range(-10, 11, 2)],  # Creates ticks at 0.2 intervals
            tickformat='.1f',  # Display one decimal place
            row=1, col=1
)
        fig.update_yaxes(title_text="Number of Ratings", row=2, col=1)
        fig.update_yaxes(title_text="Total Responses", row=3, col=1)
        fig.update_xaxes(tickangle=45)
        
        # Save visualization
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        output_path = os.path.join(vis_dir, f'journey_visualization_{timestamp}.html')
        
        fig.write_html(output_path)
        webbrowser.open('file://' + os.path.abspath(output_path))
        
        print(f"Visualization saved")
        return output_path
        
    except Exception as e:
        print(f"Error generating visualization: {str(e)}")
        raise

if __name__ == "__main__":
    generate_graph()