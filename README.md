# T-Mobile Park's Effect On Major League Baseball in Seattle

The Seattle Mariners are the only Major League Baseball team to never make the World Series. Despite being near the middle of the pack in terms of payroll, Mariner teams since the early 2000s have been disappointing to say the least, with historically bad offenses in the 2010s. Since the team's move from their old stadium into what would become T-mobile Park (formerly Safeco Field), some analysts have noticed that batters seem to perform poorly in the stadium. Former sluggers who were traded to the Mariners would constantly under-perform with their new team, or so it seemed. Some analysts began to theorize there was some external factor causing batters to lose production when being traded to the Mariners. The most prominent theory is that the Seattle climate and the stadium itself that was causing hitters to under-perform. This theory is reinforced by the pitching statistics for Seattle which, since 2000, have been historically good. While a ''cursed" stadium is a romantic way to explain the Mariner's historic woes, there are also many other explanations. This project examines if hitting in Seattle is significantly 'harder' or if players are worse when playing in Seattle by looking at historical batting numbers and investigating the physical conditions in T-Mobile Park.

# Atmosphere Effects

The three forces that determine the path of a baseball though the air are gravity, drag, and the Magnus force. This folder simulates these forces on a batted baseball (given parameters like velocity and spin rate) for a given MLB stadium using a combination of lattitude and longitude data scraped from Google Maps, as well as historical weather data scraped from the Open Mateo libraries. It also compares simulated hits to real hit data from Baseball Sevant (built on StatCast).

## trajectory_calculation.py

This file defines 4 helper functions that compute the drag and Magnus effect coefficents due to drag and the Magnus force, as well as the forces themselves based on the required input parameters. The 5th function combines these helper functions with the force due to gravity into a comprehensive function that numerically computes the flight path of the ball in the 2D x-z plane (keeing the same axis convention as StatCast) by computing the forces, the velocity, and position of the ball at time steps defined by the user.

### c_l_baseball(v, omega)

Required inputs: v (float), omega (float)
Outpus: $C_l$

Takes in an initial velocity (v, m/s) and angular velocity (omega, rad/s) for a baseball and returns the lift coefficent ($C_l$) which is generated due to the magnus effect as parameterized by Sawicki, Hubbard, and Stronge (2003).

### f_m_baseball(v, omega, rho)

Required inputs: v (float), omega (float), rho (float)
Optional inputs: axis (float = 0)
Output: $F_m$

Takes an initial velocity (v, m/s), an angular velocity (omega, rad/s), air density (rho, kg/m^3), and the axis of rotation (axis, rad), and, in conjunction with the c_l_baseball function, returns the force due to the magnus effect. The axis is measured in the clockwise direction from the positive y axis (0 = pure back-spin, $\pi$ = pure top-spin)

### c_d_baseball(v, omega)

Required inputs: v (float), omega (float)
Output: $C_d$

Takes in an initial velocity (v, m/s) and angular velocity (omega, rad/s) for a baseball 
and returns the drag coefficent ($C_d$) which is generated due to quadratic drag.

### f_d_baseball(v, omega, rho)

Required inputs: v (float), omega (float), rho (float)
Output: $F_d$

Takes an initial velocity (v, m/s), an angular velocity (omega, rad/s), and air density
(rho, kg/m^3), and, in conjunction with the c_d_baseball function, returns the force
due to quadratic drag.

### trajectory(v, omega, rho, angle)

Required inputs: v (float), omega (float), rho (float), angle (float)
Optional inputs: axis (float = 0), step (float = 0.01), label (str = None), color (str = 'k'), marker (str = None), linestyle (str = None), g (float = 9.81), m (float = 0.145), x (float = 0), z (float = 1), show_distance (bool = False), label_density (bool = True), savefig (bool = False)
Outputs: distance (float)

Takes required arguments exit velocity (v, m/s), spin rate (omega, rad/s), air density (rho, kg/m^3), launch angle (angle, rad), and spin vector (axis, rad), as well as default arguments time step (step, s), trajectory label, line color, step marker, line style, acceleration due to gravity (g), the mass of the ball (m) the initial position of the ball (x), and the initial height of the ball (z). The function produces a numerically calculated trajectory of an MLB baseball via plotting the 2D position of the ball in x-z space while z is positive and returns the final x distance. The savefig function is not called so that multiple instances of the trajectory function can be stacked in a single graph to show parameter variation. An important note is that the spin axis is restricted to the y-axis where 0 rad defines pure backspin and $\pi$ rad is pure top spin.

## example.ipynb

This is an example notebook that shows how the flight_trajectory_numerical_calculation.py functions are meant to be used. The example uses are the calls that generated the graphics in the accompanying paper.

# Historical Batting

## traded_player_performance.py

This file will contain functions to pull batting data of players who were traded to or from a team in a given time-span to compare thier performaces on the given team to all other teams to check for trends.

## seattle_example.ipynb

This will be an example notebook that shows how the traded_player_performance.py functions are meant to be used. The example uses will be the calls that generate the graphics in the accompanying paper.

# Ancillary Data

## stadium_data.csv

This file contains extra useful data on MLB stadiums manually scraped from MLB.com and Google Maps. Elevation is rounded to the nearest meter. Data is up to date (2026). This is important for historical analysis considering the Athletics moved from Oakland in 2025 to Sacramento in 2026, and the Rays played in Tampa for the 2025 season due to huricane damage to Tropicana Field before returning in 2026.
