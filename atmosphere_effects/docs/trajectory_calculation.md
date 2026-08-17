# trajectory calculation

`trajectory(v, omega, rho, angle)`

This file defines 4 helper functions that compute the drag and Magnus effect coefficents due to drag and the Magnus force, as well as the forces themselves based on the required input parameters. The 5th function combines these helper functions with the force due to gravity into a comprehensive function that numerically computes the flight path of the ball in the 2D x-z plane (keeping the same axis convention as StatCast) by computing the forces, the velocity, and position of the ball at time steps defined by the user. An important note is that the spin axis is restricted to the y-axis where 0 rad defines pure backspin and $\pi$ rad is pure top spin.

## Arguments

`v:` Float representing hit velocity in meters per second. A valid entry would be 45 (~ 100mph).

`omega:` Float representing the angular velocity of the ball in radians per second. A valid entry would be 150 (~ 1500rpm).

`rho:` float

`angle:` float

`axis:` Optional float = 0.

`step:` Optional float = 0.01.

`label:` Optional Str = None

color (str = 'k'), 
marker (str = None), 
linestyle (str = None), 
g (float = 9.81), 
m (float = 0.145), 
x (float = 0), 
z (float = 1), 
show_distance (bool = False), 
label_density (bool = True), 
savefig (bool = False)

## Example
```python
import trajectory_calculation as tra

# user input
v = 45  # m/s
omega = 150  # rad/s
axis = 0  # rad, pure backspin
angle = np.pi/6  # rad (45 deg)
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