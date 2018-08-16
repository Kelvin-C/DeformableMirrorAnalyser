# |**********************************************************************;
# * Project           : MSci Project: PLAS-Smith-3
# *
# * Program name      : func_optimise.py
# *
# * Author            : Kelvin Chan
# *
# * Date created      : 07 Dec 2017
# *
# * Purpose           : Fits the intensity data.
# *
# * Revision History  : v1.0
# *
# |**********************************************************************;

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MultipleLocator
import matplotlib.animation as an
from matplotlib.widgets import Slider
from scipy import optimize
import scipy.fftpack as scfft


def optimise_mean(image_tiff, vertical_fringes=True):
    # OPEN .tif FILE
    imarray = np.array(image_tiff)

    no_of_rows, no_of_columns, rgb = imarray.shape

    I = []
    
    # CONVERTS TO (no_of_columns, no_of_rows, rgb) shape
    if vertical_fringes == True:
        imarrayT = imarray.transpose((1, 0, 2))
        # CHOOSE THE VERTICLE PIXELS TO AVERAGE
        indexes_to_average = range(no_of_rows)
        x = np.arange(0, no_of_columns, 1)
        for i in range(no_of_columns):
            imarray_to_average = list(map(lambda j: imarrayT[i][j], indexes_to_average))
            I.append(np.mean(imarray_to_average))
        
    else:
        imarrayT = imarray
        indexes_to_average = range(no_of_columns)
        #x = np.linspace(0, (no_of_rows-1)*100, no_of_rows)
        x = np.arange(0, no_of_rows, 1)
        for i in range(no_of_rows):
            imarray_to_average = list(map(lambda j: imarrayT[i][j], indexes_to_average))
            I.append(np.mean(imarray_to_average))

    return optimise(I,x)

def optimise_mode(image_tiff, vertical_fringes=True):
    # OPEN .tif FILE
    imarray = np.array(image_tiff)

    no_of_rows, no_of_columns, rgb = imarray.shape
    
    I = []

    # CONVERTS TO (no_of_columns, no_of_rows, rgb) shape
    if vertical_fringes == True:
        imarrayT = imarray.transpose((1, 0, 2))
        # CHOOSE THE VERTICLE PIXELS TO AVERAGE
        indexes_to_average = range(no_of_rows)
        x = np.arange(0, no_of_columns, 1)
        for i in range(no_of_columns):
            imarray_to_average = list(map(lambda j: imarrayT[i][j][1], indexes_to_average))
            I.append(hist_peak(imarray_to_average))
    else:
        imarrayT = imarray
        indexes_to_average = range(no_of_columns)
        x = np.arange(0, no_of_rows, 1)
        for i in range(no_of_rows):
            imarray_to_average = list(map(lambda j: imarrayT[i][j][1], indexes_to_average))
            I.append(hist_peak(imarray_to_average))
        
    return optimise(I,x)

def optimise(I, x):
    #PROPETIES OF THE WAVE
    offset = np.mean(I)
    amplitude = max(I)-min(I)

    # OPTIMISATION ALGORITHM REQUIRES AN INITIAL GUESS
    guess_k = np.pi/200
    guess_phase = -np.pi/4

    counter = 0
    k_val = guess_k
    phase_val = guess_phase
    while counter < 100:
        counter += 1

        # FUNCTIONS TO FIT
        optimize_func_k = lambda u: osc_func_k(u, x, amplitude, offset, k_val) - I
        u = optimize.leastsq(optimize_func_k, [phase_val])[0]
        phase_val = u[0]

        optimize_func_phase = lambda u: osc_func_phase(u, x, amplitude, offset, phase_val) - I
        u = optimize.leastsq(optimize_func_phase, [k_val])[0]
        k_val = u[0]

    u = [amplitude, k_val, phase_val, offset]
    # RETURNS THE OPTIMISED PARAMETERS IN THE FITTED FUNCTION
    return u, I, x

def fit(I, x):
    N = len(x)
    T = max(x) / float(N)

    F_I = scfft.fft(I)
    f1 = np.linspace(0.0, 1.0 / (2.0 * T), N / 2)

    g1_plot_val = 2.0 / N * np.abs(F_I[:N // 2])

    ind = np.where(g1_plot_val > 1)[0]

    temp = []
    for i in ind:
        if i != 0:
            temp.append(g1_plot_val[i])
    temp = np.array(temp)

    # OPTIMISATION ALGORITHM REQUIRES AN INITIAL GUESS
    guess_k = np.pi / 200.
    guess_amplitude = max(I)-min(I)
    guess_offset = np.mean(I) - guess_amplitude/2
    guess_phase = np.pi/4
    u = [guess_amplitude, guess_k, guess_phase, guess_offset]

    maxfreq =  f1[np.where(temp == max(temp))[0][0]]
    print(maxfreq)

    yy = u[0]*np.cos(maxfreq * 2*np.pi*x)**2 + u[-1] - u[0]/2

    plt.figure()
    plt.subplot(1, 2, 1)
    plt.plot(x, I)
    plt.plot(x,yy)

    plt.subplot(1, 2, 2)
    plt.plot(f1, 2.0 / N * np.abs(F_I[:N // 2]))
    plt.axis([0, 0.05, 0, 200])

    plt.show()
    return

def hist_peak(array, o=1, bins='auto'):
    n, bins = np.histogram(array, bins=bins)
    if o == 2:
        n, bins, patches = plt.hist(array, bins=bins)
    return bins[_max_value_index(n)]

def _max_value_index(array):
    if type(array) is list:
        array = np.array(array)
    loc = np.where(array == max(array))[0][0]
    return loc

def oscillate_func(u, x, A, offset):
    return A * (np.cos(u[0] * x + u[1])) ** 2 + offset - A/2

def osc_func_k(u, x, A, offset, k):
    return A * (np.cos(k * x + u[0])) ** 2 + offset - A / 2

def osc_func_phase(u, x, A, offset, phase):
    return A * (np.cos(u[0] * x + phase)) ** 2 + offset - A / 2

def oscillate_func_1(u, x):
    return u[0] * (np.cos(u[1] * x + u[2])) ** 2 + u[-1] - u[0]/2

def oscillate_func_2(u, x):
    return (np.cos(u[0] * x + u[1])) ** 2


def optimise_algorithm(image_tiff, vertical_fringes=False, mode_or_mean='mean'):
    
    if mode_or_mean == 'mode':
        wave_optimised_params, intensity, x = optimise_mode(image_tiff, vertical_fringes=vertical_fringes)
    else:
        wave_optimised_params, intensity, x = optimise_mean(image_tiff, vertical_fringes=vertical_fringes)

    amp_values = wave_optimised_params[0]
    k_values = wave_optimised_params[1]
    phase_values = wave_optimised_params[2]
    offset_values = wave_optimised_params[3]
    intensity_fit = oscillate_func_1(wave_optimised_params, x)

    
    return amp_values, k_values, phase_values, offset_values, intensity, intensity_fit, x