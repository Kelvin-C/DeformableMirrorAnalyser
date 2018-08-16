# |**********************************************************************;
# * Project           : MSci Project: PLAS-Smith-3
# *
# * Program name      : plotter.py
# *
# * Author            : Alice Cao
# *
# * Date created      : 4 Feb 2018
# *
# * Purpose           : Helper function for plotting results.
# *                     Can plot x,y data or
# *                     x, y, yerr data
# *
# * Revision History  : v1.0
# *
# |**********************************************************************;

import matplotlib.pyplot as plt
import numpy as np

class Plotter:
    """ Plotter class, initialise with a file.
    Data in the file must have x column, y column with optional third yerror column.
    First line of file is not read, so column titles can be used.
    Data entries must be separated by a tab ("\t").
    """
    def __init__(self, filename=""):
        self.__filename = filename
        
    def sort(self):
        """ Convert .txt file into data arrays.
        """
        with open(self.__filename, "r") as file:
            
            data = file.readlines()
            
            x_list = []
            y_list = []
            yerr_list = []
            
            for line in range(1, len(data)) :
                entries = data[line].split("\t")

                x_list.append(float(entries[0]))
                y_list.append(float(entries[1]))

                if len(entries) == 2:
                    None
                elif len(entries) == 3:
                    yerr_list.append(float(entries[2]))
            
            file.close()
            return x_list, y_list, yerr_list
        
        
    def x(self):
        xs = np.array(self.sort()[0])
        return xs
    
    def y(self):
        ys = np.array(self.sort()[1])
        return ys
    
    def err(self):
        errs= np.array(self.sort()[2])
        return errs

# plot with x, y data, no error bars            
    def show_plot(self, title="", x_axis="", y_axis=""):
        plt.plot(self.x(),self.y(), "bo-")
        plt.title(title)
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)
        plt.show()

# plot with y error bars        
    def stat_plot(self, title="", x_axis="", y_axis=""):
        if self.err().size == 0:
            raise Exception("No y-error data available.")
        else:
            plt.errorbar(self.x(),self.y(), yerr=self.err(), fmt='go-', lw=2.5)
            plt.title(title)
            plt.xlabel(x_axis)
            plt.ylabel(y_axis)
            plt.show()        
            
