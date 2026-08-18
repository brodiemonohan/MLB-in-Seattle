'''
Brodie Monohan
CSE 163

This file tests the traded_player_performance function
using assert statments and data directly from the
Baseball Reference website.
'''

import traded_player_performance as tra
import team_build as tb
import travel_split_performance as tsp

home, away = tsp.home_away_splits(2025, 2025, team='Seattle')
df = tsp.find_split(home, away, 'OBP')
df = df[df['Name'] == 'J.P. Crawford']

print(df['OBP_diff'].iloc[0])

assert 0.011 > df['OBP_diff'].iloc[0] > 0.009

df = tra.find_traded_players(team='Seattle')

df_ken = df[df['Name'] == 'Ken Griffey Jr.']

assert df_ken['Teams'].iloc[0] == 'from Chicago,Cincinnati'
assert df_ken['Years'].iloc[0] == '2008 -> 2009'
assert df_ken['PA_Seattle'].iloc[0] == 454
assert df_ken['PA_other'].iloc[0] == 575
assert df_ken['AB_Seattle'].iloc[0] == 387
assert df_ken['AB_other'].iloc[0] == 490

# within 0.01
assert -0.03 >= df_ken['BA_diff'].iloc[0] >= -0.04
assert -0.01 >= df_ken['SLG_diff'].iloc[0] >= -0.02
assert -0.02 >= df_ken['OBP_diff'].iloc[0] >= -0.03

df = tb.rel_team_power(2008, 2025, 'Seattle')

df = df[df['Season'] == 2025]

assert 0.017 >= df['ISO'].iloc[0] >= 0.015
assert 0.018 >= df['SLG'].iloc[0] >= 0.016
assert 0.007 >= df['HR_rate'].iloc[0] >= 0.005

