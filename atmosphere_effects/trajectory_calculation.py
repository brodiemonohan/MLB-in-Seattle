'''
Brodie Monohan
CSE 163

This file defines the trajectory calculator function and its four
helper functions. It computes and plots the trajecotry
of a baseball in a given environment.
'''

# import dependencies
import numpy as np
import matplotlib.pyplot as plt
import air_densities as ad
import pandas as pd


def c_l_baseball(v: float, omega: float) -> float:
    '''
    Takes in an initial velocity (v, m/s) and angular velocity (omega, rad/s)
    for a baseball and returns the lift coefficent (C_l) which is generated
    due to the magnus effect as parameterized by Sawicki, Hubbard, and
    Stronge (2003).
    '''
    R = 0.0364  # radius of an MLB baseball (Nathan 2007)
    S = R * omega / v
    if S > 0.1:
        return 0.09 + (0.6 * S)
    else:
        return 1.5 * S


def f_m_baseball(v: float, omega: float, rho: float, axis: float = 0) -> float:
    '''
    Takes an initial velocity (v, m/s), an angular velocity (omega, rad/s),
    air density (rho, kg/m^3), and the axis of rotation (axis, rad), and, in
    conjunction with the c_l_baseball function, returns the force due to the
    magnus effect. The axis is measured in the clockwise direction from the
    positive y axis (0 = pure back-spin, pi = pure top-spin)
    '''
    R = 0.0364  # radius of an MLB baseball (Nathan 2007)
    A = np.pi * (R ** 2)
    return (((1 / 2) * c_l_baseball(v, omega)
             * rho * A * (v ** 2)) * np.cos(axis))


def c_d_baseball(v: float, omega: float) -> float:
    '''
    Takes in an initial velocity (v, m/s) and angular velocity (omega, rad/s)
    for a baseball and returns the drag coefficent (C_d) which is generated due
    to quadratic drag.
    '''
    R = 0.0364  # radius of an MLB baseball (Nathan 2007)
    S = R * omega / v
    C_d0 = 0.3008   # zero-spin baseline, Nathan/Kensrud batted-ball fits
    return C_d0 + 0.0292 * S


def f_d_baseball(v: float, omega: float, rho: float) -> float:
    '''
    Takes an initial velocity (v, m/s), an angular velocity (omega, rad/s), and
    air density (rho, kg/m^3), and, in conjunction with the c_d_baseball
    function, returns the force due to quadratic drag.
    '''
    R = 0.0364  # radius of an MLB baseball (Nathan 2007)
    A = np.pi * (R ** 2)
    return (1 / 2) * c_d_baseball(v, omega) * rho * A * (v ** 2)


def trajectory(v: float, omega: float, rho: float, angle: float,
               axis: float = 0, step: float = 0.01, label: str = None,
               color: str = None, marker: str = None, linestyle: str = None,
               g: float = 9.81, m: float = 0.145, x: float = 0, z: float = 1,
               show_distance: bool = False, label_density: bool = True,
               savefig: bool = False, plot: bool = True, lw: int = 1.5,
               legend: bool = True, zorder: int = 0, alpha: int = 1) -> float:
    '''
    Takes required arguments exit velocity (v, m/s), spin rate (omega, rad/s),
    air density (rho, kg/m^3), launch angle (angle, rad), and spin vector
    (axis, rad), as well as default arguments time step (step, s), trajectory
    label, line color, step marker, linestyle, acceleration due to gravity (g),
    the mass of the ball (m) the initial position of the ball (x), and the
    initial height of the ball (z). The function produces a numerically
    calculated trajectory of an MLB baseball via plotting the 2D position of
    the ball in x-z space while z is positive and returns the final x distance.
    The savefig function is not called so that multiple instances of the
    trajectory function can be stacked in a single graph to show parameter
    variation. An important note is that the spin axis is restricted to the
    y-axis where 0 rad defines pure backspin and pi rad is pure top spin.
    '''
    R = 0.0364  # radius of an MLB baseball (Nathan 2007)
    k = 0.1  # torque parameter Nathan 2008b

    # inital values
    v_x = np.cos(angle) * v
    v_z = np.sin(angle) * v

    # initialize x and z lists
    xs = [x]
    zs = [z]

    while z > 0:

        # isolate and sum the x components of the forces using trigonometry
        f_x = (-1 * (f_d_baseball(v, omega, rho) * np.cos(angle))
               - (f_m_baseball(v, omega, rho, axis)) * np.sin(angle))

        # isolate and sum the z components of the forces using trigonometry
        # z will include all of gravity (m * g)
        f_z = (-1 * (f_d_baseball(v, omega, rho) * np.sin(angle))
               + (f_m_baseball(v, omega, rho, axis) * np.cos(angle))
               - m * g)

        # update for this time step
        # velocities
        v_x += (f_x / m) * step
        v_z += (f_z / m) * step

        # positions
        x += v_x * step
        z += v_z * step
        xs.append(x)
        zs.append(z)

        # update for next time step calculation
        v = np.sqrt((v_x ** 2) + (v_z ** 2))
        angle = np.arctan(v_z / v_x)

    # plotting
    if label_density and g == 9.81 and label is not None:
        plot_label = f'{label} ({rho} $\\rm kg/m^3$)'
    elif label_density and label is not None:
        plot_label = f'{label} ({rho} $\\rm kg/m^3$, g = {g} $\\rm m/s^2$)'
    else:
        plot_label = None

    if show_distance:
        plt.axvline(xs[-1], color=color, linestyle=':')

    if marker is not None:
        plt.scatter(xs, zs, color=color, marker=marker)

    if plot:
        plt.plot(xs, zs, color=color, label=plot_label, linestyle=linestyle,
                 lw=lw, zorder=zorder, alpha=alpha)
        plt.ylabel('Height (m)')
        plt.xlabel('Distance (m)')
        if legend:
            plt.legend()

    if savefig and label:
        plt.savefig(label + '_trajectory_plot.png', bbox_inches='tight')
    elif savefig:
        plt.savefig('trajectory_plot.png', bbox_inches='tight')

    # return final distance
    return xs[-1]


def main():

    print('Running')
    print('...')

    df = pd.read_csv('../ancillary_data/stadium_data.csv')
    lons = df['longitude']
    lats = df['latitude']
    stadiums = df['stadium']
    ids = df['venue_id']

    output = []

    for lon, lat, stadium, id in zip(lons, lats, stadiums, ids):
        d = {}
        T = ad.average_temp(lon, lat, venue_id=id)
        e = ad.elevation(lon, lat)
        rho = ad.density(T, e, 0.0289647)
        d['stadium'] = stadium
        d['rho'] = rho
        output.append(d)

    df2 = pd.DataFrame(output)

    mark = ['T-Mobile Park', 'Coors Field', 'Oracle Park']

    # user input
    v = 45  # m/s
    omega = 150  # rad/s
    axis = 0  # rad, pure backspin
    angle = np.pi/6  # rad (45 deg)
    step = 0.05  # s

    plt.figure(figsize=(14, 7))

    for i in df2.index:
        row = df2.loc[i]
        color = 'k'
        if row['stadium'] in mark:
            label = row['stadium']
            color = None
            zorder = 5
            alpha = 1
        else:
            label = '_'
            zorder = 0
            alpha = 0.5
        if row['rho'] != np.NaN:
            trajectory(v, omega, row['rho'], angle, axis, step, color=color,
                       label=label, linestyle='-', savefig=False, legend=False,
                       zorder=zorder, alpha=alpha, lw=2)
    plt.title('Baseball Trajectory in Different Stadiums')
    plt.xlim(128, 140)
    plt.ylim(0, 6)
    plt.legend()
    plt.savefig('full_trajectory_plot.png', bbox_inches='tight')

    print('Done')


if __name__ == '__main__':
    main()
