# T-Mobile Park's Effect On Major League Baseball in Seattle

The three forces that determine the path of a baseball though the air are gravity, drag, and the Magnus force. This project simulates these forces on a batted baseball (given parameters like velocity and spin rate) for a given MLB stadium using a combination of lattitude, longitude, and elevation data scraped from Google Maps, as well as historical weather data scraped from the Open Mateo libraries. It is important to note that the Magnus forces is not strictly lift as it points perpendicular to the direction of motion and the spin axis, typically making a lift force only a component of the overall force and effect.

# Atmosphere Effects

## flight_trajectory_numerical_calculation.py

This file defines 4 helper functions that compute the drag and Magnus effect coefficents due to drag and the Magnus force, as well as the forces themselves based on the required input parameters. The 5th function combines these helper functions with the force due to gravity into a comprehensive function that numerically computes the flight path of the ball in the 2D x-z plane (keeing the same axis convention as StatCast) by computing the forces, the velocity, and position of the ball at time steps defined by the user.

## example.ipynb

This is an example notebook that shows how the flight_trajectory_numerical_calculation.py functions are meant to be used. The example uses are the calls that generated the graphics in the accompanying paper.

# Historical Batting

## traded_player_performance.py

This file will contain functions to pull batting data of players who were traded to or from a team in a given time-span to compare thier performaces on the given team to all other teams to check for trends.

## seattle_example.ipynb

This will be an example notebook that shows how the traded_player_performance.py functions are meant to be used. The example uses will be the calls that generate the graphics in the accompanying paper.

# Ancillary Data

## stadium_data.csv

This file contains extra useful data on MLB stadiums manually scraped from MLB.com and Google Maps. Elevation is rounded to the nearest meter. Data is up to date, scraped 2026. This is important for historical analysis considering the Athletics moved from Oakland in 2025 to Sacramento in 2026, and the Rays played in Tampa for the 2025 season due to huricane damage to Tropicana Field before returning in 2026.
