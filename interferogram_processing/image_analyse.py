# |**********************************************************************;
# * Project           : MSci Project: PLAS-Smith-3
# *
# * Program name      : image_analyse.py
# *
# * Author            : Kelvin Chan
# *
# * Date created      : 05 Dec 2017
# *
# * Purpose           : Analyse the images taken from Michelson interferometry
# *
# * Revision History  : v1.0
# *
# |**********************************************************************;

import func_optimise
import func_clean
import func_crop
import func_voltages
import plots

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MultipleLocator
import matplotlib.animation as an
from matplotlib.widgets import Slider
import pickle
from scipy.optimize import curve_fit

##################### INPUT ######################

#Location of the image files in format: "folder/base_name+number.file_ext"
#Example: images/file0.tif
folder = 'original'
base_name = 'image_'
file_ext = '.tif'

#How many images?
no_of_images = 91

#Image Dimensions
vert_pixel_size = 1024
hor_pixel_size = 1280

#Volage xlsx file location (ensure values are in column 0 with a heading on row 0).
voltage_file = 'Voltages.xlsx'

#Wavelength of the laser used for the Michelson interferometry.
wavelength = 543.e-3

#Number of Repeats/Sections (The images are cropped into several sections and are analysed to produce a distribution)
no_of_repeats = 6

#Vertical fringes? If False, horizontal fringes are assumed.
vertical_fringes = True

#Find the stroke at a specific voltage with extrapolation.
max_stroke_voltage = 150 #V

#Saves the data to a 'pickle' file to be used later.
picklefile = 'data1.p'

##############################################################

def makefile(filename):
    """
    Create a file if it doesn't already exist

    Params:
    filename = String of the file location.
    """
    with open(filename, 'w') as f:
        f.close()
    return

def linear_fit(x, y, yerr):
    """
    Fit a linear fit to the data points. Includes the stroke errors in the fit.
    """
    line_func = lambda V, m, c: m*V + c

    m0 = 0.016
    c0 = 0
    parameters, error = curve_fit(line_func, x, y, p0=[m0, c0], sigma=yerr, absolute_sigma=True, maxfev=200000)

    m, c = parameters
    y_fit = line_func(x, *parameters)
    return y_fit, m, c, error

def largest_intensity(intensity_values_fit):
    """
    Finds the largest intensity value of the mean_intensities. Used for the setting graph axes limits.

    Param:
    intensity_values_fit = The 3D array that includes the mean and sd of the intensities.
    """
    max_intensity = 0
    for i in range(len(intensity_values_fit)):
        temp_max = max(intensity_values_fit[i][0])
        if temp_max > max_intensity:
            max_intensity = temp_max
    return max_intensity

def smallest_intensity(intensity_values_fit):
    """
    Finds the smallest intensity value of the mean_intensities. Used for the setting graph axes limits.

    Param:
    intensity_values_fit = The 3D array that includes the mean and sd of the intensities.
    """
    min_intensity = largest_intensity(intensity_values_fit)
    for i in range(len(intensity_values_fit)):
        temp_min = min(intensity_values_fit[i][0])
        if temp_min < min_intensity:
            min_intensity = temp_min
    return min_intensity

def format_fn(tick_val, tick_pos):
    """
    Used in plotdata function to have y-axis ticks in 'pi' intervals.
    """
    if tick_val == np.pi:
        return "$\pi$"
    elif tick_val == -np.pi:
        return "$-\pi$"
    elif tick_val == 0:
        return "$0$"
    else:
        return "$%i\pi$" % (tick_val / np.pi)

def plotdata(no_of_images, fig, plot_list):
    """
    Plots the data of k-values, phase-values and original unedited phase values.

    Params:
    no_of_images = How many images were used?
    fig = plt.figure()
    plot_list = The class object used to store plots.
    """
    num_up = int(no_of_images / 2) + 1

    ax21 = fig.add_subplot(2, 3, 4)
    k_up = ax21.errorbar(voltages[:num_up], k_values[0][:num_up], yerr=k_values[1][:num_up], fmt='gx', label='Increasing voltage')
    k_down = ax21.errorbar(voltages[num_up:], k_values[0][num_up:], yerr=k_values[1][num_up:], fmt='kx', label='Decreasing voltage')
    ax21.set_title('Optimised wavenumbers with voltage')
    ax21.set_ylabel('$Wavenumber$ $(not$ $m^{-1})$', fontsize=18)
    ax21.set_xlabel('$Voltage$ $(V)$', fontsize=18)
    ax21.legend()

    ax22 = fig.add_subplot(2, 3, 5)
    ax22.yaxis.set_major_formatter(FuncFormatter(format_fn))
    ax22.yaxis.set_major_locator(MultipleLocator(base=np.pi))
    phase_up = ax22.errorbar(voltages[:num_up], phase_values[0][:num_up], yerr=phase_values[1][:num_up], fmt='gx', label='Increasing voltage')
    phase_down = ax22.errorbar(voltages[num_up:], phase_values[0][num_up:], yerr=phase_values[1][num_up:], fmt='kx', label='Decreasing voltage')
    ax22.set_title("Phases (solved)")
    ax22.set_ylabel('$Phase$', fontsize=18)
    ax22.set_xlabel('$Voltage$ $(V)$', fontsize=18)
    ax22.legend()

    ax23 = fig.add_subplot(2, 3, 6)
    orig_phase_up = ax23.errorbar(voltages[:num_up], original_phases[0][:num_up], yerr=original_phases[1][:num_up], fmt='gx', label='Increasing voltage')
    orig_phase_down = ax23.errorbar(voltages[num_up:], original_phases[0][num_up:], yerr=original_phases[1][num_up:], fmt='kx', label='Decreasing voltage')
    ax23.set_title('Original phases')
    ax23.set_ylabel('$Phase$', fontsize=18)
    ax23.set_xlabel('$Voltage$ $(V)$', fontsize=18)
    ax23.legend()

    errbar_list = [k_up, k_down, phase_up, phase_down, orig_phase_up, orig_phase_down]
    for errbar in errbar_list:
        plot_list.adderrorbar(errbar)
    return

def plot0():
    """
    Plots the intensity/interference pattern.
    """
    fig = plt.figure(figsize=(9, 6))
    ax00 = plt.subplot2grid((10, 1), (0, 0), rowspan=8)

    pattern00 = ax00.errorbar(x, intensity_values[0][0], yerr=intensity_values[0][1], fmt='g-', linewidth=1,
                              label='measurements')
    fitted_pattern00 = ax00.errorbar(x, intensity_values_fit[0][0], yerr=intensity_values_fit[0][1], fmt='b-',
                                     linewidth=1, label='fitted')
    title00 = ax00.set_title("$i$ = %i, $\lambda$ = %i, $stroke$ = %0.4f$\mu m$, $voltage$ = %0.2fV" % (0, fitted_cos_period[0][0], stroke_values[0][0], voltages[0]), fontsize=16)
    ax00.set_xlim(x[0], x[-1])
    ax00.set_ylim(smallest_intensity(intensity_values_fit), largest_intensity(intensity_values_fit))
    ax00.legend()
    ax00.tick_params(labelsize=16)
    ax00.set_ylabel('$Intensity$', fontsize=18)
    ax00.set_xlabel('$Distance$ $(Pixel)$', fontsize=18)
    ax00.legend(fontsize=18)

    axcolor = 'lightgoldenrodyellow'
    ax_slider = plt.axes([0.15, 0.1, 0.65, 0.03], facecolor=axcolor)
    slide = Slider(ax_slider, 'i', 0, no_of_images - 1, valinit=0, valfmt='%i')

    plot_list = plots.Plots()

    plot_list.adderrorbar(pattern00)
    plot_list.adderrorbar(fitted_pattern00)

    def update(val):
        """
        Allows the change of interference pattern with the slider.
        """
        val = int(val)
        plot_list.removeerrorbar(n=-1)
        plot_list.removeerrorbar(n=-1)
        pattern00 = ax00.errorbar(x, intensity_values[val][0], yerr=intensity_values[val][1], fmt='g-', linewidth=1,
                                  label='measurements')
        fitted_pattern00 = ax00.errorbar(x, intensity_values_fit[val][0], yerr=intensity_values_fit[val][1], fmt='b-',
                                         linewidth=1, label='fitted')
        plot_list.adderrorbar(pattern00)
        plot_list.adderrorbar(fitted_pattern00)
        title00.set_text(
            "$i$ = %i, $\lambda$ = %0.5f, $stroke$ = %0.4f$\mu m$, $voltage$ = %0.2fV" % (val, fitted_cos_period[0][val], stroke_values[0][val], voltages[val]))
        plt.draw()
        return

    slide.on_changed(update)
    return slide

def plot1():
    """
    Plots the graph of stroke against voltage.
    """
    fig = plt.figure(figsize=(9, 6))
    ax = fig.add_subplot(111)

    phase_down_fit_plot = ax.plot(voltages[num_up - 1:], phase_fit_down, 'k--', label='Decreasing voltage (fit)')
    phase_up_fit_plot = ax.plot(voltages[:num_up], phase_fit_up, 'g--', label='Increasing voltage (fit)')
    phase_down = ax.errorbar(voltages[num_up:], stroke_values[0][num_up:], yerr=stroke_values[1][num_up:], fmt='kx', ms=6,
                             label='Decreasing voltage (measured)')
    phase_up = ax.errorbar(voltages[:num_up], stroke_values[0][:num_up], yerr=stroke_values[1][:num_up], fmt='gx', ms=6,
                           label='Increasing voltage (measured)')

    ax.tick_params(labelsize=16)
    tick_spacing_x = 10
    tick_spacing_y = 5
    ax.xaxis.set_major_locator(MultipleLocator(tick_spacing_x))
    # ax.yaxis.set_major_locator(MultipleLocator(tick_spacing_y))
    ax.set_ylabel('$Stroke$ $(\hspace{0.1} \mu m)$', fontsize=18)
    ax.set_xlabel('$Voltage$ $(V)$', fontsize=18)
    ax.legend(fontsize=13)

###################### SCRIPT #######################
filenumbers = range(no_of_images)

#Assumes half of voltages taken are increasing and half are decreasing voltages
no_of_points_forward = (no_of_images + 1) // 2
no_of_points_backward = no_of_points_forward - 1

num_up = int(no_of_images / 2) + 1

#Read voltages from voltage file
voltages = np.array(func_voltages.get_voltages(voltage_file))
print(voltages)

#Checks if voltages correspond to the correct number of images.
if len(voltages) != no_of_images:
    raise ValueError('Incorrect number of images or incorrect values of voltages')

if vertical_fringes == False:
    max_space = hor_pixel_size
    x = np.arange(vert_pixel_size)
    xlen = vert_pixel_size
else:
    max_space = vert_pixel_size
    x = np.arange(hor_pixel_size)
    xlen = hor_pixel_size

crop_intervals = max_space/(no_of_repeats+1)
crop_spacing = np.arange(0, max_space, crop_intervals)

# LISTS OF PARAMETERS FROM FITTING
amp_values = np.zeros((no_of_images, no_of_repeats))
k_values = np.zeros((no_of_images, no_of_repeats))
phase_values = np.zeros((no_of_images, no_of_repeats))
offset_values = np.zeros((no_of_images, no_of_repeats))

intensity_values = np.zeros((no_of_images, no_of_repeats, xlen))
intensity_values_fit = np.zeros((no_of_images, no_of_repeats, xlen))

#LOOP ON EVERY IMAGE
for file_number in filenumbers:

    file_number_str = str(file_number)
    print(file_number_str)
    
    #OPEN .tif FILE
    filename = folder + '/' + base_name + file_number_str + file_ext

    #Process for each section
    for repeat_number in range(no_of_repeats):

        #Crop the images
        new_image = func_crop.crop_algorithm(filename, vertical_fringes=vertical_fringes, min_crop=crop_spacing[repeat_number], max_crop=crop_spacing[repeat_number+1], num=repeat_number)

        #Clean each section
        new_image = np.asarray(new_image.convert('L'))
        new_image = func_clean.clean_algorithm(new_image, x_sd=10, y_sd=10, A=1000)

        #Fit the data
        optimised_data = func_optimise.optimise_algorithm(new_image, vertical_fringes=vertical_fringes, mode_or_mean='mean')

        #Store fitted values
        amp_values[file_number, repeat_number] = optimised_data[0]
        k_values[file_number, repeat_number] = optimised_data[1]
        phase_values[file_number, repeat_number] = optimised_data[2]
        offset_values[file_number, repeat_number] = optimised_data[3]

        intensity_values[file_number, repeat_number] = optimised_data[4]
        intensity_values_fit[file_number, repeat_number] = optimised_data[5]

original_phases = np.array(phase_values)

#Convert phase offsets into total phase shift.
for u in range(1, no_of_images):
    for rep in range(no_of_repeats):
        diff = phase_values[u][rep] - phase_values[u-1][rep]
        diff_sign = np.sign(diff)
        while abs(diff) > np.pi/2:
            phase_values[u][rep] = phase_values[u][rep] - diff_sign*np.pi
            diff = abs(phase_values[u][rep] - phase_values[u - 1][rep])


def mean_std(array):
    """
    Calculate mean and standard deviations of each image.
    Returns a 2D (3D for intensities) array of mean and standard deviations of each image.
    """
    if array.ndim == 3:
        array = array.transpose(0, 2, 1)
        array = list(map(mean_std, array))
        return array
    array = [list(map(np.mean, array))] + [list(map(np.std, array))]
    return array

# Finds the mean and standard deviation of the repeats/cropped images.
amp_values = mean_std(amp_values)
k_values = mean_std(k_values)
phase_values = mean_std(phase_values)
offset_values = mean_std(offset_values)
original_phases = mean_std(original_phases)
intensity_values = mean_std(intensity_values)
intensity_values_fit = mean_std(intensity_values_fit)

fitted_cos_period = (2*np.pi)/np.array(k_values)
stroke_values = np.array(phase_values) * wavelength/(2*np.pi)

phase_fit_up, grad, const, error = linear_fit(x=voltages[:num_up], y=stroke_values[0][:num_up], yerr=stroke_values[1][:num_up])
phase_fit_down, temp1, temp2, err = linear_fit(x=voltages[num_up-1:], y=stroke_values[0][num_up-1:], yerr=stroke_values[1][num_up-1:])

m_err = error[0, 0]**0.5
c_err = error[1, 1]**0.5

stroke = lambda V: grad*V + const
stroke_err = lambda V, m_err, c_err: np.sqrt((m_err*V)**2 + c_err**2)
delta_stroke_err = lambda V1, V2, m_err, c_err: np.sqrt(stroke_err(V1, m_err, c_err)**2 + stroke_err(V2, m_err, c_err)**2)

print("INFORMATION OF INCREASING VOLTAGE FIT")
print("Gradient: %f +- %f" %(grad, m_err))
print("Stroke at 0V: %f +- %f" %(const, c_err))
print("Max Stroke = %f +- %f" %(stroke(max_stroke_voltage)-stroke(0), delta_stroke_err(max_stroke_voltage, 0, m_err, c_err)))

# Store all processed data into new pickle file
datafile = open(picklefile, 'wb')
pickle.dump([no_of_images, filenumbers, no_of_repeats, vertical_fringes,
             voltages, amp_values, k_values, phase_values, offset_values, original_phases, intensity_values, intensity_values_fit], datafile)
datafile.close()

# # PLOT THE INFORMATION INTO GRAPHS
# fig = plt.figure(num=1, figsize=(12, 8))
# ax00 = plt.subplot2grid((10, 1), (0, 0), rowspan=8)
#
# pattern00 = ax00.errorbar(x, intensity_values[0][0], yerr=intensity_values[0][1], fmt='g-', linewidth=1, label='measurements')
# fitted_pattern00 = ax00.errorbar(x, intensity_values_fit[0][0], yerr=intensity_values_fit[0][1], fmt='b-', linewidth=1, label='fitted')
# title00 = ax00.set_title(' ')
# ax00.set_xlim(x[0], x[-1])
# ax00.set_ylim(smallest_intensity(intensity_values), largest_intensity(intensity_values))
# ax00.legend()

# #Initiate the slider to transition between images.
# axcolor = 'lightgoldenrodyellow'
# ax_slider = plt.axes([0.15, 0.1, 0.65, 0.03], facecolor=axcolor)
# shte = Slider(ax_slider, 'i', 0, no_of_images-1, valinit=0, valfmt='%i')
#
# #Initiate an object to store all plots.
# plot_list = plots.Plots()
#
# plot_list.adderrorbar(pattern00)
# plot_list.adderrorbar(fitted_pattern00)
#
# def update(val):
#     """
#     Change intensity plots with the slider.
#     """
#     val = int(val)
#     plot_list.removeerrorbar(n=-1)
#     plot_list.removeerrorbar(n=-1)
#     pattern00 = ax00.errorbar(x, intensity_values[val][0], yerr=intensity_values[val][1], fmt='g-', linewidth=1,
#                               label='measurements')
#     fitted_pattern00 = ax00.errorbar(x, intensity_values_fit[val][0], yerr=intensity_values_fit[val][1], fmt='b-',
#                                      linewidth=1, label='fitted')
#     plot_list.adderrorbar(pattern00)
#     plot_list.adderrorbar(fitted_pattern00)
#     #title00.set_text("i = %i, k = %0.5f, phase = %0.4f, orig_phase = %0.4f" % (val, k_values[val], phase_values[val], original_phases[val]))
#     plt.draw()
#     return

slide = plot0()
plot1()
plt.show()
# shte.on_changed(update)
#
# plt.show()






















