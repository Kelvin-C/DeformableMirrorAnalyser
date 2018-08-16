circuit data collection v.1.0 - 06/06/2018



The files and folders in this directory are used for data collection from the Adafruit 16-Channel 12-bit PCA9685 PWM/Servo Driver
and Adafruit ADS1115 16-Bit ADC - 4 Channel with Programmable Gain.




Required modules:

All critical libraries are outlined in requirements.txt.
Please refer to https://stackoverflow.com/questions/7225900/how-to-install-packages-using-pip-according-to-the-requirements-txt-file-from-a to see how to install the packages using pip.



————————————————————————————————



Modules:
	actions.py
		
		* This module contains the main control subroutines for the PWM and ADC boards.

		
		Example of how to run:

		
		from actions import *

		
		pwm_sweep(filename="test_data_file", N=100, trials=3, g=1, ref=2.048)
		
		
	

		comparison_graphs.py
		
		* A series of functions which plot various graphs when the functions are called using data found in the data directories.
	
	


		gain_lookup.py
		
		* A lookup table for scaling the output values from the 16-bit ADC board.
		
		The ADC board outputs values from -32768 to +32,768, to convert this to a voltage, the value must be scaled according to the specified gain value of the ADC board.
	
	

		hardware_init.py
		
		* Hardware initialisation. This module is used in actions.py
	
	

		plotter.py
		
		* This module is imported in actions.py in order to plot the data collected.




Data directories:
	optoswitch_output_06_02
		
		* voltage over duty cycle data taken from the optoswitch with no smoother circuit taken on 6th Feb

	

		optoswitch_output_09_02
		
		* voltage over duty cycle data taken from the optoswitch with no smoother circuit taken on 9th Feb

	

		optoswitch_output_16_02
		
		* voltage over duty cycle data taken from the optoswitch with no smoother circuit taken on 16th Feb, with 10 trials and errors.
		
		The large error bar for the first data point is due to an earlier iteration of the data collection routine which did not reset the duty cycle to 0 before each trial.

	


		pwm_output_09_02
		
		* voltage over duty cycle data taken directly from the PWM board, no optoswitch, no smoother circuit. Linear as expected.

	

		switch_data_27_02_2018
		
		* Data taken from 8 separate optoswitches, s1-s8: PWM sweeps and time sweeps at 1%, 50% and 98% chosen to reflect deadzone, linear region and saturation zones of the PWM sweep.




————————————————————————————————



e-mail: alice.cao14@imperial.ac.uk

	kelvin.chan14@imperial.ac.uk