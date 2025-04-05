"""
This module provides test cases to validate the loadshedding estimation
functions and weather data fetching functions.

It includes tests for:
- Load shedding estimation functions
- Weather data fetching functions

Dependencies:
    - pandas
    - pytest (for running the tests)

Functions:
    - test_tune_threshold(): Validates the tune_threshold function.
    - test_estimate_loadshedding(): Validates estimate_loadshedding function.
    - test_get_last_recorded_date(): Validates get_last_recorded_date function.
"""

import pandas as pd
import pytest
from datetime import datetime
from det_loadshedding import tune_threshold, estimate_loadshedding
from fetch_weather_data import get_last_recorded_date


def test_tune_threshold():
    """
    Test the tune_threshold function.

    Asserts that the function returns the correct threshold based on the
    time of day.
    """
    assert tune_threshold(19) == 2100, "Threshold for 19:00 is incorrect."
    assert tune_threshold(1) == 1500, "Threshold for 01:00 is incorrect."
    assert tune_threshold(18) == 1950, "Threshold for 18:00 is incorrect."
    assert tune_threshold(2) == 1650, "Threshold for 02:00 is incorrect."
    assert tune_threshold(10) == 1789, "Default threshold is incorrect."


def test_estimate_loadshedding():
    """
    Test the estimate_loadshedding function.

    Asserts that the function correctly estimates load shedding based on
    input data.
    """
    row = pd.Series({
        "residual_demand": 5000,
        "dispatchable_generation": 3000,
        "eskom_ocgt_generation": 200,
        "hydro_water_generation": 100,
        "manual_load_reduction(mlr)": 500,
        "international_imports": 300,
        "international_exports": 100,
        "load_shedding_threshold": 1500
    })
    assert estimate_loadshedding(row) == 1, "Loadshedding estimation incorrect"

    row["residual_demand"] = 2000
    assert estimate_loadshedding(row) == 0, "Loadshedding estimation incorrect"


def test_get_last_recorded_date():
    """
    Test the get_last_recorded_date function.

    Asserts that the function returns the correct last recorded date based on
    the CSV file.
    """
    # Mock the CSV file content
    mock_csv_content = """timestamp,cape_town_temp,cape_town_humidity,cape_town_precipitation,cape_town_snow,cape_town_windspeed
2024-01-01 00:00:00,20,60,0,0,10
2024-01-02 01:00:00,21,61,0,0,11
"""
    with open("sample_data.csv", "w") as f:
        f.write(mock_csv_content)

    last_date = get_last_recorded_date("Cape Town")
    assert last_date == datetime(2024, 1, 2), "Last recorded date is incorrect"
