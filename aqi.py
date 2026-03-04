"""
AQI Simple Reflex Agent
-----------------------

This program implements a Simple Reflex Agent that:

1. Reads environmental data from a CSV file (aqi_data.csv)
2. Extracts PM2.5 concentration values
3. Calculates AQI using standard breakpoints
4. Categorizes AQI level
5. Prints results for each region

The CSV file acts as sensor input from the environment.
"""

import pandas as pd


# ------------------------------------------------------
# AQI Breakpoints for PM2.5 (US EPA Standard)
# ------------------------------------------------------

AQI_BREAKPOINTS = [
    (0.0, 12.0, 0, 50),
    (12.1, 35.4, 51, 100),
    (35.5, 55.4, 101, 150),
    (55.5, 150.4, 151, 200),
    (150.5, 250.4, 201, 300),
    (250.5, 350.4, 301, 400),
    (350.5, 500.4, 401, 500),
]


# ------------------------------------------------------
# AQI Calculation Function
# ------------------------------------------------------

def calculate_aqi(concentration):
    """
    Calculate AQI using linear interpolation formula
    """

    for bp_low, bp_high, aqi_low, aqi_high in AQI_BREAKPOINTS:
        if bp_low <= concentration <= bp_high:
            aqi = ((aqi_high - aqi_low) / (bp_high - bp_low)) * \
                  (concentration - bp_low) + aqi_low
            return round(aqi)

    return None


# ------------------------------------------------------
# AQI Category Function
# ------------------------------------------------------

def categorize_aqi(aqi):
    """
    Categorize AQI into health levels
    """

    if aqi is None:
        return "Invalid"

    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Satisfactory"
    elif aqi <= 150:
        return "Moderate"
    elif aqi <= 200:
        return "Poor"
    elif aqi <= 300:
        return "Very Poor"
    else:
        return "Severe"


# ------------------------------------------------------
# Simple Reflex Agent Class
# ------------------------------------------------------

class AQISimpleReflexAgent:

    def __init__(self, file_path="aqi_data.csv"):
        self.file_path = file_path

    def perceive(self):
        """
        Read data from CSV file (environment sensor input)
        """

        try:
            data = pd.read_csv(self.file_path, encoding="latin1")
            print("\nDataset loaded successfully.\n")
            return data

        except FileNotFoundError:
            print("\nERROR: CSV file not found.")
            print("Make sure 'aqi_data.csv' is in the same folder as this script.")
            return None

    def detect_pm25_column(self, dataframe):
        """
        Automatically detect PM2.5 column
        """

        possible_names = ["PM2.5", "pm2_5", "PM25", "pm25", "Pm2.5"]

        for col in dataframe.columns:
            if col in possible_names:
                return col

        return None

    def act(self):
        """
        Apply condition-action rules
        """

        data = self.perceive()

        if data is None:
            return

        pm25_column = self.detect_pm25_column(data)

        if pm25_column is None:
            print("ERROR: No PM2.5 column found in dataset.")
            print("Please check column name.")
            return

        print("AQI Results:\n")
        print("=" * 50)

        for index, row in data.iterrows():

            try:
                pm25_value = float(row[pm25_column])
                aqi = calculate_aqi(pm25_value)
                category = categorize_aqi(aqi)

                print(f"Row {index + 1}")
                print(f"PM2.5 Concentration : {pm25_value}")
                print(f"Calculated AQI      : {aqi}")
                print(f"AQI Category        : {category}")
                print("-" * 50)

            except:
                print(f"Skipping invalid data at row {index + 1}")

        print("\nAgent execution completed.\n")


# ------------------------------------------------------
# Main Execution
# ------------------------------------------------------

if __name__ == "__main__":
    agent = AQISimpleReflexAgent("aqi_data.csv")
    agent.act()