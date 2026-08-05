'''
Brodie Monohan
CSE 163

This file tests the traded_player_performance function
using assert statments and data directly from the
Baseball Reference website.
'''

import traded_player_performance as tra

df = tra.find_traded_players(team='Seattle')

df_ken = df[df['Name'] == 'Ken Griffey Jr.']
print(df_ken)

assert df_ken['Teams'].iloc[0] == 'from Chicago,Cincinnati'
assert df_ken['Years'].iloc[0] == '2008 -> 2009'
assert df_ken['PA_Seattle'].iloc[0] == 454
assert df_ken['PA_other'].iloc[0] == 575
assert df_ken['AB_Seattle'].iloc[0] == 387
assert df_ken['AB_other'].iloc[0] == 490

assert -0.03 >= df_ken['BA_diff'].iloc[0] >= -0.04
assert -0.01 >= df_ken['SLG_diff'].iloc[0] >= -0.02
assert -0.02 >= df_ken['OBP_diff'].iloc[0] >= -0.03
