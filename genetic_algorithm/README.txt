genetic algorithm v.1.0 - 06/06/2018

These MATLAB and Python files are used to optimise focal spots with Genetic Algorithm (GA).
The MATLAB algorithm generates generations of duty cycles and is sent to the Raspberry Pi. The Raspberry Pi reads the duty cycles (with server.py) and sends the new square waves to the circuit.
The deformable mirror bends and the camera images the new intensity distribution. The intensity distribution of the focal spot is analysed by calculating the sum of the squares of the intensities. The sum of the squares is maximised with GA.

———————————————————————————————————————

Tested System:
- Windows 10 with MATLAB 9.3.0.713579 (R2017b)

Required MATLAB Packages:
- Global Optimisation Toolbox

Required MATLAB files:
- genetic_algorithm.m
- fitness_func.m
- take_img.m

Required Python files:
- server.py
- actions.py

Other required installations:
- ThorCam

———————————————————————————————————————

Variables to edit:
- From genetic_algorithm.m, you can edit the variables:
	'numberOfVariables', 'opts.PopulationSize', 'generations'
- The code assumes that all duty cycles are available (range from 0 to 100)
	The range can be changed by changing the lower and upper bound by editing the variables:
	'LB', 'UB', 'opts.InitialPopulationRange'
- From fitness_func.m, edit:
	t = tcpip('169.254.99.105', 30004, 'NetworkRole', 'client');
	The first argument is the IP address of the Raspberry Pi, and the 2nd argument is the PORT number, which is set
	by the Python code 'server.py' in the Raspberry Pi.
- From take_img.m, edit:
	'exposure', 'gain' and 'crop'

Experimental apparatus/structure:
- Laser should be reflected by the deformable mirror and focused by a lens.
- A camera, controlled by the computer running MATLAB, should image the focal spot.

To run:
- Ensure the Raspberry Pi is connected to the computer that is using MATLAB via Ethernet cable or WiFi.
- Ensure the camera is connected to the same computer and that its drivers are installed.
- Transfer 'server.py' to the Raspberry Pi. Edit the variables 'host' and 'port'. The 'host' is the IP address
	of the Raspberry Pi (can be found using ifconfig in terminal). 'port' can be any value.
- Ensure the IP address and the PORT number in MATLAB is the same as the ones set by the Raspberry Pi.
- Once the hardware are set up, run server.py on the Raspberry Pi. It should display the IP address and the port number.
- Now run, genetic_algorithm.m 

Possible fixes to errors:
- Changing the PORT number of Rasperry Pi
- Ensure the IP address and PORT number are correct
- Ensure the camera is NOT open anywhere else (i.e. must close ThorCam)

———————————————————————————————————————

CONTACT DETAILS:
- kelvin.chan14@imperial.ac.uk
- alice.cao14@imperial.ac.uk
