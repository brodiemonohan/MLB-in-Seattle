'''
Brodie Monohan
CSE 163

This file defines the home_away_split() and find_split() functions which
look at average player performance on a team due to external factors by
comparing performance of recently traded players.
'''

# import data
import pybaseball
from pybaseball import batting_stats_bref, get_splits, playerid_reverse_lookup
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt

pybaseball.cache.enable()


def home_away_splits(start_year: int = 2008, end_year:
                     int = 2025, team: str = 'Seattle') -> pd.DataFrame:
    '''
    Takes a year range and a team. Returns the home and away
    stats for every player that played at least a full season
    for the given team.
    '''

    home_tot = []
    away_tot = []

    # this function took up to 45 mins when I ran it...
    print('Running')
    print('...')

    for year in range(start_year, end_year + 1):

        # add sleep sections to not hit limits for rapid scraping
        # from baseball reference
        time.sleep(1)

        # get a list of players who played this season like in
        # traded_players
        this_year = batting_stats_bref(year)

        # filter for specified team. I really only need the name here.
        # there was probably a simpler way to do this but I ge to re-use
        # my framework from the traded_plyers function here
        players_this_year = this_year[this_year['Tm'] == team]

        # the next function I will use from pybaseball needs the IDs
        # in a specific style which I need to convert to here. Here I
        # am making a key to find the mlb-id from the bbref ID for
        # inside the upcoming loop
        mlb_ids = list(players_this_year['mlbID'])
        ids = playerid_reverse_lookup(mlb_ids, key_type='mlbam')

        # loop through each player in the players df
        for i in players_this_year.index:

            d_home = {}
            d_away = {}

            # find mlb-id from keys
            row = players_this_year.loc[i]
            name = row['Name']
            mlb_id = row['mlbID']
            match = ids[ids['key_mlbam'] == mlb_id]
            bbref_id = match['key_bbref'].iloc[0]

            # sleep then find split stats
            time.sleep(1)
            df = get_splits(bbref_id, year=year)

            # filter for just home vs away splits then reset index
            home_away = df.loc['Home or Away']
            home_away = home_away.reset_index()

            # put name back in
            home_away['Name'] = name

            # split into seperate home and away dfs
            home = home_away[home_away['Split'] == 'Home']
            away = home_away[home_away['Split'] == 'Away']

            # make sure the player played at least one game at home and away
            if (len(home['G']) > 0) and (len(away['G']) > 0):

                # save all stats to a list of dictionaries
                # there was probably a much better way to do this
                # but I dont know it.
                g = home['G'].iloc[0]
                gs = home['GS'].iloc[0]
                pa = home['PA'].iloc[0]
                ab = home['AB'].iloc[0]
                r = home['R'].iloc[0]
                h = home['H'].iloc[0]
                hr = home['HR'].iloc[0]
                twb = home['2B'].iloc[0]
                thb = home['3B'].iloc[0]
                rbi = home['RBI'].iloc[0]
                sb = home['SB'].iloc[0]
                cs = home['CS'].iloc[0]
                bb = home['BB'].iloc[0]
                so = home['SO'].iloc[0]
                tb = home['TB'].iloc[0]
                gdp = home['GDP'].iloc[0]
                hbp = home['HBP'].iloc[0]
                sh = home['SH'].iloc[0]
                sf = home['SF'].iloc[0]
                ibb = home['IBB'].iloc[0]
                roe = home['ROE'].iloc[0]
                ob = home['1B'].iloc[0]

                d_home['Name'] = name
                d_home['G'] = g
                d_home['GS'] = gs
                d_home['PA'] = pa
                d_home['AB'] = ab
                d_home['R'] = r
                d_home['H'] = h
                d_home['HR'] = hr
                d_home['2B'] = twb
                d_home['3B'] = thb
                d_home['RBI'] = rbi
                d_home['SB'] = sb
                d_home['CS'] = cs
                d_home['BB'] = bb
                d_home['SO'] = so
                d_home['TB'] = tb
                d_home['GDP'] = gdp
                d_home['HBP'] = hbp
                d_home['SH'] = sh
                d_home['SF'] = sf
                d_home['IBB'] = ibb
                d_home['ROE'] = roe
                d_home['1B'] = ob

                g = away['G'].iloc[0]
                gs = away['GS'].iloc[0]
                pa = away['PA'].iloc[0]
                ab = away['AB'].iloc[0]
                r = away['R'].iloc[0]
                h = away['H'].iloc[0]
                hr = away['HR'].iloc[0]
                twb = away['2B'].iloc[0]
                thb = away['3B'].iloc[0]
                rbi = away['RBI'].iloc[0]
                sb = away['SB'].iloc[0]
                cs = away['CS'].iloc[0]
                bb = away['BB'].iloc[0]
                so = away['SO'].iloc[0]
                tb = away['TB'].iloc[0]
                gdp = away['GDP'].iloc[0]
                hbp = away['HBP'].iloc[0]
                sh = away['SH'].iloc[0]
                sf = away['SF'].iloc[0]
                ibb = away['IBB'].iloc[0]
                roe = away['ROE'].iloc[0]
                ob = away['1B'].iloc[0]

                d_away['Name'] = name
                d_away['G'] = g
                d_away['GS'] = gs
                d_away['PA'] = pa
                d_away['AB'] = ab
                d_away['R'] = r
                d_away['H'] = h
                d_away['HR'] = hr
                d_away['2B'] = twb
                d_away['3B'] = thb
                d_away['RBI'] = rbi
                d_away['SB'] = sb
                d_away['CS'] = cs
                d_away['BB'] = bb
                d_away['SO'] = so
                d_away['TB'] = tb
                d_away['GDP'] = gdp
                d_away['HBP'] = hbp
                d_away['SH'] = sh
                d_away['SF'] = sf
                d_away['IBB'] = ibb
                d_away['ROE'] = roe
                d_away['1B'] = ob

                home_tot.append(d_home)
                away_tot.append(d_away)

    # convert to dataframe objects
    home_tot = pd.DataFrame(home_tot)
    away_tot = pd.DataFrame(away_tot)

    # I want each players full career stats to be summed over
    # all their seasons with the specified team however rate
    # stats like BA which are a decimal wont sum nicely. I
    # just drop them and re-compute here from raw counts to
    # correctly weight by PA or AB

    c_home = home_tot.groupby(['Name']).sum()
    c_away = away_tot.groupby(['Name']).sum()

    # make sure no zerodivision error
    c_home = c_home[c_home['AB'] > 0]
    c_away = c_away[c_away['AB'] > 0]

    # recompute rate stats
    c_home['BA'] = c_home['H'] / c_home['AB']
    c_home['SLG'] = c_home['TB'] / c_home['AB']

    c_away['BA'] = c_away['H'] / c_away['AB']
    c_away['SLG'] = c_away['TB'] / c_away['AB']

    c_home['OBP'] = (c_home['H'] + c_home['BB'] + c_home['HBP']) / (
        c_home['AB'] + c_home['BB'] + c_home['HBP'] + c_home['SF'])
    c_away['OBP'] = (c_away['H'] + c_away['BB'] + c_away['HBP']) / (
        c_away['AB'] + c_away['BB'] + c_away['HBP'] + c_away['SF'])

    c_home['OPS'] = c_home['OBP'] + c_home['SLG']
    c_away['OPS'] = c_away['OBP'] + c_away['SLG']

    c_home['HR_rate'] = c_home['HR'] / c_home['AB']
    c_away['HR_rate'] = c_away['HR'] / c_away['AB']

    c_home['1B_rate'] = c_home['1B'] / c_home['PA']
    c_away['1B_rate'] = c_away['1B'] / c_away['PA']

    c_home['Split'] = 'Home'
    c_away['Split'] = 'Away'

    print('Done')
    return c_home, c_away


def find_split(home_stats: pd.DataFrame, away_stats: pd.DataFrame,
               stat: str = 'BA', min_PA: int = 0,
               min_AB: int = 0) -> pd.DataFrame:
    '''
    Takes the home and away dfs from home_away_splits as well as a
    stat and a minimum PA and/or AB threshold. Returns the difference
    in all ths stats at home vs away with negative being worse at
    home/better on the road and visa versa.
    '''

    # initialize output list of dicts to be cast to a df
    output = []

    # since i used groupby earlier, the indicies are now player names
    for name in home_stats.index:

        # pull out home and away rows
        home = home_stats.loc[name]
        away = away_stats.loc[name]

        # impliment AB and PA threshold
        if (home['PA'] >= min_PA
                and away['PA'] >= min_PA
                and home['AB'] >= min_AB
                and away['AB'] >= min_AB):

            output.append({'Name': name,
                           f'{stat}_diff': (home[stat] - away[stat])})

    return pd.DataFrame(output)


def main():

    home, away = home_away_splits(2008, 2025, team='Seattle')

    # user input
    stat1 = 'SLG'
    stat2 = 'OBP'
    stat3 = 'HR_rate'
    stat4 = '1B_rate'

    stats = [stat1, stat2, stat3, stat4]

    df1 = find_split(home, away, stat1, min_PA=320)
    df2 = find_split(home, away, stat2, min_PA=460)
    df3 = find_split(home, away, stat3, min_PA=170)
    df4 = find_split(home, away, stat4, min_PA=290)

    dfs = [df1, df2, df3, df4]

    fig, [[ax1, ax2], [ax3, ax4]] = plt.subplots(2, 2, figsize=(14, 10))

    axs = [ax1, ax2, ax3, ax4]

    for i in range(4):

        xs = list(dfs[i][stats[i] + '_diff'])
        axs[i].hist(xs, color='k', bins=15)

        # average marker
        axs[i].axvline(np.mean(xs), color='r', linestyle=':')

        # 0 lines
        axs[i].axvline(0.0, color='k', linestyle=':')

        axs[i].set_xlabel(f'{stats[i]}')
        axs[i].set_ylabel('Counts')

    fig.suptitle('Home and Away Splits')
    plt.savefig('home_away_splits.png', bbox_inches='tight')


if __name__ == '__main__':
    main()
