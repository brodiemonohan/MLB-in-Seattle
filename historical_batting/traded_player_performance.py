'''
Brodie Monohan
CSE 163

This file defines the find_traded_player() function which looks at
average player performance on a team due to external factors by
comparing performance of recently traded players.
'''

# import data
import pybaseball
from pybaseball import batting_stats_bref

# libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# New library. Users of pybaseball have noted this is required
# due to blocks from repeated requests on the Baseball Reference
# website which pybaseball scrapes.
import time

pybaseball.cache.enable()  # store already scraped data locally


def find_traded_players(team: str, start_year: int = 2009,
                        end_year: int = 2025, min_PA: int = 0,
                        min_AB: int = 0) -> pd.DataFrame:
    '''
    This function takes a team location, a start year (inclusive),
    an end year (inclusive), and minimum PAs and ABs, and returns
    a pandas dataframe of the name of all of the players
    that were traded to or from that team, the year, the
    previous or next team, and their batting average on
    the given team. This may take a while (~3m max) to run
    becasue Baseball
    Reference blocks rapid requests so a sleep section is
    required between each call to the batting_stats_bref
    function. Ignores mid-season trades to or from specified
    team.
    '''

    # this is a slow function so this helps to know it is working.
    print('Running\n ...')

    # initialize output list for dataframe.
    traded_players = []

    for year in range(start_year, end_year + 1):

        # make this_year all player batting stats of that season.
        time.sleep(3)
        this_year = batting_stats_bref(year)

        if year > 2008:
            # make last_year all player batting stats of last season.
            # makes sure the last year data exists.
            time.sleep(3)
            last_year = batting_stats_bref(year - 1)

        if year < 2026:
            # make next_year all player batting stats of next season.
            # makes sure the next year data exists.
            time.sleep(3)
            next_year = batting_stats_bref(year + 1)

        # all three calls to batting_stats_bref return DataFrames
        # filter players in this_year df to only the specified team
        players_this_year = this_year[this_year['Tm'] == team]

        for i in players_this_year.index:

            # need to loop throuhg each row which is a unique player.
            row = players_this_year.loc[i]

            # pulls the player's name from their df row.
            name = row['Name']

            if year > 2008:

                # finds the same players row in the previous year.
                previous = last_year[last_year['Name'] == name]

                # Need to check that there is previous data otherwise error.
                if len(previous) > 0:

                    # the filtering above still returns a df even if
                    # there is only one entry row so I need to turn this
                    # into a series like the row of players_this_year.
                    # Need to use iloc becuase indicies are retained
                    # from pre-filter.
                    previous = previous.iloc[0]

                    # check input restrictions and for traded players.
                    # mid-season trades show up a both teams seperated
                    # by a comma so team must not be in previous or next
                    if (team not in previous['Tm']
                            and row['PA'] >= min_PA
                            and previous['PA'] >= min_PA
                            and row['AB'] >= min_AB
                            and previous['AB'] >= min_AB):

                        traded_players.append({
                            'Name': name,
                            'Years': str(year - 1) + ' -> ' + str(year),
                            'Teams': f'from {previous['Tm']}',
                            f'PA_{team}': row['PA'],
                            'PA_other': previous['PA'],
                            f'AB_{team}': row['AB'],
                            'AB_other': previous['AB'],
                            'HR/PA_diff': ((row['HR'] / row['PA'])
                                           - (previous['HR'] /
                                              previous['PA'])),
                            'SLG_diff': (row['SLG'] - previous['SLG']),
                            'BA_diff': (row['BA'] - previous['BA']),
                            'OBP_diff': (row['OBP'] - previous['OBP'])})

            if year < 2026:

                # next finds the same players row from the next year
                next = next_year[next_year['Name'] == name]

                # check data exists
                if len(next) > 0:

                    # same df -> series step and empty df check.
                    next = next.iloc[0]

                    # check inputs and traded player
                    if (team not in next['Tm']
                            and row['PA'] >= min_PA
                            and next['PA'] >= min_PA
                            and row['AB'] >= min_AB
                            and next['AB'] >= min_AB):

                        traded_players.append({
                            'Name': name,
                            'Years': str(year) + ' -> ' + str(year + 1),
                            'Teams': f'to {next['Tm']}',
                            f'PA_{team}': row['PA'],
                            'PA_other': next['PA'],
                            f'AB_{team}': row['AB'],
                            'AB_other': next['AB'],
                            'HR/PA_diff': ((row['HR'] / row['PA'])
                                           - (next['HR'] / next['PA'])),
                            'SLG_diff': (row['SLG'] - next['SLG']),
                            'BA_diff': (row['BA'] - next['BA']),
                            'OBP_diff': (row['OBP'] - next['OBP'])})

    print('Done')
    return pd.DataFrame(traded_players)


def main():

    # user input
    team = 'Seattle'
    stat1 = 'SLG'
    stat2 = 'OBP'
    stat3 = 'HR/PA'

    players = find_traded_players(team)

    stats = [stat1, stat2, stat3]

    fig, ax = plt.subplots(1, 3, figsize=(14, 5))

    df1 = players[(players['PA_Seattle'] > 320) & (players['PA_other'] > 320)]
    df2 = players[(players['PA_Seattle'] > 460) & (players['PA_other'] > 460)]
    df3 = players[(players['PA_Seattle'] > 170) & (players['PA_other'] > 170)]

    dfs = [df1, df2, df3]

    for i in range(3):

        xs = list(dfs[i][stats[i] + '_diff'])
        ax[i].hist(xs, color='grey', bins=8)

        # average marker
        ax[i].axvline(np.mean(xs), color='r', linestyle=':')

        # 0 lines
        ax[i].axvline(0.0, color='k', linestyle=':')

        ax[i].set_xlabel(f'{stats[i]}')
        ax[i].set_ylabel('Counts')

    # had to look up how to do this
    fig.suptitle('Traded Player Splits')
    plt.savefig('traded_player_performance.png', bbox_inches='tight')


if __name__ == '__main__':
    main()
