import os
import json
import pandas as pd
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor
import matplotlib.pyplot as plt
from pathlib import Path

# Constants
FLIGHTS_DIR = "./tmp/flights"


def process_file(file_path):
    """Reads a single JSON file and processes its records."""
    with open(file_path, "r") as f:
        records = json.load(f)
    total_records = len(records)
    dirty_records = [record for record in records if any(
        v is None for v in record.values())]
    clean_records = [record for record in records if all(
        v is not None for v in record.values())]
    return total_records, len(dirty_records), clean_records


def plot_data(null_counts, clean_counts):
    """
    Plots a bar graph comparing data with NULL values before
    and after cleaning, and adds value labels on top of the bars.
    Additionally, adds a third bar showing the total records 
    (sum of NULL and Clean counts).
    """
    # Labels for the bars
    labels = ['Null records', 'Clean records', 'Total records']
    
    # Data: sum of null counts, clean counts, and total records
    null_sum = sum(null_counts)
    clean_sum = sum(clean_counts)
    total_sum = null_sum + clean_sum
    
    data = [null_sum, clean_sum, total_sum]

    # Create a bar graph with 3 bars
    bars = plt.bar(labels, data, color=['red', 'green', 'yellow'])
    
    # Adding the values on top of the bars
    for bar in bars:
        height = bar.get_height()  # Get the height of the bar
        plt.text(
            bar.get_x() + bar.get_width() / 2,  # X position: center of the bar
            height,  # Y position: top of the bar
            f'{height}',  # Text to display (value)
            ha='center',  # Horizontal alignment of the text
            va='bottom',  # Vertical alignment (above the bar)
            fontsize=10,  # Font size
            color='black'  # Color of the text
        )
    
    # Title and labels
    plt.title('Count of Records')
    plt.ylabel('Number of Records')
    plt.xlabel('Category')
    plt.xticks(labels)

    # Save the plot as an image
    Path("./tmp/image/").mkdir(parents=True, exist_ok=True)
    output_path = "./tmp/image/flights_analysis.png"
    plt.savefig(output_path)
    print(f"Bar graph saved to {output_path}")

    # Display the plot
    plt.show()


def plot_visualize_data(x, y, title, xlabel, ylabel, color='#5DADE2'):
    """
    Plots a bar graph with the necessary details, adds values on top of the bars,
    changes the color of the bars, and saves the file.
    """
    # Create the bar graph
    plt.barh(x,y, color=color)
    plt.ylabel(xlabel)
    plt.xlabel(ylabel)
    plt.title(title)

    # Add numbers on top of each bar
    for i, v in enumerate(y):
        plt.text(v + 0.01, i, str(round(v,2)), va='center',color='black')

    # Save the plot as an image
    Path("./tmp/image/").mkdir(parents=True, exist_ok=True)
    output_path = f"./tmp/image/{title}.png"
    plt.savefig(output_path)
    print(f"Bar graph saved to {output_path}")

    # Display the plot
    plt.show()


def analyze_and_clean():
    """Main function to analyze and clean flight data."""
    print("Analyzing and cleaning flight data...")
    start_time = datetime.now()
    files = [os.path.join(FLIGHTS_DIR, f)
             for f in os.listdir(FLIGHTS_DIR) if f.endswith(".json")]
    total_records = 0
    dirty_records = 0
    clean_data = []
    null_counts = []
    clean_counts = []

    # Parallel processing for efficiency
    with ProcessPoolExecutor() as executor:
        results = executor.map(process_file, files)
        for total, dirty, clean in results:
            total_records += total
            dirty_records += dirty
            null_counts.append(dirty)
            clean_counts.append(total - dirty)
            clean_data.extend(clean)

    # Convert clean data to DataFrame
    df = pd.DataFrame(clean_data)
    df['flight_duration_secs']=round(df['flight_duration_secs']/3600,2)
    df.rename(columns={'flight_duration_secs': 'flight_duration_hours'}, inplace=True)

    # Top 25 destination cities by count
    top_dest_cities = df["destination_city"].value_counts().nlargest(25).index
    top_dest_df = df[df["destination_city"].isin(top_dest_cities)]

    # Flight duration stats
    avg_duration = top_dest_df.groupby("destination_city")[
        "flight_duration_hours"].mean().reset_index()
    avg_duration=avg_duration.sort_values(by='flight_duration_hours').reset_index()
    p95_duration = top_dest_df.groupby("destination_city")[
        "flight_duration_hours"].quantile(0.95).reset_index()
    p95_duration=p95_duration.sort_values(by='flight_duration_hours').reset_index()

    # Passengers arriving and departing
    passengers_arrived = df.groupby("destination_city")[
        "passengers_on_board"].sum()
    passengers_departed = df.groupby("origin_city")[
        "passengers_on_board"].sum()
    max_arrival_city = passengers_arrived.idxmax()
    max_departure_city = passengers_departed.idxmax()

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()


    # Print results
    print(f"\nTotal Records Processed: {total_records}")
    print(f"\nDirty Records: {dirty_records}")
    print(f"\nProcessing Duration: {duration} seconds")
    # print(f"\nTop 25 Destinations AVG Duration:\n{avg_duration}")
    # print(f"\nTop 25 Destinations P95 Duration:\n{p95_duration}")
    print(f"\nCity with Max Passengers Arrived: {max_arrival_city}")
    print(f"\nCity with Max Passengers Departed: {max_departure_city}")
    print('\n')


    # Plot dirty vs clean records
    plot_data(null_counts, clean_counts)

    #Plotting the Top 25 Destinations AVG Duration
    plot_visualize_data(x=avg_duration['destination_city'],y=avg_duration['flight_duration_hours'],
                        xlabel="Destination Cities",ylabel='flight_duration_hours',title='Top 25 Destinations AVG Duration')
    
    #Plotting the Top 25 Destinations P95 Duration
    plot_visualize_data(x=p95_duration['destination_city'],y=p95_duration['flight_duration_hours'],
                        xlabel="Destination Cities",ylabel='flight_duration_hours',title='Top 25 Destinations P95 Duration')
    


if __name__ == "__main__":
    analyze_and_clean()
