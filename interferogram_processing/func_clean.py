# |**********************************************************************;
# * Project           : MSci Project: PLAS-Smith-3
# *
# * Program name      : func_clean.py
# *
# * Author            : Kelvin Chan
# *
# * Date created      : 10 Dec 2017
# *
# * Purpose           : Cleans the fringes through Fast Fourier Transforms.
# *
# * Revision History  : v1.0
# *
# |**********************************************************************;

from PIL import Image
import numpy as np
import cv2

def _big(fft2, xlen, ylen, minI):
    """
    Parameters:
    fft2: A 2D array of the intensity values after the fourier transform.
    xlen: Number of pixels horizontally
    ylen: Number of pixels vertically
    minI: All intensities above this value are recorded

    Return:
    I: Intensity value that's kept
    loc: Index location of the intensity value in [i, j]
    """

    I = []
    loc = []
    for i in range(ylen):
        for j in range(xlen):
            if fft2[i][j] > minI:
                I.append(fft2[i][j])
                loc.append([i, j])
    return I, loc

def _OLD_make_2DGaussian(A, y_sd, x_sd, y0_i, x0_i, xlen, ylen):
    """
    "OLD Version"
    Parameters:
    A: The multiple of a normalised Gaussian
    y_sd: Standard deviation of vertical Gaussian
    x_sd: Standard deviation of horizontal Gaussian
    y0_i: The vertical index of the Gaussian centre
    x0_i: The horizontal index of the Gaussian centre
    xlen: Number of pixels horizontally
    ylen: Number of pixels vertically
    """

    #MAKES A LINEARLY INCREASING ARRAY WITH 0 AT y0_i, x0_i AND WITH SPACING OF 1
    x = np.arange(-x0_i, xlen-x0_i)
    y = np.arange(-y0_i, ylen-y0_i)

    #FUNCTION OF 1D GAUSSIAN
    gaussian = lambda A, sd, u: np.sqrt(A)*(1/(sd*np.sqrt(2*np.pi)))*np.exp(-0.5*(u/sd)**2)

    #MAKES 2D GAUSSIAN CENTRED AT y0_i, x0_i
    gaussian2D = np.zeros((len(y), len(x)))
    for i in range(len(x)):
        for j in range(len(y)):
            gaussian2D[j][i] = gaussian(A, y_sd, y[j])*gaussian(A, x_sd, x[i])
    return gaussian2D

def _make_2DGaussian(A, y_sd, x_sd, y0_i, x0_i, xlen, ylen):
    """
    "Improved version"
    Parameters:
    A: The multiple of a normalised Gaussian
    y_sd: Standard deviation of vertical Gaussian
    x_sd: Standard deviation of horizontal Gaussian
    y0_i: The vertical index of the Gaussian centre
    x0_i: The horizontal index of the Gaussian centre
    xlen: Number of pixels horizontally
    ylen: Number of pixels vertically
    """

    x = np.zeros(xlen)
    y = np.zeros(ylen)

    #MAKE THE 1D GAUSSIAN CURVES
    kernelx = cv2.getGaussianKernel(xlen, x_sd)
    kernely = cv2.getGaussianKernel(ylen, y_sd)

    #THIS IS USED TO SHIFT THE GAUSSIAN KERNAL
    check_x = xlen//2 - x0_i
    check_y = ylen//2 - y0_i

    #SHIFT THE x GAUSSIAN CURVE TO x0_i
    #SOME POINTS OF THE GAUSSIAN CURVE IS LOST FROM SHIFTING
    #THE LOST POINTS ARE REPLACED WITH ZEROS (THEY ARE FAR FROM PEAK)
    if check_x > 0:
        kernelx = kernelx[xlen//2 - x0_i:]
        kernelx_len = len(kernelx)
        x[:kernelx_len] = kernelx.T[0]
    elif check_x < 0:
        max_x_index = xlen-x0_i+xlen//2
        kernelx = kernelx[:max_x_index]
        kernelx_len = len(kernelx)
        x[-kernelx_len:] = kernelx.T[0]

    #SHIFT THE x GAUSSIAN CURVE TO y0_i
    #SOME POINTS OF THE GAUSSIAN CURVE IS LOST FROM SHIFTING
    #THE LOST POINTS ARE REPLACED WITH ZEROS (THEY ARE FAR FROM PEAK)
    if check_y > 0:
        kernely = kernely[ylen//2 - y0_i:]
        kernely_len = len(kernely)
        y[:kernely_len] = kernely.T[0]
    elif check_y < 0:
        max_y_index = ylen-y0_i+ylen//2
        kernely = kernely[:max_y_index]
        kernely_len = len(kernely)
        y[-kernely_len:] = kernely.T[0]

    #AMPLIFY THE GAUSSIAN CURVES
    x, y = A*x, A*y

    #CONVERT THE 1D GAUSSIAN CURVES INTO A 2D MASK
    x, y = np.array([list(x)]), np.array([list(y)])
    mask = x*y.T
    return mask

def _make_ellipse(A, y_rad, x_rad, y_i, x_i, xlen, ylen):
    """
    Parameters:
    A: The amplification of the mask
    y_rad: Max vertical distance from eclipse centre
    x_rad: Max horizontal distance from eclipse centre
    y_i: The vertical index of the eclipse centre
    x_i: The horizontal index of the eclipse centre
    xlen: Number of pixels horizontally
    ylen: Number of pixels vertically
    """

    #MAKES A LINEARLY INCREASING ARRAY WITH 0 AT y0_i, x0_i AND WITH SPACING OF 1
    x = np.arange(-x_i, xlen-x_i)
    y = np.arange(-y_i, ylen-y_i)

    #EQUATION FOR ECLIPSE
    ellipse_eq = lambda u, u0, u_rad, v, v0, v_rad: (u/u_rad)**2 + (v/v_rad)**2 - 1

    #CREATE THE ECLIPSE MASK CENTRED AT y_i, x_i. EVERYTHING INSIDE THE ECLIPSE GETS AMPLIFIED BY a
    ellipse = np.ones((len(y), len(x)))
    for i in range(xlen):
        for j in range(ylen):
            ellipse_val = ellipse_eq(x[i], x_i, x_rad, y[j], y_i, y_rad)
            if ellipse_val < 0:
                ellipse[j][i] = A
    return ellipse

def _applymask(mask_func, fft2, points_loc, xlen, ylen, x_sd, y_sd, A):
    """
    Parameters:
    mask_func: The mask function defined above
    fft2: A 2D array of the intensity values after the fourier transform.
    points_loc: The location where the highest intensity values are in fourier space.
    xlen: Number of pixels horizontally
    ylen: Number of pixels vertically
    """

    #ALGORITHM TO APPLY MASK TO AMPLIFY THE HIGHEST INTENSITY VALUES
    mask_list = []
    for y_i, x_i in points_loc:
        mask = mask_func(A, y_sd, x_sd, y_i, x_i, xlen, ylen)
        mask_list.append(mask)
        
    mask = sum(mask_list)
    newfft2 = mask*fft2

    #RETURNS A NEW 2D ARRAY IN FOURIER SPACE AND THE 2D ARRAY OF THE MASK
    return newfft2, mask

def _remove_multiple_masking(points_loc, max_rad=10):
    """
    Removes all high intensity points in the same cluster and leaves only 1 location per cluster
    """
    new_points_loc = []

    for i in range(len(points_loc)):
        temp_cluster = []
        save = True

        #FIND POINTS NEAR points_loc[i]
        for j in range(len(points_loc)):
            dist = np.sqrt((points_loc[i][0] - points_loc[j][0])**2 + (points_loc[i][1] - points_loc[j][1])**2)
            if dist < max_rad:
                temp_cluster.append(points_loc[j])

        #IF NO POINTS IN THE CLUSTER OF POINTS ARE SAVED
        #points_loc[i] WILL BE SAVED IN new_points_loc
        for loc in temp_cluster:
            if loc in new_points_loc:
                save = False
        if save == True:
            new_points_loc.append(points_loc[i])

    return new_points_loc

def clean_image(image, mask_func, x_sd, y_sd, A):
    #FFT THE IMAGE
    fft2 = np.fft.fft2(image)
    absfft2 = np.abs(fft2)
    
    #FIND THE LOCATIONS THAT HAVE HIGH INTENSITY IN FFT IMAGE
    ylen, xlen = absfft2.shape
    points, points_loc = _big(absfft2, xlen, ylen, 1e6) #points_loc = [[y_i, x_i], ....]
    points_loc = _remove_multiple_masking(points_loc)
    
    #APPLY MASK TO EVERY HIGH INTENSITY POINT ON FOURIER IMAGE
    newfft2, mask = _applymask(mask_func, fft2, points_loc, xlen, ylen, x_sd, y_sd, A)
    absnewfft2 = abs(newfft2)
    newimage = np.fft.ifft2(newfft2)
    absnewimage = abs(newimage)

    return fft2, absfft2, newfft2, absnewfft2, newimage, absnewimage, mask


def clean_algorithm(image, x_sd=10, y_sd=10, A=1000., num=1):
    """
    Algorithm to clean the fringe patterns.
    
    Paramters:
    image = 2D array of image
    """
    #DEFINE PROPERTIES FOR MASKING
    ylen, xlen = image.shape
    
    #DEFINE THE MASK FUNCTION
    mask_func = _make_2DGaussian
    #mask_func = _make_ellipse

    #APPLY MASK TO THE IMAGE TO CLEAN (CAN REPEATEDLY CLEAN THE IMAGE)
    fft2, absfft2, newfft2, absnewfft2, newimage, absnewimage, mask = clean_image(image, mask_func, x_sd, y_sd, A)

    #CREATE A NEW ARRAY OF THE CLEANED COLOURED IMAGE TO SAVE AS .tif FILE
    absnewimage = absnewimage/absnewimage.max()*255 
    absnewimage = absnewimage.astype(int)
    new_array = np.zeros((ylen,xlen,4), dtype='uint8')
    for i in range(ylen):
        for j in range(xlen):
            new_array[i][j] = [absnewimage[i][j],absnewimage[i][j],absnewimage[i][j],255]

    #CONVERT ARRAY INTO IMAGE AND SAVE IT.
    new_image = Image.fromarray(new_array, mode='RGBA') # float32
    #new_image.save('cropped/image_%i.tif' %num, "TIFF")
    
    return new_image