# trajectory calculation

`trajectory(v, omega, rho, angle)`

This file defines 4 helper functions that compute the drag and Magnus effect coefficents due to drag and the Magnus force, as well as the forces themselves based on the required input parameters. The 5th function combines these helper functions with the force due to gravity into a comprehensive function that numerically computes the flight path of the ball in the 2D x-z plane (keeping the same axis convention as StatCast) by computing the forces, the velocity, and position of the ball at time steps defined by the user. An important note is that the spin axis is restricted to the y-axis where 0 rad defines pure backspin and $\pi$ rad is pure top spin.

## Arguments

`v:` Float representing hit velocity in meters per second. A valid entry would be 45 (~ 100mph).

`omega:` Float representing the angular velocity of the ball in radians per second. A valid entry would be 150 (~ 1500rpm).

`rho:` Float representing the air mass density in the stadium (kg/m^3). Perhaps use the air_densities.py file to calculate this value.

`angle:` Float representing the launch angle in radians measured from parallel with the ground.

`axis:` Optional float representing the spin axis in radians where 0 is pure backspin and pi is pure top spin. Defaults to 0.

`step:` Optional float representing the time step in Euler's method in seconds. Defaults to 0.01.

`label:` Optional string which will label the trajectory in the legend if called.

`color:` Optional string to color the trajectory in the plot. Defaults to black.

`marker:` Optional string which will mark the location of the ball at each timestep. A valid entry would be '+' or 'o'. Defaults to none.

`linestyle:` Optional string which changes the style of the line that traces the trajectory. A valid entry would be '--' or '-.'. Defaults to '-'.

`g:` Optional float which represents the acceleration due to gravity. Defaults to earth at sea level: 9.81 m/s^2.

`m:` Optional float which represents the mass of the ball in kg. Defaults to MLB baseball mass: 0.145 kg.

`x:` Optional float representing the initial x position of the ball when hit in meters. Defaults to home plate: 0 m.

`z:` Optional float representing the initial z position of the ball when hit in meters. Defaults to one meter above home plate: 1 m.

`show_distance:` Optional boolean which can toggle on a line which marks the final distance of the ball when reaching z = 0. Defaults to False.

`label_density:` Optional boolean which can toggle off labeling the air density in the legend for each trajectory. Defaults to True.

`savefig:` Optional boolean which can toggle on saving the figure. Defaults to False.

## Example
```python
import trajectory_calculation as tra

# user input
v = 45  # m/s
omega = 150  # rad/s
axis = 0  # rad, pure backspin
angle = np.pi/6  # rad (30 deg)
step = 0.05  # s
rho = 1.20. # kg/m^3

tra.trajectory(v, omega, rho, angle, axis, step, 
            color='k', label='Seattle', linestyle='-', 
            savefig=False, legend=True,
            zorder=5, alpha=0.8, lw=2, marker='+')

plt.title('Baseball Trajectory in Different Stadiums')
plt.xlim(0, 140)
plt.ylim(0, 140)
plt.savefig('full_trajectory_plot.png', bbox_inches='tight')
```
