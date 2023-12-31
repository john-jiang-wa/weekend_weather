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

Before using the `weather_api` package, you need to obtain an API key from [OpenWeatherMap](https://openweathermap.org/api). Then set your API key as an environment variable named `API_KEY` on your system. 


For Unix-like systems:

```bash
export API_KEY="YOUR_API_KEY"
```

For Windows systems (using PowerShell):

```powershell
$env:API_KEY="YOUR_API_KEY"
```

## Usage

### Weather API

The API allows you to retrieve the weekend weather forecast for a specific zip code.

1. Start the API server: 

    For Unix-like systems:

    ```bash
    FLASK_APP=weather_api/api.py flask run --port={port_number}
    ```

    For Windows systems (using PowerShell):

    ```powershell
    $env:FLASK_APP="weather_api/api.py"
    flask run --port={port_number}
    ```

    Replace `{port_number}` with the desired port.

2. Open your web browser and navigate to `http://localhost:{port_number}/forecast/{zip_code}`. 

    Replace `{port_number}` and`{zip_code}` with the desired port and zip code.

    Example: `http://localhost:8000/forecast/12345`

3. The API will return a JSON response containing the weather forecast for the weekend.

### Weather CLI

The CLI provides a command-line interface to retrieve the weekend weather forecast for a specific zip code.

```bash
python weather_api/cli.py {zip_code}
```

Replace `{zip_code}` with the desired zip code.

Example: `python -m weather_api.cli 12345`

The CLI will print the weather forecast for the weekend.

### Diagram Generator

The diagram generator creates a flowchart of the code in the specified directory.

```
python diagram/generate_diagram.py --directory weather_api --output weather_api.html
```

This will create an HTML file `weather_api.html` in the project directory, which contains a flowchart of the `weather_api` code.

## Contributing

Contributions to the "Weekend Weather" project are welcome! If you find any issues or have suggestions for improvement, please open an issue or submit a pull request on the GitHub repository.

## License

This project is licensed under the [MIT License](https://opensource.org/license/mit/).
