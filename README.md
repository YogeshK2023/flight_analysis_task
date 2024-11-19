This project consists of two main components:

Data Generation (generate_flights.py): Generates synthetic flight data and stores it in JSON files.
Data Analysis (analyze_flights.py): Reads the generated data, cleans it, and performs various analyses, including visualizations of key metrics.


Installation

To get started with this project, you need to install the required dependencies. This can be done using pip.

bash commands
```sh
python3.12 -m venv env3.12
source env3.12/bin/activate  # For Linux/macOS

.\env3.12\Scripts\activate   # For Windows
```

Install the dependencies:
bash command
```sh
pip install -r requirements.txt
```

Setup and Usage

Generating Flight Data
To generate synthetic flight data, run the generate_flights.py script. This script creates flight records and saves them as JSON files in the ./tmp/flights directory.

bash command
```sh
python generate_flights.py
```

This will generate 5000 flight data files with a random number of flight records (ranging from 50 to 100 records per file) and store them in ./tmp/flights. Each file will be named with the format MM-YY-origin_city-flights.json.

Analyzing Flight Data
Once the data is generated, you can analyze it using the analyze_flights.py script. This script performs several tasks, including:

Cleaning the flight records by removing or marking records with NULL values.
Generating various statistics (e.g., average flight duration by destination, total passengers, etc.).
Plotting data visualizations, such as bar graphs comparing null, clean records and total records.

To run the analysis:

bash command
```sh
python analyze_flights.py
```

This will process all the flight data files, clean the records, and generate plots. The plots will be saved in the ./tmp/image directory as PNG files. The script also prints key statistics to the console.

Output
Processed Flight Data: The script processes and cleans the flight data.

Plots: The analysis script generates several visualizations, including:
A bar chart comparing the number of "dirty" (with NULL values), "clean" records and "total" records.
A horizontal bar chart showing the average flight duration for the top 25 destination cities.
A horizontal bar chart showing the 95th percentile flight duration for the same cities.


Notes:
Data Generation: The generate_flights.py script uses random data for city names, flight dates, and flight durations, so the generated data is not real, but realistic enough for testing purposes.
Data Analysis: The analysis functions include parallel processing for efficiency, especially when handling large datasets.
Visualizations: The script uses matplotlib to generate bar charts and plots. These visualizations are saved in the ./tmp/image folder.