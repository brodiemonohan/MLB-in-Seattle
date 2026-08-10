import pandas as pd
import numpy as np
import openmeteo_requests
from openmeteo_sdk.Variable import Variable
import requests
from datetime import timedelta

openmeteo = openmeteo_requests.Client()

url_om = "https://archive-api.open-meteo.com/v1/archive"
url_mlb = "https://statsapi.mlb.com/api/v1/schedule"


def elevation(lon: float, lat: float) -> float:
    '''
    Takes an elevation and a temperature and returns the air density
    of the environment (on earth).
    '''

    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": ["temperature_2m", "relative_humidity_2m"]
    }

    responses = openmeteo.weather_api(url_om, params=params)
    response = responses[0]

    e = response.Elevation()
    return e


def hour_rounder(t):
    # Rounds to nearest hour by adding a timedelta hour if minute >= 30
    return (t.replace(second=0, microsecond=0, minute=0, hour=t.hour)
            + timedelta(hours=t.minute//30))


def start_times(year: int = 2025, venue_id: int = 680) -> list[str]:
    '''
    '''
    params = {
        "sportId": 1,
        "season": year,
        "venueIds": venue_id,
    }

    resp = requests.get(url_mlb, params=params).json()

    start_times = []

    for date_entry in resp["dates"]:
        for game in date_entry["games"]:
            start_times.append(hour_rounder(
                pd.to_datetime(game["gameDate"], utc=True)))

    return pd.Series(start_times)


def temp_data(lon, lat, year):
    '''
    '''
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": (str(year) + '-01-01'),
        "end_date": (str(year) + '-12-31'),
        "hourly": ["temperature_2m"],
        "timezone": "UTC",  # keep aligned with game_date_utc
    }

    responses = openmeteo.weather_api(url_om, params=params)
    response = responses[0]

    hourly = response.Hourly()
    hourly_variables = list(map(lambda i: hourly.Variables(i),
                                range(0, hourly.VariablesLength())))

    hourly_temperature_2m = next(
        filter(
            lambda x: x.Variable() == Variable.temperature
            and x.Altitude() == 2,
            hourly_variables
        )
    ).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    )}

    hourly_data["temperature_2m"] = hourly_temperature_2m
    hourly_dataframe_pd = pd.DataFrame(data=hourly_data)

    df = hourly_dataframe_pd.groupby('date')['temperature_2m'].mean()
    return df


def average_temp(lon, lat, year: int = 2025, venue_id: int = 680):
    T = temp_data(lon, lat, year)
    s = start_times(year, venue_id)
    temps = []
    for timestamp in s:
        temps.append(T[timestamp])
    ts = np.array(temps)
    return ts.mean() + 274.15


def density(T, e, kg_mol):

    R = 8.314462  # J/(mol*K)
    P_0 = 101325  # Pa

    P = P_0 * (1 - 2.25577 * 10 ** (-5) * e) ** 5.25588
    rho_mol = P / (R * T)  # mol / m^3

    return rho_mol * kg_mol


def main():

    df = pd.read_csv('stadium_data.csv')
    lons = df['longitude']
    lats = df['latitude']
    stadiums = df['stadium']
    ids = df['venue_id']

    output = []

    for lon, lat, stadium, id in zip(lons, lats, stadiums, ids):
        d = {}
        T = average_temp(lon, lat, venue_id=id)
        e = elevation(lon, lat)
        rho = density(T, e, 0.0289647)
        d[stadium] = rho
        output.append(d)

    print(output)
