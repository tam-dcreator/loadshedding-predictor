"""
This module fetches historical weather data from the Visual Crossing API
and stores it in a CSV file.

The script checks for an existing CSV file: - If the file exists,
it retrieves the last recorded date and continues fetching data from that
point. - If the file does not exist, it starts from January 1, 2024. - If
data from a city is already present, it appends new records in the same
format. - If data from a new city is fetched, it adds new columns for the
city's weather data.

Data is retrieved in 19-day intervals due to API restrictions and appended to
the CSV file.
If HTTPError: 429 Client Error is raised then you've exceeded your daily API
quota

Dependencies:
    - requests
    - os
    - pandas
    - dotenv
    - datetime

Environment Variables:
    - WEATHER_API: API key for accessing the Visual Crossing API.

Functions:
    - get_last_recorded_date(city):
    Checks CSV file for last recorded date for the specified city; defaults to
    2024-01-01 if missing.
    - get_data(city='Cape Town'):
    Fetches and appends weather data for the specified city to the CSV file.

Example usage:
    # >>> from fetch_weather_data import get_data
    # >>> get_data(city='Johannesburg')
"""

import requests
import os
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables (API key)
load_dotenv("./.env")  # Ensure .env file is in the same directory

WEATHER_API_KEY = os.getenv("WEATHER_API")
CSV_FILE = "weather_data.csv"
UNIT_GROUP = "metric"
OPTIONS = "hours"
HEADERS = "datetime,temp,humidity,precip,snow,windspeed"


def get_last_recorded_date(city):
    """Retrieve the last recorded date for the city from the CSV file or
    default to Jan 1, 2024.

    Args:
        city (str): The city for which to retrieve the last recorded date.

    Returns:
        datetime: The last recorded date or Jan 1, 2024 if no data is found.
    """
    # filename = f"{city}_{WEATHER_API_KEY}" # TODO Implement after extracting
    # Check if the file exists and read into it
    if os.path.exists(CSV_FILE):  # TODO change to filename
        df = pd.read_csv(CSV_FILE)

        # Check if file is not empty
        if not df.empty:
            # Check if there's existing data for the city and get the last
            # recorded value
            if f"{city}_temp" in df.columns:
                last_date_str = df.iloc[-1]["timestamp"]
                if last_date_str == "2024-03-31 23:00:00":
                    print("Last date for power dataset encountered: ",
                          last_date_str)
                    raise ValueError("Crosscheck the dates on the csv")
                last_date = datetime.strptime(last_date_str,
                                              "%Y-%m-%d %H:%M:%S")
                last_date += timedelta(days=1)

                return last_date

    return datetime(2024, 1, 1)


def get_data(city='Cape Town'):
    """Fetch historical weather data and append it to the CSV file.

    Args: city (str): The city for which to fetch the weather data. Defaults
    to 'Cape Town'.
    Returns On error: HTTPError: 429 Client Error, signifying daily alloted API
    quota has been exceeded
    """
    nme = city.lower().replace(" ", "_")
    start_date = get_last_recorded_date(city=nme).date()
    end_date = start_date + timedelta(days=19)
    # Ensure end date doesn't exceed March 31 2024, which is the last entry
    # for the Eskom power csv.
    max_end_date = datetime(2024, 3, 31, 0, 0, 0).date()
    end_date = min(end_date, max_end_date)  # Select Min value

    weather_url = (f"https://weather.visualcrossing.com"
                   f"/VisualCrossingWebServices/rest/services/t"
                   f"imeline/{city}/{start_date}/{end_date}")

    weather_params = {
        "unitGroup": UNIT_GROUP,
        "include": OPTIONS,
        "key": WEATHER_API_KEY,
        "contentType": "json"
    }

    response = requests.get(url=weather_url, params=weather_params)
    response.raise_for_status()
    data = response.json()

    records = []

    for day in data.get("days", []):
        for hour in day.get("hours", []):
            records.append([
                f"{day['datetime']} {hour['datetime']}", hour["temp"],
                hour["humidity"], hour.get("precip", 0), hour.get("snow", 0),
                hour["windspeed"]
            ])

    # Create a dataframe for the newly received data
    df = pd.DataFrame(records,
                      columns=["timestamp", f"{nme}_temp", f"{nme}_humidity",
                               f"{nme}_precipitation", f"{nme}_snow",
                               f"{nme}_windspeed"])

    # Check if there's an existing file to determine if the data would be
    # appended or created in a new csv
    if os.path.exists(CSV_FILE):  # TODO change to filename
        existing_df = pd.read_csv(CSV_FILE)

        # Check if any column starts with "City_Name_"
        city_exists = any(col.startswith(f"{nme}_") for col in
                          existing_df.columns)

        # Set timestamp as index for correct merging of more than one city info
        # existing_df.set_index("timestamp", inplace=True)
        # df.set_index("timestamp", inplace=True)

        # Check if existing city
        if city_exists:
            # if yes add new rows
            existing_df = pd.concat([existing_df, df], axis=0)
        else:
            # If no, add the data as a column in the file
            existing_df = pd.concat([existing_df, df], axis=1)
        existing_df.to_csv(CSV_FILE, index=False)  # TODO Change to filename
    else:
        df.to_csv(CSV_FILE, index=False)

    print(f"Weather data saved to {CSV_FILE} from {start_date} "
          f"to {end_date} for {city}.")  # TODO change to filename
