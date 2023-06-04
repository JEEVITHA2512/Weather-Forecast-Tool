import contextlib
import json
import urllib
import requests
import typer
from datetime import datetime
from decouple import config
from rich import box, print
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from about import print_about_app
from banner import print_banner

import logging

API_KEY = config('API_KEY')
console = Console(record=False, color_system="truecolor")

# Create and configure logger
logging.basicConfig(filename="weather.log", format='%(asctime)s %(message)s',filemode='a')

# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to INFO
logger.setLevel(logging.INFO)


# app info 
app = typer.Typer(
    name="Weather CLI (Built by @Jeevitha) with the power of Github Copilot ",
    add_completion=False,
    rich_markup_mode="rich",
    help="📕[bold green] Easy to use weather data fetcher and forecaster center within your terminal [/bold green]",
)


@app.command(rich_help_panel="Weather CLI", help="🎫 Shows information about the CLI")
def about():
    """
    Print the about banner for the app. 
    """
    print_banner(console)
    print_about_app()


def print_weather(data):
    """
    This function takes in a dictionary of weather data, which is a JSON response from the API request and prints out the current weather information and forecast for the given location.
    The dictionary must contain location, current, and forecast keys. The location key must contain name, region, and country subkeys.
    The current key must contain temp_f, temp_c, condition, wind_mph, wind_dir, and humidity subkeys.
    The forecast key must contain forecastday subkeys, which is a list of dictionaries. Each dictionary must contain date, day, and condition subkeys.
    The function does not return anything.
    """
    
    # get the current location
    location = data['location']['name']
    region = data['location']['region']
    country = data['location']['country']
    address = f"{location}, {region}, {country}"

    current_temp_farenheit = data['current']['temp_f']
    current_temp_celsius = data['current']['temp_c']
    current_condition = data['current']['condition']['text']

    current_wind_mph = data['current']['wind_mph']
    current_wind_direction = data['current']['wind_dir']
    current_humidity = data['current']['humidity']
    # get current date in human readable format
    date = datetime.now().strftime('%d %B %Y')
    table = Table(
            show_header=True,
            header_style="bold gold3",
            border_style="white",
            title=f"\n📰 CURRENT WEATHER | {date}\n",
            title_style="bold white on black",
            title_justify="center",
            box=box.SIMPLE_HEAVY
        )

    table.add_column("📍 Location", width=40, style="green", justify="center")
    table.add_column("🌡️ Current Temperature", width=20, style="blue", justify="center")
    table.add_column("🌬️ Current Wind Speed", width=25, style="yellow", justify="center")
    table.add_column("💧 Current Humidity", width=20, style="violet", justify="center")
    table.add_column("🌤️ Current Condition", width=30, style="dark_orange3", justify="center")

    table.add_row(address, f"{current_temp_celsius}°C", f"{current_wind_mph} mph, {current_wind_direction}", f"{current_humidity}%", current_condition)
    print("\n\n")
    console.print(table)
    print("\n\n")

    total_forecast_days = len(data['forecast']['forecastday'])
    table = Table(
            show_header=True,
            header_style="bold gold3",
            border_style="white",
            title=f"\n📰 FORECAST FOR THE NEXT {total_forecast_days} DAYS\n",
            title_style="bold white on black",
            title_justify="center",
            box=box.SIMPLE_HEAVY
        )

    table.add_column("📅 Date", width=12, style="bold blue", justify="center")
    table.add_column("📈 Max Temp °C", width=14, style="bold green", justify="center")
    table.add_column("📉 Min Temp °C", width=14, style="bold red", justify="center")
    table.add_column("🌡️ Avg Temp °C ", width=15, style="bold yellow", justify="center")
    table.add_column("🌬️ Max Wind (kph)", width=18, style="bold magenta", justify="center")
    table.add_column("💧 Rain (mm)", width=15, style="bold cyan", justify="center")
    table.add_column("🌤️ Condition", width=20, style="bold dark_orange3", justify="center")
    table.add_column("🌞 UV", width=5, style="bold violet", justify="right")
    table.add_column("💧 Humidity", width=10, style="bold dark_orange3", justify="right")

    for day in range(1, total_forecast_days):
        day_json = data['forecast']['forecastday'][day]
        date = day_json['date']

        # convert date to datetime object and then into human readable format
        date = datetime.strptime(date, '%Y-%m-%d').strftime('%d %B %Y')

        max_temp_celsius = day_json['day']['maxtemp_c']
        min_temp_celsius = day_json['day']['mintemp_c']
        avg_temp_celsius = day_json['day']['avgtemp_c']
        max_wind_kph = day_json['day']['maxwind_kph']
        total_precip_mm = day_json['day']['totalprecip_mm']
        condition = day_json['day']['condition']['text']
        uv = day_json['day']['uv']
        humidity = day_json['day']['avghumidity']

        # convert all values to string
        max_temp_celsius = str(max_temp_celsius)
        min_temp_celsius = str(min_temp_celsius)
        avg_temp_celsius = str(avg_temp_celsius)
        max_wind_kph = str(max_wind_kph)
        total_precip_mm = str(total_precip_mm)
        uv = str(uv)
        humidity = str(humidity)

        table.add_row(date, max_temp_celsius, min_temp_celsius, avg_temp_celsius, max_wind_kph, total_precip_mm, condition, uv, humidity)

    console.print(table)
    print()
    


@app.command(rich_help_panel="Weather CLI", help="🎫 Get the weather forecast for a city")
def forecast(city:str = typer.Argument(..., help="🏙️ City name")):
    """
    Retrieves the weather forecast for a given city from the WeatherAPI. If the forecast for that city is already saved in a 'data.json' file, it returns the cached data. If the cached data is outdated or does not exist, it sends a GET request to the WeatherAPI and saves the response to the 'data.json' file. 

    Args:
        city (str): City name.
        
    Returns:
        None
    """
    
    try:
        data = None
        file_exists = False

        # Check if the data.json file exists
        with contextlib.suppress(FileNotFoundError):
            with open('data.json') as f:
                data = json.load(f)
            file_exists = True
        if file_exists:
            # check if city.lower is a substring of data['location']['name'].lower()
            name_exists = city.lower() in data['location']['name'].lower() 
            fetched_today = data['fetched_on'].split(',')[0] == datetime.now().strftime("%d %B %Y")
            no_errors = not data.get('error')

            if name_exists and fetched_today and no_errors:
                logger.info(msg=f"**CACHE HIT!** User requested for ***{city}***.")
                print_weather(data)
                return

        logger.info(msg=f"**CACHE MISS!** Making a request to the WeatherAPI for ***{city}***.")
        # Add parameters to the URL
        url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=6&aqi=no&alerts=no"

        # Send GET request
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Get JSON response
            data = response.json()

            # Check if the response contains any errors
            if 'error' not in data:
                # Add a field to the JSON data called "fetched_on" and set it to the current date
                data['fetched_on'] = datetime.now().strftime("%d %B %Y, %H:%M:%S")

                # Dump to a JSON file
                with open('data.json', 'w') as f:
                    json.dump(data, f)
                print_weather(data)
            else:
                print(f"Error: {data['error']['message']}")
        else:
            print("[b red]🚨 Error: Failed to retrieve weather data. Please enter a valid city.[/b red]")

    except KeyError:
        print("[red b]🚨 The city you entered does not exist.[/red b] Please try again.")
    except requests.exceptions.Timeout:
        print("The server didn't respond. Please try again later.")
    except requests.exceptions.TooManyRedirects:
        print("The URL was bad. Try a different one.")
    except requests.exceptions.RequestException as e:
        raise SystemExit(e) from e
 
 
@app.command(rich_help_panel="Weather CLI", help="🎫 See history of forecast lookups")
def history():
    """
    Refer the weather.log file for the history of lookups. The weather.log file contains the date and time of the lookup, the city name. Parse it and display it in a table.
    """
    
    # read the weather.log file
    with open('weather.log', 'r') as f:
        data = f.readlines()
        
    # get the first 10 characters of each line
    dates = [line[:18] for line in data]
    
    # convert all objects in data to datetime object 
    dates = [datetime.strptime(line, '%Y-%m-%d %H:%M:%S') for line in dates]
    
    # convert all dates to human readable format with h:m:s
    dates = [line.strftime('%d %B %Y, %H:%M:%S') for line in dates]
    
    # split each line on the third **
    cities = [line.split('***') for line in data]
    
    # get the second element of each line
    cities = [line[1] for line in cities]
    
    # reverse both lists
    cities = cities[::-1]
    dates = dates[::-1]
    
    # zip and iterate over the two lists
    cities = list(zip(dates, cities))
    
    # make a table
    table = Table(show_header=True, header_style="bold magenta", title="History of forecast lookups")
    table.add_column("Date", justify="center")
    table.add_column("City", justify="center")
    
    for date, city in cities:
        table.add_row(date, city)
         
    console.print(table)
    

if __name__ == "__main__":
    app()