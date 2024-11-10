from datetime import datetime
import requests, os
from typing import Dict, Any
import time
import psutil
from typing import List, Tuple

def get_weather(city: str, country: str, api_key: str  = os.getenv("WEATHER_API_KEY")) -> Dict[str, Any]:
    """
    Retrieves current weather information for a specified city and country.

    This function uses the WeatherAPI to get weather data, including temperature, 
    humidity, wind speed, and general weather description. An API key is required to 
    access the service.

    Args:
        city (str): The name of the city for which to retrieve weather information.
        country (str): The two-letter country code (ISO 3166) of the country.
        api_key (str): Your API key for the WeatherAPI.

    Returns:
        Dict[str, Any]: A dictionary containing weather information, including temperature,
                        humidity, weather description, and wind speed.

    Raises:
        requests.exceptions.RequestException: If there is an issue with the API request.
        ValueError: If the response does not contain valid weather data.

    Example:
        >>> get_weather("Berlin", "DE", "YOUR_API_KEY")
        {
            'city': 'Berlin',
            'temperature_celsius': 15.2,
            'humidity': 82,
            'description': 'Partly cloudy',
            'wind_kph': 18.5
        }
    """
    try:
        # Construct the API URL with the provided parameters
        url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city},{country}"
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        data = response.json()
        
        # Parse and return relevant weather information
        weather_info = {
            'city': data['location']['name'],
            'temperature_celsius': data['current']['temp_c'],
            'humidity': data['current']['humidity'],
            'description': data['current']['condition']['text'],
            'wind_kph': data['current']['wind_kph']
        }
        return weather_info
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve weather data: {e}")
        raise
    except ValueError as e:
        print("Invalid response format received.")
        raise

def get_current_time():
    """
    Returns the current time as a formatted string.

    This function uses the datetime module to fetch the current time 
    in the format 'HH:MM:SS'.

    Returns:
        str: The current time in 'HH:MM:SS' format.
    
    Example:
        >>> get_current_time()
        '14:23:56'
    """
    # Get the current time using datetime.now() and format it to 'HH:MM:SS'
    current_time = datetime.now().strftime("%H:%M:%S")
    return current_time

def get_public_ip() -> str:
    """
    Retrieves the public IP address of the current machine.

    This function makes an HTTP GET request to a public IP API service (such as "https://api.ipify.org").
    It returns the IP address as a string. The IP service used here is free and widely available.
    
    Returns:
        str: The public IP address of the machine in IPv4 format.
    
    Raises:
        requests.exceptions.RequestException: If there is an issue connecting to the IP service.
        ValueError: If the response from the service is not in a valid format.

    Example:
        >>> get_public_ip()
        '192.168.1.1'
    """
    try:
        # Using ipify API to fetch the public IP address
        response = requests.get("https://api.ipify.org", params={"format": "text"})
        response.raise_for_status()  # Check if the request was successful
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve IP address: {e}")
        raise

import requests
from typing import Dict, Any

def get_location_by_ip(ip_address: str = None) -> Dict[str, Any]:
    """
    Retrieves geographical location information based on a given IP address.

    This function makes a request to the `ipinfo.io` service to fetch location data.
    If no IP address is provided, the service will use the public IP of the current machine.
    The function returns a dictionary with location details, including city, region, country, and more.

    Args:
        ip_address (str, optional): The IP address to retrieve location information for.
                                    If not provided, it defaults to the public IP of the caller.

    Returns:
        Dict[str, Any]: A dictionary containing location information such as city, region, country, 
                        latitude, longitude, and timezone.

    Raises:
        requests.exceptions.RequestException: If there is an issue with the API request.
        ValueError: If the response does not contain valid location data.

    Example:
        >>> get_location_by_ip()
        {
            'ip': '203.0.113.195',
            'city': 'Mountain View',
            'region': 'California',
            'country': 'US',
            'loc': '37.3860,-122.0838',
            'org': 'AS15169 Google LLC',
            'timezone': 'America/Los_Angeles'
        }
    """
    try:
        # Use ipinfo.io API to fetch location data based on IP
        url = f"https://ipinfo.io/{ip_address if ip_address else ''}/json"
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve location data: {e}")
        raise
    except ValueError as e:
        print("Invalid response format received.")
        raise



def get_cpu_usage() -> float:
    """
    Retrieves the current CPU usage percentage of the machine.

    This function uses the `psutil` library to check the CPU utilization in real-time.
    It can help in monitoring system health or making decisions based on resource availability.

    Returns:
        float: The current CPU usage percentage.

    Example:
        >>> get_cpu_usage()
        23.5
    """
    return psutil.cpu_percent(interval=1)

def get_memory_usage() -> Dict[str, float]:
    """
    Retrieves the current memory usage of the system.

    This function uses the `psutil` library to retrieve memory statistics and calculates
    the percentage of used memory. It can help monitor system performance.

    Returns:
        Dict[str, float]: A dictionary containing memory usage details, including total,
                          available, used memory in MB, and usage percentage.

    Example:
        >>> get_memory_usage()
        {'total_mb': 8192, 'available_mb': 4096, 'used_mb': 4096, 'percent': 50.0}
    """
    memory = psutil.virtual_memory()
    return {
        'total_mb': memory.total / (1024 ** 2),
        'available_mb': memory.available / (1024 ** 2),
        'used_mb': memory.used / (1024 ** 2),
        'percent': memory.percent
    }

def retry_request(url: str, retries: int = 3, delay: int = 2) -> Any:
    """
    Makes an HTTP GET request with retry logic in case of failure.

    This function attempts to send an HTTP GET request to a specified URL. If the request
    fails, it will retry up to a specified number of attempts, waiting a set number of seconds
    between each retry.

    Args:
        url (str): The URL to which the GET request is sent.
        retries (int): Number of retry attempts in case of failure (default is 3).
        delay (int): Delay in seconds between retries (default is 2 seconds).

    Returns:
        Any: The response data if the request is successful.

    Raises:
        requests.exceptions.RequestException: If the request fails after all retries.

    Example:
        >>> retry_request("https://example.com/api/data")
        {'data': {...}}
    """
    attempt = 0
    while attempt < retries:
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            attempt += 1
            time.sleep(delay)
    raise requests.exceptions.RequestException(f"Failed to retrieve data from {url} after {retries} attempts")

def check_disk_space() -> Dict[str, float]:
    """
    Checks the disk space usage on the primary disk.

    This function uses the `psutil` library to check the total, used, and free disk space
    on the primary drive. It is useful for monitoring storage usage in a system.

    Returns:
        Dict[str, float]: A dictionary containing disk space information in GB, including
                          total, used, free space, and usage percentage.

    Example:
        >>> check_disk_space()
        {'total_gb': 256.0, 'used_gb': 128.0, 'free_gb': 128.0, 'percent': 50.0}
    """
    disk = psutil.disk_usage('/')
    return {
        'total_gb': disk.total / (1024 ** 3),
        'used_gb': disk.used / (1024 ** 3),
        'free_gb': disk.free / (1024 ** 3),
        'percent': disk.percent
    }

def parse_iso_datetime(iso_date_str: str) -> Tuple[int, int, int, int, int, int]:
    """
    Parses an ISO 8601 formatted date-time string and returns its components.

    This function takes a date-time string in ISO format (e.g., "2023-10-05T14:48:00")
    and extracts the year, month, day, hour, minute, and second as individual components.

    Args:
        iso_date_str (str): The ISO 8601 formatted date-time string to parse.

    Returns:
        Tuple[int, int, int, int, int, int]: A tuple containing the year, month, day, hour,
                                             minute, and second.

    Example:
        >>> parse_iso_datetime("2023-10-05T14:48:00")
        (2023, 10, 5, 14, 48, 0)
    """
    try:
        dt = datetime.fromisoformat(iso_date_str)
        return dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second
    except ValueError:
        raise ValueError(f"Invalid ISO date-time format: {iso_date_str}")

from datetime import datetime

def get_formatted_time(format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Retrieves the current date and time in a specified format.

    This function allows customization of the date-time format using standard
    Python date format codes. By default, it returns the current date and time
    in the format 'YYYY-MM-DD HH:MM:SS'.

    Args:
        format (str): The format in which to return the date-time string.
                      Defaults to "%Y-%m-%d %H:%M:%S".

    Returns:
        str: The current date and time in the specified format.

    Example:
        >>> get_formatted_time()
        '2023-11-10 15:30:45'
    """
    return datetime.now().strftime(format)

def add_numbers(a: float, b: float) -> float:
    """
    Adds two numbers and returns the result.

    This function takes two numeric inputs (int or float) and returns their sum.
    It can handle integers or floating-point numbers.

    Args:
        a (float): The first number to add.
        b (float): The second number to add.

    Returns:
        float: The sum of the two numbers.

    Example:
        >>> add_numbers(5, 3)
        8
        >>> add_numbers(5.5, 3.2)
        8.7
    """
    return a + b
