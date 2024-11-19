import os
import json
import random
from datetime import datetime
from pathlib import Path

# Constants
FLIGHTS_DIR = "./tmp/flights"
NUM_FILES = 5000
NULL_PROB = random.uniform(0.005, 0.001)  # 0.5% to 0.1%
RECORDS_PER_FILE = (50, 100)
DATE_FORMAT = "%Y-%m-%d"

# Predefined list of real city names
CITY_NAMES = [
    "New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia",
    "San Antonio", "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville",
    "Fort Worth", "Columbus", "San Francisco", "Charlotte", "Indianapolis",
    "Seattle", "Denver", "Washington", "Boston", "El Paso", "Detroit", "Nashville",
    "Memphis", "Portland", "Oklahoma City", "Las Vegas", "Louisville", "Baltimore",
    "Milwaukee", "Albuquerque", "Tucson", "Fresno", "Sacramento", "Kansas City",
    "Mesa", "Atlanta", "Omaha", "Colorado Springs", "Raleigh", "Miami", "Long Beach",
    "Virginia Beach", "Oakland", "Minneapolis", "Tulsa", "Tampa", "Arlington"
]


def generate_random_date():
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 1, 1)
    return (start_date + (end_date - start_date) * random.random()).strftime(DATE_FORMAT)


def generate_flight_record():
    record = {
        "date": generate_random_date(),
        "origin_city": random.choice(CITY_NAMES),
        "destination_city": random.choice(CITY_NAMES),
        "flight_duration_secs": random.randint(3600, 14400),  # 1 to 4 hours
        "passengers_on_board": random.randint(1, 500),
    }
    # Introduce NULL with a small probability
    if random.random() < NULL_PROB:
        key = random.choice(list(record.keys()))
        record[key] = None
    return record


def generate_files():
    Path(FLIGHTS_DIR).mkdir(parents=True, exist_ok=True)
    for i in range(NUM_FILES):
        month_year = datetime.now().strftime("%m-%y")
        origin_city = random.choice(CITY_NAMES).replace(
            " ", "_")  # Replace spaces in file name
        file_path = f"{FLIGHTS_DIR}/{month_year}-{origin_city}-flights.json"
        records = [generate_flight_record()
                   for _ in range(random.randint(*RECORDS_PER_FILE))]
        with open(file_path, "w") as f:
            json.dump(records, f)
    print(f"Generated {NUM_FILES} flight files in {FLIGHTS_DIR}")


if __name__ == "__main__":
    generate_files()
