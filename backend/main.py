from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import openmeteo_requests
import requests_cache
import pandas as pd
import numpy as np
from retry_requests import retry
import requests
from datetime import datetime, timedelta

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

WEATHER_API_URL = "https://historical-forecast-api.open-meteo.com/v1/forecast"
GEOCODING_API_URL = "https://geocoding-api.open-meteo.com/v1/search"

cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

async def get_coordinates(city: str):
    """Fetches latitude and longitude for a city using Open-Meteo's geocoding API."""
    params = {"name": city, "count": 1}
    response = requests.get(GEOCODING_API_URL, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch city coordinates")

    data = response.json()
    if not data.get("results"):
        raise HTTPException(status_code=404, detail="City not found")

    location = data["results"][0]
    return location["latitude"], location["longitude"]

@app.get("/weather/average")
async def get_average_temperature(city: str, days: int):
    if days <= 0:
        raise HTTPException(status_code=400, detail="Days must be greater than 0")

    latitude, longitude = await get_coordinates(city)

    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "hourly": "temperature_2m",
    }

    try:
        responses = openmeteo.weather_api(WEATHER_API_URL, params=params)
        response = responses[0]

        hourly = response.Hourly()
        hourly_temperature_2m = np.array(hourly.Variables(0).ValuesAsNumpy(), dtype=float)

        hourly_data = {
            "date": pd.date_range(
                start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=hourly.Interval()),
                inclusive="left"
            ),
            "temperature_2m": hourly_temperature_2m
        }
        hourly_dataframe = pd.DataFrame(data=hourly_data)

        average_temp = hourly_dataframe["temperature_2m"].tail(days * 24).mean()

        return {
            "city": city,
            "days": days,
            "average_temperature": round(float(average_temp), 2)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching weather data: {str(e)}")
