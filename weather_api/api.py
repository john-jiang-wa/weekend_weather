#!/usr/bin/env python
# coding: utf-8

import os
import json
import logging
import requests
from datetime import datetime, timedelta
from flask import Flask, jsonify

# Constants
URL_GEO = "http://api.openweathermap.org/geo/1.0/zip?zip={zip},us&appid={key}"
URL_WEATHER = "https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={key}&units=imperial"

# # Configuration
API_KEY = os.environ.get('API_KEY')
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

def valid_zip_code(zip_code):
    return len(zip_code) == 5 and zip_code.isdigit()

def filter_weekend_data(weather_data):
    try:
        weekend_forecast = {'Location': f"{weather_data['name']}, {weather_data['country']}",
                            'Saturday': {'Summary': '', 'Hourly': []},
                            'Sunday': {'Summary': '', 'Hourly': []}}

        current_date = datetime.utcnow()
        next_saturday = current_date + timedelta((5 - current_date.weekday() + 7) % 7)
        next_sunday = next_saturday + timedelta(days=1)

        for day in weather_data.get('daily', []):
            forecast_time = datetime.fromtimestamp(day.get('dt'))

            if forecast_time.date() == next_saturday.date():
                day_key = 'Saturday'
            elif forecast_time.date() == next_sunday.date():
                day_key = 'Sunday'
            else:
                continue

            max_temp = day['temp'].get('max', 'N/A')
            min_temp = day['temp'].get('min', 'N/A')
            weekend_forecast[day_key]["Summary"] = day.get('summary', '') + f" with a high of {max_temp}°F and low of {min_temp}°F"

        for hour in weather_data.get('hourly', []):
            forecast_time = datetime.fromtimestamp(hour.get('dt'))

            if forecast_time.date() == next_saturday.date() or forecast_time.date() == next_sunday.date():
                hour_str = forecast_time.strftime("%I %p")
                hour_temp = hour.get('temp', 'N/A')
                hourly_forecast = {"hour": hour_str, "temp": hour_temp}
                date_key = forecast_time.strftime("%A")
                weekend_forecast[date_key]['Hourly'].append(hourly_forecast)

        return weekend_forecast

    except KeyError as e:
        logging.error(f"KeyError: {e} not found in weather data")
        return {"error": f"KeyError: {e} not found in weather data"}

    except Exception as e:
        logging.error(f"An error occurred when filtering weather data: {e}")
        return {"error": f"An error occurred when filtering weather data: {e}"}
    
def get_weekend_weather(zip_code):
    
    logging.info("Making API request for %s", zip_code)

    try:
        response = requests.get(URL_GEO.format(zip = zip_code, key = API_KEY))        
        if response.status_code != 200:
            sanitized_error_message = response.text.replace(API_KEY, "<API_KEY>")
            return {"error": sanitized_error_message}, response.status_code
        geo_data = response.json()
        latitude, longitude = geo_data['lat'], geo_data['lon']

        response = requests.get(URL_WEATHER.format(lat = latitude, lon = longitude, key = API_KEY))
        if response.status_code != 200:
            sanitized_error_message = response.text.replace(API_KEY, "<API_KEY>")
            return {"error": sanitized_error_message}, response.status_code
        weather_data = response.json()
    
    except (requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.RequestException) as err:
        sanitized_error_message = str(err).replace(API_KEY, "<API_KEY>")
        logging.error(f"Error occurred during OpenWeatherMap API call: {sanitized_error_message}")
        return {"error": sanitized_error_message}, 500
    
    except json.decoder.JSONDecodeError:
        logging.error("Unable to parse API response")
        return {"error": "Unable to parse API response"}, 500

    merged_data = {**geo_data, **weather_data}
    weekend_weather = filter_weekend_data(merged_data)

    logging.info("Successfully retrieved weekend weather for %s", zip_code)

    return weekend_weather, response.status_code    

@app.route('/forecast/<zip_code>', methods=['GET'])
def forecast(zip_code):

    if not valid_zip_code(zip_code):
        return {"error": "Invalid zip code"}, 400

    weekend_weather, status_code = get_weekend_weather(zip_code)

    if status_code != 200:
        return jsonify({"error": weekend_weather}), status_code
    
    return jsonify(weekend_weather), status_code