# Team Power

`team_power(start_year, end_year, team)`

Gets team power stats ('ISO', 'HR rate', and 'SLG') for seasons in given range. Returns a pandas DataFrame.

## Arguements

`start_year:` Integer start year/season (2008 - 2025).

`end_year:` Integer start year/season (2008 - 2025).

`team:` String representing the team location. A valid example for the Seattle Mariners is 'Seattle'.

## Example

```python
import team_build

# find the split stats for the Seattle Mariners between 2008 and 2025
df = team_power(2008, 2025, 'Seattle')
```

# Relative Team Power

`rel_team_power(start_year, end_year, team)`

Gets team power stats ('ISO', 'HR rate', and 'SLG') for seasons in given range relative to league average. Returns a pandas DataFrame.

## Arguements

`start_year:` Integer start year/season (2008 - 2025).

`end_year:` Integer start year/season (2008 - 2025).

`team:` String representing the team location. A valid example for the Seattle Mariners is 'Seattle'.

## Example

```python
import team_build

# find the split stats for the Seattle Mariners between 2008 and 2025
df = rel_team_power(2008, 2025, 'Seattle')
```