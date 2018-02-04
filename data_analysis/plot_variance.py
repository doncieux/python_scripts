#!/usr/bin/python

import numpy as np

#import matplotlib
from matplotlib import *
use('Agg')
import matplotlib.pyplot as plt
from itertools import cycle

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


def plot_variants_with_variance(data,filename,title,axis=[],names={}):
    """Plots the data corresponding to multiple variants with their variance. The arguments are the data, the list of variant names and a filename to save the figure. The data is a dictionary that associates to a variant name a dictionay that associates a list of variants values to each x value.   
    """


    color=['b','g','r','c','m','y','k']
    ls=['-','--','-.',':']
    marker=['+','*','.',',','o','v','^','<','>']

    styles=[]

    for l in ls:
        for c in color:
            styles.append(c+l)
            

    fig=plt.figure()
    ax=fig.add_subplot(111)

    if (len(axis)==4):
        ax.axis(axis)


    num_style=0

    datakeys = data.keys()
    datakeys.sort()

    for variant in datakeys:
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

        mylabel = variant if variant not in names.keys() else names[variant]

        ax.fill_between(lx,perc_25,perc_75,alpha=0.25, linewidth=0)
        ax.plot(lx,median,styles[num_style], label=mylabel)
        num_style=num_style+1

    ax.set_xlabel("generation")
    ax.set_ylabel("max fitness")
    ax.legend(loc='lower right', bbox_to_anchor=(1., 0.),
              fancybox=True, shadow=True, ncol=1)
#    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1),
#              fancybox=True, shadow=True, ncol=1)
#    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
#              fancybox=True, shadow=True, ncol=1)

#    ax.set_title(title)
    fig.savefig(filename+".pdf",bbox_inches="tight")
    fig.savefig(filename+".svg",bbox_inches="tight")
