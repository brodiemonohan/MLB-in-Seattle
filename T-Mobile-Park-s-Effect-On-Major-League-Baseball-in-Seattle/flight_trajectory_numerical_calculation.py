import numpy as np
import matplotlib.pyplot as plt


def c_l_baseball(v: float, omega: float) -> float:
    '''
    Takes in an initial velocity (v, m/s) and angular velocity (omega, rad/s) for a baseball 
    and returns the lift coefficent (C_l) which is generated due to the magnus 
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
    (rho, kg/m^3), and the axis of rotation (axis, rad), and, in conjunction with the c_l_baseball function, returns the force
    due to the magnus effect.
    '''
    A = np.pi * (0.0364 ** 2) #cross-sectional area of an MLB baseball (Nathan 2007)
    return (1 / 2) * c_l_baseball(v, omega) * rho * A * (v ** 2)


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


def trajectory(v: float, omega: float, rho: float, angle: float, axis: float, step: float = 0.01) -> None:
    '''
    Takes advanced statistics exit velocity (v, m/s), spin rate (omega, rad/s), air density 
    (rho, kg/m^3), launch angle (angle, rad), spin vector (axis, rad), and a time step (step, s) 
    and produces a numerically calculated trajectory of an MLB baseball via plotting the 2D position
    of the ball in x-z space while z is positive.
    '''
    # inital values metric
    m = 0.145 # mass of MLB baseball (Nathan 2007) (kg)
    g = 9.81 # acceleration due to gravity (m/s/s)
    v_x = np.cos(angle) * v
    v_z = np.sin(angle) * v
    x = 0 # initial position at home plate
    z = 1 # initial height 1 meter above home plate

    # while z > 0:
    for i in range(100):
        
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

        # update for next time step calculation
        v = np.sqrt((v_x ** 2) + (v_z ** 2))
        angle = np.arctan(v_z / v_x)
        
        #plot
        plt.plot(x, z, color = 'k')
    plt.ylabel('Height (m)')
    plt.xlabel('Distance (m)')
    