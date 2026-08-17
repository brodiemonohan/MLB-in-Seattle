# Get Split Stat

`get_split(home_stats, away_stats, stat, min_PA, min_AB)`

Filter home and away stats from `home_away_splits` to the home difference and a single stat. Returns a pandas DataFrame.

## Arguments

`home_stats:` Pandas DataFrame containing home stats with player names as indicies as output from `home_away_splits`.

`away_stats:` Pandas DataFrame containing away stats with player names as indicies as output from `home_away_splits`.

`stat:` String representing the chosen stat. A valid example would be 'OBP'.

`min_PA` Optional integer representing the minimum plate apperances a player must have to be included in the output.

`min_BA` Optional integer representing the minimum at-bats a player must have to be included in the output.

## Example:

```python
import travel_player_splits

# find the split stats for the Seattle Mariners between 2008 and 2025
home, away = home_away_split(2008, 2025, 'Seattle')

# find the OBP split for Mariners with at least 460 plate appearances at home and away
# where more negative means worse performance at home and vis versa.
df = get_split(home, away, 'OBP', min_PA = 460)
```