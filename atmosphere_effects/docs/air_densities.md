# Elevation

`elevation(lon, lat)`

Takes a latitude and logitude from `stadium_data.csv` and returns the elevation in m from `openmateo-requests`.

## Arguments

`lon:` Float representing stadium longitude

`lat:` Float representing stadium latitude

## Example

```python
import air_densities as ad
import pandas as pd

df = pd.read_csv('stadium_data.csv')
lons = df['longitude']
lats = df['latitude']
stadiums = df['stadium']

output = []

for lon, lat, stadium in zip(lons, lats, stadiums):
    d = {}
    e = ad.elevation(lon, lat)
    d[stadium] = e
    output.append(d)

print(output)
```

# Temperature

`temperature(lon, lat, year, venue_id)`

Takes a latitude, logitude from `stadium_data.csv`, year, and a venue id and returns the average temperature during the start of games over the given year/season from `openmateo-requests` and `mlbstats-api`.

## Arguments

`lon:` Float representing stadium longitude

`lat:` Float representing stadium latitude

`year:` Optional integer representing a season/year range. Defaults to 2025.

`venue_id:` Optional integer representing a current stadium ID from https://statsapi.mlb.com/api/v1/venues. Defaults to 680 (T-Mobile Park).

## Example

```python
import air_densities as ad
import pandas as pd

df = pd.read_csv('stadium_data.csv')
lons = df['longitude']
lats = df['latitude']
stadiums = df['stadium']
ids = df['venue_id']

output = []

for lon, lat, stadium in zip(lons, lats, stadiums):
    d = {}
    T = ad.average_temp(lon, lat, venue_id=id)
    d[stadium] = T
    output.append(d)

print(output)
```

# Air Density

`density(T, e, kg_mol)`

Takes temperature and elevation data as well as the mass of a mol of dry air and returns the air density via the barometric equation and the ideal gas law.

## Arguments

`T:` Float representing the temperature of the environment in kelvin.

`e:` Float representing the elevation of the environment above sea-level in meters.

`kg_mol:` Optional float representing the mass of a mol of air. Defaults to the mass of dry air (0.0289647 kg/mol).

## Example

```python
import air_densities as ad
import pandas as pd

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
```