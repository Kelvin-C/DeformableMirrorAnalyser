# |**********************************************************************;
# * Project           : MSci Project: PLAS-Smith-3
# *
# * Program name      : plots.py
# *
# * Author            : Kelvin Chan
# *
# * Date created      : 15 JAN 2018
# *
# * Purpose           : Allows simpler modification of plots with error bars. Stores plots, errorbar plots, figures.
# *
# * Revision History  : v1.0
# *
# |**********************************************************************;

import matplotlib.pyplot as plt

class Plots():

    def __init__(self):
        self.fig = []
        self.plot = []
        self.errplot = []
        return

    def addfig(self, fig):
        """
        Add figure to the list of figures
        """
        self.fig.append(fig)

    def addplot(self, plot):
        """
        Add plot to the list of plots
        """
        self.plot.append(plot)

    def adderrorbar(self, errorbar):
        """
        Add the errorbar plot with list of error bars.
        """
        self.errplot.append(errorbar)

    def removeerrorbar(self, n):
        """
        Removes all errorbar plots stored in the class.
        """
        if type(n) != int:
            for errplot in self.errplot:
                errplot[0].remove()
                for line in errplot[1]:
                    line.remove()
                for line in errplot[2]:
                    line.remove()
            self.errplot = []
        else:
            errplot = self.errplot[n]
            errplot[0].remove()
            for line in errplot[1]:
                line.remove()
            for line in errplot[2]:
                line.remove()
            del self.errplot[n]
