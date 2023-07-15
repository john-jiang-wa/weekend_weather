#!/usr/bin/env python
# coding: utf-8

import unittest
from unittest.mock import patch, Mock
from datetime import datetime, timedelta
from weather_api.api import valid_zip_code, filter_weekend_data, get_weekend_weather, app

class TestAPI(unittest.TestCase):

    def test_valid_zip_code(self):
        self.assertTrue(valid_zip_code('12345'))
        self.assertFalse(valid_zip_code('1234'))
        self.assertFalse(valid_zip_code('123456'))
        self.assertFalse(valid_zip_code('1234a'))

    def test_filter_weekend_data(self):
        current_date = datetime.utcnow()
        next_friday = current_date + timedelta((4-current_date.weekday()) % 7)
        next_frid_utc = int(next_friday.timestamp())
        next_saturday = current_date + timedelta((5-current_date.weekday()) % 7)  
        next_sat_utc = int(next_saturday.timestamp())
        weather_data = {'name': 'New York', 'country': 'US', 'daily': [{'summary': 'Friday', 'dt': next_frid_utc, 'temp': {'max': 2, 'min': 3}},
 {'summary': 'Saturday', 'dt': next_sat_utc, 'temp': {'max': 4, 'min': 5}}], 'hourly': []}
        weekend_weather = filter_weekend_data(weather_data)
        self.assertEqual(weekend_weather, {'Location': 'New York, US', 'Saturday': {'Summary': 'Saturday with a high of 4°F and low of 5°F', 'Hourly': []}, 'Sunday': {'Summary': '', 'Hourly': []}})    

    @patch('requests.get')
    def test_get_weekend_weather(self, mock_get):
        mock_responses = [
            Mock(),  # mock response for the first API call (Geo API)
            Mock()   # mock response for the second API call (One Call API)
        ]
        mock_responses[0].status_code = 200
        mock_responses[0].json.return_value = {'lat': 40.71, 'lon': -74.01}
        current_date = datetime.utcnow()
        next_friday = current_date + timedelta((4-current_date.weekday()) % 7)
        next_frid_utc = int(next_friday.timestamp())
        next_saturday = current_date + timedelta((5-current_date.weekday()) % 7)  
        next_sat_utc = int(next_saturday.timestamp())
        mock_responses[1].status_code = 200
        mock_responses[1].json.return_value = {'name': 'New York', 'country': 'US', 'daily': [{'summary': 'Friday', 'dt': next_frid_utc, 'temp': {'max': 2, 'min': 3}},
 {'summary': 'Saturday', 'dt': next_sat_utc, 'temp': {'max': 4, 'min': 5}}], 'hourly': []}
        mock_get.side_effect = mock_responses

        weekend_weather, status_code = get_weekend_weather('10001')

        self.assertEqual(status_code, 200)
        self.assertEqual(weekend_weather, {'Location': 'New York, US', 'Saturday': {'Summary': 'Saturday with a high of 4°F and low of 5°F', 'Hourly': []}, 'Sunday': {'Summary': '', 'Hourly': []}})

    @patch('weather_api.api.get_weekend_weather')
    def test_forecast_route(self, mock_get_weekend_weather):
        mock_get_weekend_weather.return_value = ({'Location': 'New York, US', 'Saturday': {'Summary': '', 'Hourly': []}, 'Sunday': {'Summary': '', 'Hourly': []}}, 200)
        with app.test_client() as client:
            response = client.get('/forecast/10001')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json(), {'Location': 'New York, US', 'Saturday': {'Summary': '', 'Hourly': []}, 'Sunday': {'Summary': '', 'Hourly': []}})

if __name__ == '__main__':
    unittest.main()
