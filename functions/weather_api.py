import openmeteo_requests
from langchain_core.tools import tool
import requests_cache
import pandas as pd
from retry_requests import retry


@tool
def get_weather() -> pd.DataFrame:
	"""
	A function that gets the weather forecast for the next 24 hours in Hayling Island sailing club channel.
	Wind speed unit is knots
	:return:
	"""
	cache_session = requests_cache.CachedSession(cache_name='.cache', expire_after = 3600)
	retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
	openmeteo = openmeteo_requests.Client(session = retry_session)

	url = "https://api.open-meteo.com/v1/forecast"
	params = {
		"latitude": 50.7838,
		"longitude": -0.9687,
		"hourly": ["wind_speed_10m", "wind_speed_80m", "wind_direction_10m", "wind_direction_80m",  "wind_gusts_10m"],
		"wind_speed_unit": "kn",
		"timeformat": "unixtime",
		"forecast_days": 1
	}
	responses = openmeteo.weather_api(url, params=params)

	response = responses[0]

	hourly = response.Hourly()
	hourly_wind_speed_10m = hourly.Variables(0).ValuesAsNumpy()
	hourly_wind_speed_80m = hourly.Variables(1).ValuesAsNumpy()
	hourly_wind_gusts_10m = hourly.Variables(2).ValuesAsNumpy()

	hourly_data = {"date": pd.date_range(
		start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
		end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
		freq = pd.Timedelta(seconds = hourly.Interval()),
		inclusive = "left"
	)}

	hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
	hourly_data["wind_speed_80m"] = hourly_wind_speed_80m
	hourly_data["wind_gusts_10m"] = hourly_wind_gusts_10m

	hourly_dataframe = pd.DataFrame(data = hourly_data)
	return hourly_dataframe
