#!/usr/bin/env python
# coding: utf-8

import argparse
from api import get_weekend_forecast

def main():
    parser = argparse.ArgumentParser(description='Get weekend weather forecast for a given zip code.')
    parser.add_argument('zip_code', type=str, help='Zip code for which to get the forecast')

    args = parser.parse_args()

    forecast = get_weekend_forecast(args.zip_code)
    print(forecast)

if __name__ == "__main__":
    main()
