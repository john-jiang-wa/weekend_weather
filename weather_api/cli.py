#!/usr/bin/env python
# coding: utf-8

import argparse
import logging
from api import get_weekend_weather

def main():
    parser = argparse.ArgumentParser(description="Get the weekend weather for a given zip code.")
    parser.add_argument('zip_code', help='The zip code to get the weather for.')
    args = parser.parse_args()

    logging.getLogger().setLevel(logging.WARNING)

    weekend_weather, status_code = get_weekend_weather(args.zip_code)

    if status_code == 200:
        print("Weekend Weather:")
        print(weekend_weather)
    else:
        print("An error occurred while fetching the weather:")
        print(weekend_weather['error'])

if __name__ == "__main__":
    main()
