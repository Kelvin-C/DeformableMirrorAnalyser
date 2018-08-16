interferogram_processing v.1.0 - 06/06/2018

These Python scripts are used to analyse the interformetry fringes created with Michelson interferometers.
The fringes are cleaned through Fourier transformations and are fitted to obtain the stroke-voltage graph.
Each image is cropped and cleaned individually to obtain a standard deviation of the results.

———————————————————————————————————————

Tested System:
- Windows 10 with 64 bit Python 3.6.4

Required Python libraries:
- matplotlib
- numpy
- pickle
- PIL
- cv2
- openpyxl
- scipy

Required Python files:
- func_clean.py
- func_crop.py
- func_optimise.py
- func_voltage.py
- plots.py

Useful Python files:
- image_pickle.py

Required non-Python files:
- Interference pattern images (example given in 'original folder')
- Voltages spreadsheet (example given in 'voltages.xlsx', must follow example template.)

———————————————————————————————————————

HOW TO USE:
- Edit the variables given under ##### INPUT ####. 
- Voltages are assumed to be in numerical order, where the voltages ascend from a minimum value to a peak value
	and then back down to another minimum value. Equal number of ascending voltages as descending voltages are assumed.
	Therefore, there should be an odd number of voltages/images.
- A pickle file will be produced after running the code. This pickle file will store the useful data generated from
	the program. The pickle file can be used with 'image_pickle.py'.
- To use image_pickle.py, edit the variables under ###### INPUT #####.

———————————————————————————————————————

CONTACT DETAILS:
- kelvin.chan14@imperial.ac.uk
- alice.cao14@imperial.ac.uk



