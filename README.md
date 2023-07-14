# Weekend Weather

This project provides a Python package named `weather_api` that interacts with the OpenWeatherMap API to retrieve the weather forecast for the weekend. It also includes a `diagram` package that generates a flow chart diagram of the `weather_api` workflow.

## Requirements

- Python 3.10 or higher
- API key from OpenWeatherMap (more details in the **Configuration** section)

## Installation

1. Clone the repository: `git clone https://github.com/john-jiang-wa/weekend_weather.git`
2. Change into the project directory: `cd weekend_weather`
3. Install the dependencies: `pip install -r requirements.txt`

## Configuration

Before using the `weather_api` package, you need to obtain an API key from OpenWeatherMap. Then set your API key as an environment variable named `API_KEY` on your system. 

```
export API_KEY="YOUR_API_KEY"
```

## Usage

### API

The API allows you to retrieve the weekend weather forecast for a specific zip code.

1. Start the API server: `FLASK_APP=weather_api/api.py flask run --port={port_number}`. 

    Replace `{port_number}` with the desired port.

2. Open your web browser and navigate to `http://localhost:{port_number}/forecast/{zip_code}`. 

    Replace `{port_number}` and`{zip_code}` with the desired port and zip code.

    Example: `http://localhost:8000/forecast/12345`

3. The API will return a JSON response containing the weather forecast for the weekend.

### CLI

The CLI provides a command-line interface to retrieve the weekend weather forecast for a specific zip code.

```bash
python weather_api/cli.py {zip_code}
```

Replace `{zip_code}` with the desired zip code.

Example: `python -m weather_api.cli 12345`

The CLI will print the weather forecast for the weekend.

## Contributing

Contributions to the "Weekend Weather" project are welcome! If you find any issues or have suggestions for improvement, please open an issue or submit a pull request on the GitHub repository.

## License

This project is licensed under the [MIT License](https://opensource.org/license/mit/).
