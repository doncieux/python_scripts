#!/usr/bin/python

import numpy as np

from matplotlib import *
import matplotlib.pyplot as plt

params = {
    'axes.labelsize': 8,
    'text.fontsize': 8,
    'legend.fontsize': 10,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'text.usetex': False #,
#    'figure.figsize': [4.5, 4.5]
}
rcParams.update(params)


def plot_variants_with_variance(data,filename,title):
    """Plots the data corresponding to multiple variants with their variance. The arguments are the data, the list of variant names and a filename to save the figure. The data is a dictionary that associates to a variant name a dictionay that associates a list of variants values to each x value.   
    """

    fig=plt.figure()
    ax=fig.add_subplot(111)

    for variant in data.keys():
        print("Plotting data associated to variant: "+variant)
        #print(str(data[variant]))
        lx=data[variant].keys()
        lx.sort()
        median=[]
        perc_25=[]
        perc_75=[]

        for x in lx:
            median.append(np.median(data[variant][x]))
            perc_25.append(np.percentile(data[variant][x],25))
            perc_75.append(np.percentile(data[variant][x],75))

        # print ("Plotting values:")
        # print ("      lx="+str(lx))
        # print ("      perc_25="+str(perc_25))
        # print ("      perc_75="+str(perc_75))

        ax.fill_between(lx,perc_25,perc_75,alpha=0.25, linewidth=0)
        ax.plot(lx,median,linewidth=2, label=variant)
        ax.legend(loc='upper left')

    ax.set_title(title)
    fig.savefig(filename+".pdf")
    fig.savefig(filename+".svg")
