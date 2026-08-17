from pybaseball import batting_stats_bref
import pandas as pd
from time import sleep

def team_power(season: int, team: str = 'Seattle') -> dict:
    '''
    Takes a season and returns the ISO, SLG, HR,
    and HR rate team stats
    '''
    sleep(1)
    df = batting_stats_bref(season)
    team_df = df[df['Tm'] == team]

    pa = team_df['PA'].sum()
    hr = team_df['HR'].sum()
    singles = team_df['H'].sum() - team_df['2B'].sum() - team_df['3B'].sum() - hr
    total_bases = singles + 2*team_df['2B'].sum() + 3*team_df['3B'].sum() + 4*hr

    slg = total_bases / team_df['AB'].sum()
    avg = team_df['H'].sum() / team_df['AB'].sum()
    iso = slg - avg
    hr_rate = hr / pa

    return {'Season': season, 'ISO': round(iso, 3), 'SLG': round(slg, 3), 'HR_rate': round(hr_rate, 3)}


def league_power(season: int) -> dict:
    '''
    Takes a season and returns the ISO, SLG, HR,
    and HR rate team stats
    '''
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

    return {'Season': season, 'ISO': round(iso, 3), 'SLG': round(slg, 3), 'HR_rate': round(hr_rate, 3)}


def main():
    mariners = []
    league = []
    for season in range(2008, 2026):
        mariners.append(team_power(season))
        league.append(league_power(season))

    print(pd.DataFrame(mariners))
    print(pd.DataFrame(league))


if __name__ == '__main__':
    main()