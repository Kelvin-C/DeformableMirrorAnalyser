## Developing Deformable Mirrors for High-Powered Ultrashort Pulses
The project's main objective was to design and engineer low-cost deformable mirrors (DMs) to be used in high-powered ultrashort laser pulses.
The DMs are controlled by a Raspberry Pi. Measurements were taken to understand the efficiency and effectiveness of the DM.

## The directories
### circuit_data
This script is written for the Raspberry Pi to measure the effectiveness of the smoother circuit. It can measure the voltage output of the smoother circuit with duty cycle/time.

### dmUI
Software with simple UI that allows the control of the piezoelectric actuators. Further development will allow continuous analysis of Michelson interference patterns.

### electronics
An LTSpice model of the circuit used for the project. Model analysis is allowed through LTSpice.

### genetic_algorithm
Uses Python and MATLAB to optimise focal spot reflections with a deformable mirror. Requires the use of a Raspberry Pi and an external computer that can run MATLAB and connect to a camera to capture the reflected image.

### interferogram_processing
This analyses Michelson interferograms made with deformable mirrors to analyse the stroke of their actuators. It can directly convert fringe pattern images into stroke-voltage graph.

### zernike_fitting
This fits a set of surface/wavefront data with zernike polynomials to allow further analysis. It is very accurate as a fit with several thousands of polynomials is possible.