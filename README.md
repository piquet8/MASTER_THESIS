# MASTER_THESIS
## trace_genarator.py
Algorithm used to filter the data extracted from the simulations log file, and convert them into Boolean string traces. Each Boolean string consists of 3 parameters: 
- the battery of the robot (3 boolean values) 
- the position of the robot (8 boolean values) 
- the grasping (1 boolean value)

If the map used during the simulation is changed, it is necessary to set the new parameters within the code that correspond to the extremes of the map (a0,a1,b0,b1). 
For the RAL2022-experiments simulation the parameters are:
- a0 = -15.5
- a1 = 6.5
- b0 = -10.8
- b1 = 16.8

For the tour-guide-robot simulation, the parameters are:
- a0 = -3.4
- a1 = 64
- b0 = -19.2
- b1 = 16.9

## Simulations
Simulations used during testing can be found here:

[RAL2022-experiments](https://github.com/SCOPE-ROBMOSYS/RAL2022-experiments) 2D simulation using the CRIS zero floor plan as a map 

[tour-guide-robot](https://github.com/hsp-iit/tour-guide-robot) 3D simulation, uses gazebo and rviz as graphic representers, uses the floor plan of the Turin museum as a map 
