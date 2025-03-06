import openmeteo_requests
import requests_cache
from retry_requests import retry


def downloadWeather():
  # Setup the Open-Meteo API client with cache and retry on error
  cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
  retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
  openmeteo = openmeteo_requests.Client(session = retry_session)

  # Make sure all required weather variables are listed here
  # The order of variables in hourly or daily is important to assign them correctly below
  url = "https://api.open-meteo.com/v1/forecast"
  params = {
      "latitude": 53.6023417,
      "longitude": 11.4311637,
      "current": ["temperature_2m", "weather_code","is_day"],
      "timezone": "Europe/Berlin"
  }
  responses = openmeteo.weather_api(url, params=params)

  # Process first location. Add a for-loop for multiple locations or weather models
  response = responses[0]
  # print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
  # print(f"Elevation {response.Elevation()} m asl")
  # print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
  # print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")


  # Current values. The order of variables needs to be the same as requested.
  current = response.Current()

  current_temperature_2m = current.Variables(0).Value()
  current_weather_code = current.Variables(1).Value()
  current_is_day = current.Variables(2).Value()


  current_weather_string = getWeatherString(current_weather_code, current_is_day)
  return {
    "temp" : current_temperature_2m,
    "weather" : current_weather_string
  }

  # print(f"Current time {current.Time()}")
  #
  # print(f"Current temperature_2m {current_temperature_2m}")
  # print(f"Current weather_code {current_weather_code}")


def getWeatherString(code: float, isDay: float) -> str:
  weatherCodes = {
    0: "Klarer Himmel",
    1: "Meist klar",
    2: "Teilw. bewölkt",
    3: "Bedeckt",
    45: "Nebel",
    48: "Reifnebel",
    51: "Leicht Niesel",
    53: "Mäßig Niesel",
    55: "Stark Niesel",
    56: "Leicht gefr. Nies",
    57: "Stark gefr. Nies",
    61: "Leichter Regen",
    63: "Mäßiger Regen",
    65: "Starker Regen",
    66: "Leicht gefr. Reg",
    67: "Stark gefr. Reg",
    71: "Leicht Schneef.",
    73: "Mäßig Schneef.",
    75: "Stark Schneef.",
    77: "Schneekörner",
    80: "Leichter Schauer",
    81: "Mäßiger Schauer",
    82: "Starker Schauer",
    85: "Leicht Schneesch.",
    86: "Stark Schneesch.",
    95: "Gewitter",
    96: "Gewitter, Hagel",
    99: "Starkes Gewitter"
  }
  value = weatherCodes.get(int(code), "Unbekannter Code")

  if isDay == 1.0:
    match value:
      case "Klarer Himmel": value = "Sonnig"
      case "Meist klar": value = "Meist Sonnig"

  return value
