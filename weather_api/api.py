#!/usr/bin/env python
# coding: utf-8

import os
import requests
import datetime
from flask import Flask, jsonify

api_key = os.environ.get('API_KEY')
app = Flask(__name__)

def get_weather_data(zip_code):
    response = requests.get(f"http://api.openweathermap.org/data/2.5/forecast?zip={zip_code},us&appid={api_key}")
    return response.json()

def get_weekend_forecast(zip_code):
    data = get_weather_data(zip_code)
    forecast_list = data['list']
    weekend_forecast = []

    for forecast in forecast_list:
        date = datetime.datetime.strptime(forecast['dt_txt'], '%Y-%m-%d %H:%M:%S').date()
        if date.weekday() >= 5:  # 5, 6 = Saturday, Sunday
            weekend_forecast.append(forecast)

    return weekend_forecast

@app.route('/forecast/<zip_code>', methods=['GET'])
def forecast(zip_code):
    return jsonify(get_weekend_forecast(zip_code))

