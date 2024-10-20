import requests
from langchain_core.tools import tool

@tool
def get_sunrise_sunset():
    """
    A function that gets the sunrise and sunset times for Hayling Island Sailing Club
    :return:
    """
    latitude= 50.7838 # HISC
    longitude= -0.9687

    url = f"https://api.sunrisesunset.io/json?lat={latitude}&lng={longitude}"

    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful
    data = response.json()  # Parse the response JSON

    if 'results' in data:
        sunrise = data['results']['sunrise']
        sunset = data['results']['sunset']
        return f"The sunrise is at {sunrise} and the sunset is at {sunset}."

