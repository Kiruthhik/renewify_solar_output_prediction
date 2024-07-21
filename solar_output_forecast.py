'''import requests
import datetime

# Define the endpoint
endpoint = "https://re.jrc.ec.europa.eu/api/v5_2/seriescalc"

# Define the parameters for the next month
latitude = 51.507222  # Example latitude
longitude = -0.1275   # Example longitude
start_date = "2023-07-01"
end_date = "2023-07-30"
#start_date = datetime.date.today().strftime("%Y-%m-%d")
#end_date = (datetime.date.today() + datetime.timedelta(days=30)).strftime("%Y-%m-%d")

params = {
    "lat": latitude,
    "lon": longitude,
    "startdate": start_date,  # Start date in YYYY-MM-DD format
    "enddate": end_date,      # End date in YYYY-MM-DD format
    "angle": 0,               # Optimal inclination
    "aspect": 0,              # Optimal aspect
    "pvtechchoice": "crystSi",# PV technology choice (crystalline silicon)
    "peakpower": 1,           # Assumed peak power of the PV system in kW
    "loss": 14,               # Assumed system losses in %
    "outputformat": "json"
}

# Send the request to the PVGIS API
response = requests.get(endpoint, params=params)

# Check for HTTP errors
response.raise_for_status()

# Parse the response JSON
data = response.json()

# Extract relevant information
if "outputs" in data and "daily" in data["outputs"]:
    daily_data = data["outputs"]["daily"]
    print("Daily Solar Output Data:")
    for entry in daily_data:
        print(f"Date: {entry['time']} - PV Output: {entry['P']:.2f} kWh")
else:
    print("No solar output data available.")'''

'''import requests

# Define the endpoint and parameters
endpoint = "https://power.larc.nasa.gov/api/temporal/daily/point"
#latitude = 51.507222 
#longitude = -0.1275
latitude = 11.065249
longitude = 77.091971
params = {
    "start": "20230701",  # Start date in YYYYMMDD format
    "end": "20230731",    # End date in YYYYMMDD format
    "latitude": latitude,
    "longitude": longitude,
    "parameters": "ALLSKY_SFC_SW_DWN",  # Surface downward shortwave radiation
    "community": "RE",
    "format": "JSON"
}

# Send the request to the API
response = requests.get(endpoint, params=params)

# Parse the response JSON
data = response.json()

# Extract relevant information
if "properties" in data and "parameter" in data["properties"]:
    solar_irradiance = data["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"]
    print("Solar Irradiance Data:")
    for date, value in solar_irradiance.items():
        print(f"{date}: {value} W/m^2")
else:
    print("No solar irradiance data available.")'''

'''import requests
from datetime import datetime, timedelta, timezone

# Replace with your Meteomatics API credentials
username = "rajalakshmiengineeringcollege_as_kiruthhik"
password = "uki6kT15IN"

# Define the endpoint and parameters
latitude = 51.507222  # Example latitude
longitude = -0.1275   # Example longitude
start_date = datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
end_date = (datetime.now(tz=timezone.utc) + timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")
parameter = "global_horizontal_irradiance"

url = f"https://api.meteomatics.com/{start_date}--{end_date}:PT1H/{parameter}/{latitude},{longitude}/json"

# Solar panel parameters
panel_area = 1  # in square meters
panel_efficiency = 0.15  # 15% efficiency

# Send the GET request
response = requests.get(url, auth=(username, password))

# Check for HTTP errors
response.raise_for_status()

# Parse the response JSON
data = response.json()

# Extract relevant information and calculate solar power output
if "data" in data:
    solar_forecast = data["data"][0]["coordinates"][0]["dates"]
    print("Hourly Solar Power Output Prediction (in kWh):")
    for entry in solar_forecast:
        date_time = entry["date"]
        irradiance = entry["value"]  # in W/m²
        # Calculate the power output in kWh
        power_output = irradiance * panel_area * panel_efficiency / 1000  # kW
        print(f"{date_time}: {power_output:.4f} kWh")
else:
    print("No solar irradiance data available.")'''

'''import requests
from datetime import datetime, timedelta

# Function to get solar irradiance data for a specific year and month
def get_solar_irradiance_data(year, month, latitude, longitude):
    endpoint = "https://power.larc.nasa.gov/api/temporal/daily/point"
    start_date = f"{year}{month:02d}01"
    end_date = (datetime(year, month, 1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    end_date = end_date.strftime("%Y%m%d")
    
    params = {
        "start": start_date,  # Start date in YYYYMMDD format
        "end": end_date,      # End date in YYYYMMDD format
        "latitude": latitude,
        "longitude": longitude,
        "parameters": "ALLSKY_SFC_SW_DWN",  # Surface downward shortwave radiation
        "community": "RE",
        "format": "JSON"
    }

    response = requests.get(endpoint, params=params)
    response.raise_for_status()
    data = response.json()

    if "properties" in data and "parameter" in data["properties"]:
        return data["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"]
    else:
        return {}

# Get the current date
current_date = datetime.now()

# Calculate the next month
next_month = current_date.replace(day=28) + timedelta(days=4)
next_month = next_month.replace(day=1)

# Get the previous four years of data for the next month
#PSG college
#latitude = 11.065249
#longitude = 77.091971
#home
latitude = 12.9651541
longitude = 80.1763840
years = [next_month.year - i for i in range(1, 5)]
month = next_month.month

irradiance_data = []
for year in years:
    data = get_solar_irradiance_data(year, month, latitude, longitude)
    #print("raw data from API response",data)
    irradiance_data.append(data)

# Calculate the average solar irradiance
total_irradiance = {}
for data in irradiance_data:
    for date, value in data.items():
        day = int(date[-2:])  # Extract day from the date string
        if day not in total_irradiance:
            total_irradiance[day] = []
        total_irradiance[day].append(value)

#print("total_irradiance:",total_irradiance)

average_irradiance = {day: sum(values) / len(values) for day, values in total_irradiance.items()}

#print("average_irradiance",average_irradiance)
# Get solar panel area and efficiency
panel_area = 16.0
panel_efficiency = 0.18

# Calculate expected solar power output
expected_output = {}
total_output = 0  # Initialize total output to zero
for day, irradiance in average_irradiance.items():
    power_output = irradiance * panel_area * panel_efficiency   # kiloWatt per day
    expected_output[day] = power_output
    total_output += power_output  # Sum up the daily outputs

# Print the expected solar power output for the next month
print("Expected Solar Power Output for the Next Month (in kWh):")
for day, output in expected_output.items():
    print(f"Day {day:02d}: {output:.4f} kWh")
print("Total power output expected for the next month is:", total_output)





from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import requests'''


from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import requests

app = Flask(__name__)

def get_solar_irradiance_data(year, month, latitude, longitude):
    endpoint = "https://power.larc.nasa.gov/api/temporal/daily/point"
    start_date = f"{year}{month:02d}01"
    end_date = (datetime(year, month, 1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    end_date = end_date.strftime("%Y%m%d")
    
    params = {
        "start": start_date,  # Start date in YYYYMMDD format
        "end": end_date,      # End date in YYYYMMDD format
        "latitude": latitude,
        "longitude": longitude,
        "parameters": "ALLSKY_SFC_SW_DWN",  # Surface downward shortwave radiation
        "community": "RE",
        "format": "JSON"
    }

    response = requests.get(endpoint, params=params)
    response.raise_for_status()
    data = response.json()

    if "properties" in data and "parameter" in data["properties"]:
        return data["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"]
    else:
        return {}

@app.route('/solar-power-expectation', methods=['GET'])
def solar_power():
    latitude = 11.065249
    longitude = 77.091971
    panel_count = 10
    efficiency = 18
    latitude = request.args.get('latitude',latitude,type=float)
    longitude = request.args.get('longitude',longitude,type=float)
    panel_count = request.args.get('panel_count',panel_count,type=int)
    efficiency = request.args.get('efficiency',efficiency,type=float)

    current_date = datetime.now()

    # Calculate the next month
    next_month = current_date.replace(day=28) + timedelta(days=4)
    next_month = next_month.replace(day=1)

    years = [next_month.year - i for i in range(1, 5)]
    month = next_month.month

    irradiance_data = []
    for year in years:
        data = get_solar_irradiance_data(year, month, latitude, longitude)
        irradiance_data.append(data)

    total_irradiance = {}
    for data in irradiance_data:
        for date, value in data.items():
            day = int(date[-2:])  # Extract day from the date string
            if day not in total_irradiance:
                total_irradiance[day] = []
            total_irradiance[day].append(value)

    average_irradiance = {day: sum(values) / len(values) for day, values in total_irradiance.items()}

    panel_area = 1.6 * panel_count
    panel_efficiency = efficiency / 100.0

    total_output = 0  # Initialize total output to zero
    for day, irradiance in average_irradiance.items():
        power_output = irradiance * panel_area * panel_efficiency   # kiloWatt per day
        total_output += power_output  # Sum up the daily outputs

    month_name = next_month.strftime("%B")
    result = {
        "month": month_name,
        "expected_total_power_output": total_output
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

