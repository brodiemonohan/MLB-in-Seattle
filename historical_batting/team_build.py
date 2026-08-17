'''
Brodie Monohan
CSE 163

This file defines the team power function.
'''

from pybaseball import batting_stats_bref
import pandas as pd
from time import sleep


def team_power(start_year: int, end_year: int, team: str) -> pd.DataFrame:
    '''
    Takes a start year and end year between 2008 and 2025 as well as
    a team and returns team power metrics.
    '''
    output = []
    for season in range(start_year, end_year + 1):
        sleep(1)
        df = batting_stats_bref(season)
        team_df = df[df['Tm'] == team]

        pa = team_df['PA'].sum()
        hr = team_df['HR'].sum()
        singles = (team_df['H'].sum() -
                team_df['2B'].sum() -
                team_df['3B'].sum() - hr)
        total_bases = (singles + 2*team_df['2B'].sum()
                    + 3*team_df['3B'].sum() + 4*hr)

        slg = total_bases / team_df['AB'].sum()
        avg = team_df['H'].sum() / team_df['AB'].sum()
        iso = slg - avg
        hr_rate = hr / pa

        output.append({'Season': season,
                      'ISO': iso,
                      'SLG': slg,
                      'HR_rate': hr_rate})

        return(pd.DataFrame(output))


def league_power(start_year: int, end_year: int) -> pd.DataFrame:
    '''
    Takes a start year and end year between 2008 and 2025 as well as
    a team and returns league power metrics.
    '''
    output = []
    for season in range(start_year, end_year + 1):
        sleep(1)
        df = batting_stats_bref(season)

        pa = df['PA'].sum()
        hr = df['HR'].sum()
        singles = df['H'].sum() - df['2B'].sum() - df['3B'].sum() - hr
        total_bases = singles + 2*df['2B'].sum() + 3*df['3B'].sum() + 4*hr

        slg = total_bases / df['AB'].sum()
        avg = df['H'].sum() / df['AB'].sum()
        iso = slg - avg
        hr_rate = hr / pa

        output.append({'Season': season,
                      'ISO': iso,
                      'SLG': slg,
                      'HR_rate': hr_rate})

        return(pd.DataFrame(output))


def team_relative_power(start_year: int, end_year: int, team: str) -> pd.DataFrame:
    '''
    Takes a start year and end year between 2008 and 2025 as well as
    a team and returns team power metrics relative to league avg.
    '''
    team_df = team_power(start_year, end_year, team)
    league_df = league_power(start_year, end_year)

    output = pd.DataFrame()
    output['Season'] = league_df['Season']
    output['ISO'] = team_df['ISO'] - league_df['ISO']
    output['SLG'] = team_df['SLG'] - league_df['SLG']
    output['HR_rate'] = team_df['HR_rate'] - league_df['HR_rate']

    return output


def main():
    print(team_relative_power(2008, 2025, 'Seattle'))


if __name__ == '__main__':
    main()
