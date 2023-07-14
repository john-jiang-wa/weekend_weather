#!/usr/bin/env python
# coding: utf-8

import unittest
from unittest.mock import patch
from weather_api.api import get_weather_data, get_weekend_forecast

class TestAPI(unittest.TestCase):

    @patch('requests.get')  # Mock the 'requests.get' function
    def test_get_weather_data(self, mock_get):
        # Mock the response from 'requests.get'
        mock_get.return_value.json.return_value = {
            'list': [
                {
                    "clouds": {"all": 100},
                    "dt": 1689422400,
                    "dt_txt": "2023-07-15 12:00:00",
                    "main": {
                        "feels_like": 299.95,
                        "grnd_level": 1004,
                        "humidity": 87,
                        "pressure": 1013,
                        "sea_level": 1013,
                        "temp": 299.03,
                        "temp_kf": 0,
                        "temp_max": 299.03,
                        "temp_min": 299.03
                    },
                    "pop": 0.71,
                    "rain": {"3h": 0.19},
                    "sys": {"pod": "d"},
                    "visibility": 10000,
                    "weather": [
                        {
                            "description": "light rain",
                            "icon": "10d",
                            "id": 500,
                            "main": "Rain"
                        }
                    ],
                    "wind": {"deg": 194, "gust": 4.91, "speed": 1.66}
                }
            ]
        }

        # Call the function with a sample zip code
        data = get_weather_data('12345')
        
        # Check the response
        self.assertEqual(len(data['list']), 1)
        self.assertEqual(data['list'][0]['main']['temp'], 299.03)
        self.assertEqual(data['list'][0]['weather'][0]['description'], 'light rain')

    @patch('weather_api.api.get_weather_data')  # Mock the 'get_weather_data' function
    def test_get_weekend_forecast(self, mock_get_weather_data):
        # Mock the response from 'get_weather_data'
        mock_get_weather_data.return_value = {
            'list': [
                {
                    "clouds": {"all": 100},
                    "dt": 1689422400,
                    "dt_txt": "2023-07-15 12:00:00",
                    "main": {
                        "feels_like": 299.95,
                        "grnd_level": 1004,
                        "humidity": 87,
                        "pressure": 1013,
                        "sea_level": 1013,
                        "temp": 299.03,
                        "temp_kf": 0,
                        "temp_max": 299.03,
                        "temp_min": 299.03
                    },
                    "pop": 0.71,
                    "rain": {"3h": 0.19},
                    "sys": {"pod": "d"},
                    "visibility": 10000,
                    "weather": [
                        {
                            "description": "light rain",
                            "icon": "10d",
                            "id": 500,
                            "main": "Rain"
                        }
                    ],
                    "wind": {"deg": 194, "gust": 4.91, "speed": 1.66}
                }
            ]
        }

        # Call the function with a sample zip code
        forecast = get_weekend_forecast('12345')

        # Check the response
        self.assertEqual(len(forecast), 1)
        self.assertEqual(forecast[0]['main']['temp'], 299.03)
        self.assertEqual(forecast[0]['weather'][0]['description'], 'light rain')

if __name__ == '__main__':
    unittest.main()
