import pandas as pd
import numpy as np
import openmeteo_requests
import numpy as np
from openmeteo_sdk.Variable import Variable

openmeteo = openmeteo_requests.Client()

url = "https://api.open-meteo.com/v1/forecast"


def elevation(lat: float, lon: float) -> float:
    '''
    Takes an elevation and a temperature and returns the air density
    of the environment (on earth).
    '''

    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": ["temperature_2m", "relative_humidity_2m"]
    }

    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

    e = response.Elevation()
    return e

def temp(lat, lon, start, end):

    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": ["temperature_2m", "relative_humidity_2m"]
    }

    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

    e = response.Elevation()

    hourly = response.Hourly()

    hourly_data = {"date": pd.date_range(
        start = pd.to_datetime(hourly.Time(), unit = "s"),
        end = pd.to_datetime(hourly.TimeEnd(), unit = "s"),
        freq = pd.Timedelta(seconds = hourly.Interval()),
        inclusive = "left"
    )}

    print(hourly_data)


def mol_m(lat, lon, start, end):



def density(T, e, mol_m):

    R = 8.314462  # J/(mol*K)
    P_0 = 101325  # Pa

    P = P_0 * (1 - 2.25577 * 10^(-5) * e) ** 5.25588
    output = P / (R * T)

    return output


def main():

    df = pd.read_csv('stadium_data.csv')
    lons = df['longitude']
    lats = df['lattitude']

    for lon, lat in zip(lons, lats):
        e = elevation(lat, lon)
        T = temp(lat, lon, 2024, 2025)
        mol_m = 



if __name__ == '__main__':
    main()
