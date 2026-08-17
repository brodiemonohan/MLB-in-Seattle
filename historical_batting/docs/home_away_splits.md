# Get Home and Away Stats

`home_away_splits(start_year, end_year, team)`

Find the split stats of every player that played at least one full season for the given team between the given years. Either the home, away or both can be returned as a pandas DataFrame with the player names as indicies.

## Arguments

`start_year:` Integer start year/season (2008 - 2025).

`end_year:` Integer start year/season (2008 - 2025).

`team:` String representing the team location. A valid example for the Seattle Mariners is 'Seattle'.

## Example:

```python
import travel_player_splits

# find the split stats for the Seattle Mariners between 2008 and 2025
home_df, away_df = home_away_split(2008, 2025, 'Seattle')
```