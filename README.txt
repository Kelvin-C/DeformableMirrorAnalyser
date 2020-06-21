———————————————————————————————————————

MSci Project 2017-18 - Developing Deformable Mirrors for High-Powered Ultrashort Pulses

———————————————————————————————————————

The project's main objective was to design and engineer low-cost deformable mirrors (DMs) to be used in high-powered ultrashort laser pulses.
The DMs are controlled by a Raspberry Pi. Measurements were taken to understand the efficiency and effectiveness of the DM.

———————————————————————————————————————

The folders:

	- circuit_data
		- Script written for the Raspberry Pi to measure the effectiveness of the smoother circuit
		- Can measure the voltage output of the smoother circuit with duty cycle/time.

	- dmUI
		- A software with simple UI that allows the control of the piezoelectric actuators.
		- Further development will allow continuous analysis of Michelson interference patterns.
	
	- electronics
		- An LTSpice model of the circuit used for the project. Model analysis allowed through LTSpice.

	- genetic_algorithm
		- Uses Python and MATLAB to optimise focal spot reflections with a deformable mirror.
		- Requires the use of a Raspberry Pi and an external computer that can run MATLAB and connect to a camera capturing the reflected image.

	- interferogram_processing
		- Analyse Michelson interferograms made with deformable mirrors to analyse the stroke of their actuators.
		- Can directly convert fringe pattern images into stroke-voltage graph.

	- zernike_fitting
		- Fits a set of surface/wavefront data with zernike polynomials to allow further analysis.
		- Is very accurate as a fit with several thousands of polynomials is possible.

———————————————————————————————————————

Contact Details:
	
	- kelvin.chan14@alumni.imperial.ac.uk
	- alice.cao14@imperial.ac.uk
