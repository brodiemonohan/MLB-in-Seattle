import numpy as np
import matplotlib.pyplot as plt


def c_l_baseball(v: float, omega: float) -> float:
    '''
    Takes in an initial velocity (v, m/s) and angular velocity (omega, rad/s) for a 
    baseball and returns the lift coefficent (C_l) which is generated due to the magnus 
    effect as parameterized by Sawicki, Hubbard, and Stronge (2003).
    '''
    R = 0.0364 #radius of MLB baseball (Nathan 2007)
    S = R * omega / v
    if S > 0.1:
        return 0.09 + (0.6 * S)
    else:
        return 1.5 * S


def f_m_baseball(v: float, omega: float, rho: float, axis: float = 0) -> float:
    '''
    Takes an initial velocity (v, m/s), an angular velocity (omega, rad/s), air density
    (rho, kg/m^3), and the axis of rotation (axis, rad), and, in conjunction with the 
    c_l_baseball function, returns the force due to the magnus effect.
    '''
    A = np.pi * (0.0364 ** 2) #cross-sectional area of an MLB baseball (Nathan 2007)
    return ((1 / 2) * c_l_baseball(v, omega) * rho * A * (v ** 2)) * np.cos(axis)


def c_d_baseball(v: float, omega: float) -> float:
    '''
    Takes in an initial velocity (v, m/s) and angular velocity (omega, rad/s) for a baseball 
    and returns the drag coefficent (C_d) which is generated due to quadratic drag.
    '''
    R = 0.0364 #radius of MLB baseball (Nathan 2007)
    S = R * omega / v
    C_d0 = 0.3008   # zero-spin baseline, ~Nathan/Kensrud batted-ball fits
    return C_d0 + 0.0292 * S


def f_d_baseball(v: float, omega: float, rho: float) -> float:
    '''
    Takes an initial velocity (v, m/s), an angular velocity (omega, rad/s), and air density
    (rho, kg/m^3), and, in conjunction with the c_d_baseball function, returns the force
    due to quadratic drag.
    '''
    A = np.pi * (0.0364 ** 2) #cross-sectional area of an MLB baseball (Nathan 2007)
    return (1 / 2) * c_d_baseball(v, omega) * rho * A * (v ** 2)


def trajectory(v: float, omega: float, rho: float, angle: float, axis: float = 0, 
                step: float = 0.01, label: str = None, color: str = 'k', marker: str = None,
                linestyle: str = None, g: float = 9.81, m: float = 0.145, x: float = 0,
                z: float = 1, show_distance: bool = False, label_density: bool = True, 
                savefig: bool = False) -> None:
    '''
    Takes required arguments exit velocity (v, m/s), spin rate (omega, rad/s), air density
    (rho, kg/m^3), launch angle (angle, rad), and spin vector (axis, rad), as well as default
    arguments time step (step, s), trajectory label, line color, step marker, line style,
    acceleration due to gravity (g), the mass of the ball (m) the initial position of the 
    ball (x), and the initial height of the ball (z). The function produces a numerically 
    calculated trajectory of an MLB baseball via plotting the 2D position of the ball in x-z 
    space while z is positive and returns the final x distance. The savefig function is 
    not called so that multiple instances of the trajectory function can be stacked in a 
    single graph to show parameter variation.
    '''
    
    # inital values
    v_x = np.cos(angle) * v
    v_z = np.sin(angle) * v

    # initialize x and z lists
    xs = [x]
    zs = [z]
    
    while z > 0:
        
        f_x = (-1 * (f_d_baseball(v, omega, rho) * np.cos(angle))
                - (f_m_baseball(v, omega, rho, axis)) * np.sin(angle))
        
        f_z = (-1 * (f_d_baseball(v, omega, rho) * np.sin(angle))
               + (f_m_baseball(v, omega, rho, axis) * np.cos(angle))
               - m * g)

        # update for this time step
        v_x += (f_x / m) * step
        v_z += (f_z / m) * step
        x += v_x * step
        z += v_z * step
        xs.append(x)
        zs.append(z)

        # update for next time step calculation
        v = np.sqrt((v_x ** 2) + (v_z ** 2))
        angle = np.arctan(v_z / v_x)

    # plotting
    if label_density and g == 9.81:
        plot_label = f'{label} ({rho} $\\rm kg/m^3$)'
    elif label_density:
        plot_label = f'{label} ({rho} $\\rm kg/m^3$, g = {g} $\\rm m/s^2$)'
    else:
        plot_label = label
        
    if show_distance:
        plt.axvline(xs[-1], color = color, linestyle = ':')
    
    if marker:
        plt.scatter(xs, zs, color = color, marker = marker)
        
    plt.plot(xs, zs, color = color, label = plot_label, linestyle = linestyle)
    plt.ylabel('Height (m)')
    plt.xlabel('Distance (m)')
    plt.legend()

    if savefig and label:
        plt.savefig(label + '_trajectory_plot.png', bbox_inches = 'tight')
    elif savefig:
        plt.savefig('trajectory_plot.png', bbox_inches = 'tight')

    # return final distance
    return xs[-1]
