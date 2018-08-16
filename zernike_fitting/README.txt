Summary:
These Python/MATLAB code allow data from the Zygo interformeter or Shack-Hartmann Wavefront Sensor to be analysed.
An accurate Zernike polynomial fit of the data can be done with these code. Particular polynomials, such as piston, tilt
and defocus can be ignored to obtain more useful information about the data. RMS values of the fit or surface flatness
can be calculated with the code.

Tested System:
- Windows 10 with 64 bit Python 3.6.4 and MATLAB 9.3.0.713579 (R2017b)

Required Python libraries:
- matplotlib
- pickle
- numpy
- csv

Required MATLAB packages:
- ZernikeCalc

Required Python files:
- shackhartmann.py
- read_xyz.py

Required MATLAB files:
- compare_Zdata.m
- fit_Zdata.m
- read_Zdata.m
- read_zernike.m
- writedata.m

Required non-Python files:
- .xyz file (Zygo data)
- .csv file (Shack-Hartmann Wavefront Sensor data)

HOW TO USE:
- If the data is from the Zygo interferometer, you can get the '.xyz' file from the machine. Use 'read_xyz.py'.
- If the data is from Shack-Hartmann Wavefront Sensor, you need the .csv file that contains the wavefront data.
- Edit the variables given under ##### INPUT #### to read the files correctly.
- Both Python codes will output a text file containing the X, Y, Z coordinates/data. These data will be read by MATLAB code.
- The matrix dimensions of the data are 'printed' in Python. This must be remembered for the MATLAB code, therefore it is best
	to open a Python IDE to run the code to see the printed display.
- Open 'fit_Zdata.m' in MATLAB and edit the variables given under %%%%%% INPUT %%%%%%. Run the code to output a text file containing
	the Zernike polynomials. Up to 3000 Zernike polynomials have been tested with this code. 
- Open 'compare_Zdata.m' in MATLAB and edit the variables given under %%%%%% INPUT %%%%%%. Run the code to calculate the
	the wanted RMS value and display the fitted data.

CONTACT DETAILS:
- kelvin.chan14@imperial.ac.uk
- alice.cao14@imperial.ac.uk