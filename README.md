# TRAILS
According to state-of-the-art research, mobile network simulation is preferred over real testbeds, especially to evaluate communication protocols used in OpNet or MANET. The main reason behind it is the difficulty of performing experiments in real scenarios. However, in a simulation, a mobility model is required to define users' mobility patterns. Trace-based models can be used for this purpose, but they are difficult to obtain, and they are not flexible or scalable. Another option is TRAILS. TRAILS mimics the spatial dependency, geographic restrictions, and temporal dependency from real scenarios. Additionally, with TRAILS, it is possible to scale the number of mobile users and simulation time.

We observed that TRAILS simulations requires less computation time than a simulation with real traces and that a TRAILS graph consumes less memory than traces.

In this repository, we share the algorithms used by TRAILS to generate mobility graphs from real scenarios and simulate human mobility.

## Requirements
- Python3
- Scipy
- Omnet++ 5.4.1
- INET 4.0.0

## Installation Steps
- Copy the content of the Simulator folder from the project with your INET framework.
- Copy the Generator folder in your preferred local directory.

To learn how to use TRAILS you can check our [wiki](https://github.com/ComNets-Bremen/TRAILS---OMNeT-Implementation/wiki).
