# |**********************************************************************;
# * Project           : MSci Project: PLAS-Smith-3
# *
# * Program name      : func_crop.py
# *
# * Author            : Kelvin Chan
# *
# * Date created      : 05 Dec 2017
# *
# * Purpose           : Crops the images.
# *
# * Revision History  : v1.0
# *
# |**********************************************************************;

from PIL import Image
import numpy as np

def crop_algorithm(filename, vertical_fringes, min_crop=600, max_crop=700, num=1):
    if type(vertical_fringes) != bool:
        raise TypeError('vertical_fringes must be True or False')

    min_crop, max_crop = int(min_crop), int(max_crop)

    # print("min_crop = %f" %min_crop)
    # print("max_crop = %f" %max_crop)

    #OPEN .tif FILE
    image_tiff = Image.open(filename)
    
    imarray = np.array(image_tiff)
    no_of_rows, no_of_columns, rgba = imarray.shape

    if vertical_fringes == False:
        imarray = imarray.transpose((1, 0, 2))

    #CROP THE IMAGE AND SAVE THE CROPPED IMAGE
    new_imarray = imarray[min_crop:max_crop]

    if vertical_fringes == False:
        new_imarray = new_imarray.transpose((1, 0, 2))

    #print(new_imarray.shape)
    new_image = Image.fromarray(new_imarray, mode='RGBA') # float32
    return new_image