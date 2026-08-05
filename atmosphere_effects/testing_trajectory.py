'''
Brodie Monohan
CSE 163

This file tests the trajectory function with Julio Rodrígez
real hit data directly from Stat Cast (via Baseball Savant).
'''

import trajectory_calculation as tra
import numpy as np
import matplotlib.pyplot as plt
from pybaseball import playerid_lookup, statcast_batter
import pybaseball

pybaseball.cache.enable()


def test_tajectory_helper(v: float, d: float, rho: float,
                          angle: float, z: float) -> str:
    '''
    Tests the trajectory function in trajectory_calculation.py by comparing
    to real hits in the MLB. Since spin rate and axis data are not publicly
    availible, I try to find the best fit by minimizing the % difference.
    '''

    # mph to m/s
    v_ms = v * 0.44704

    # feet to m
    d_actual_m = d * 0.3048

    # deg to rad
    a_r = angle * 0.01745329

    # in to m
    z_m = z * 0.0254

    step = 0.1  # s
    axis = 0

    ds_sim = {}

    for i in range(-100, 201, 10):
        d_sim = tra.trajectory(v_ms, i, rho, a_r, axis,
                               step, z=z_m, plot=False)
        ds_sim[d_sim] = [i]

    min_diff = 100

    # find lowest % difference
    for d in ds_sim:
        per_diff = (np.abs(d_actual_m - d) / ((d_actual_m + d) / 2)) * 100
        ds_sim[d].append(per_diff)
        if per_diff < min_diff:
            min_diff = per_diff
            key = d

    tra.trajectory(v_ms, ds_sim[key][0], rho, a_r,
                   axis, step, z=z_m, legend=False)

    return f'{ds_sim[key][1]} % diff with spin {ds_sim[key][0]} rad/s'


def test_trajectory(name_first: str, name_last: str, rho: float,
                    team: str, year: int, hit_type: str) -> None:
    '''
    Takes a player name (first and last), an air density, team, year and
    hit-type (e.g. home-run) and compares the trajectory function prediction
    for a range of angular velocities to the actual hit data.
    '''
    player = playerid_lookup(name_last, name_first)
    id = player['key_mlbam'].iloc[0]
    data = statcast_batter(str(year) + '-01-01', '2026-12-31', player_id=id)
    data = data[(data['events'] == hit_type) & (data['home_team'] == team)]

    date = data['game_date']
    v_mph = data['launch_speed']
    angle_deg = data['launch_angle']
    d_feet = data['hit_distance_sc']
    z = data['plate_z']

    for i in date.index:
        print(name_first, name_last, date[i],
              test_tajectory_helper(v_mph[i], d_feet[i],
                                    rho, angle_deg[i], z[i]))

    plt.title(f'Simulated {year} {name_first} {name_last} {hit_type}s')
    plt.xlim(0, 135)
    plt.ylim(0, 135)
    plt.savefig('trajectory_plot_test.png', bbox_inches='tight')


def main():

    # testing with real home-runs by Julio Rodríguez:

    name_first = 'Julio'
    name_last = 'Rodríguez'
    rho = 1.2  # kg/m^3
    team = 'SEA'
    year = 2026
    hit_type = 'home_run'

    test_trajectory(name_first, name_last, rho, team, year, hit_type)


if __name__ == '__main__':
    main()
