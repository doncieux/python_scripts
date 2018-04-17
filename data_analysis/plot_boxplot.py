#!/usr/bin/python

import numpy as np

#import matplotlib
from matplotlib import *
use('Agg')
import matplotlib.pyplot as plt
from itertools import cycle

import glob
from pylab import *
import scipy.stats

import brewer2mpl


params = {
    'axes.labelsize': 8,
    'text.fontsize': 8,
    'font.size': 10,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'text.usetex': False,
    'pdf.fonttype': 42, # Avoid Type3 fonts in PDF for submission
    'ps.fonttype': 42
#    'figure.figsize': [4.5, 4.5]
}
rcParams.update(params)

def stars(p):
    if p < 0.0001:
        return "****"
    elif (p < 0.001):
        return "***"
    elif (p < 0.01):
        return "**"
    elif (p < 0.05):
        return "*"
    else:
        return "-"


def plot_boxplot(data,filename,title,gen, names={},ylabel="max fitness",orderedkeys=None,colordict=None):
    """Plots the data corresponding to multiple variants with their variance. The arguments are the data, the list of variant names and a filename to save the figure. The data is a dictionary that associates to a variant name a dictionay that associates a list of variants values to each x value.   
    """

    fig=plt.figure()
    ax=fig.add_subplot(111)
    
    bp_data=[]
    bp_name=[]

    y_min=10000
    y_max=-10000

    if orderedkeys:
        datakeys = orderedkeys
    else:
        datakeys = data.keys()
        datakeys.sort()

    for variant in datakeys:
        print("Plotting data associated to variant: "+variant)
        lx=data[variant].keys()

        if (not(gen in lx)):
            print("no data...")
            continue

        print(str(data[variant][gen]))
        y_min=min(y_min,min(data[variant][gen]))
        y_max=max(y_max,max(data[variant][gen]))

        bp_data.append(data[variant][gen])
        if (variant in names.keys()):
            name=names[variant]
        else:
            name=variant
        bp_name.append(name)

    print("Boxplot data: "+str(bp_data))
    if (len(bp_data)==0):
        return

    y_max=y_max+0.1*(y_max-y_min)

    bp = ax.boxplot(bp_data, notch=0, sym='b+', vert=1, whis=1.5,
             positions=None, widths=0.6)

    bmap = brewer2mpl.get_map('Set3', 'qualitative', 12)
    colors = bmap.mpl_colors

    for i in range(len(bp['boxes'])):
        box = bp['boxes'][i]
        box.set_linewidth(0)
        boxX = []
        boxY = []
        col = colors[i % len(colors)] if not colordict else colordict[datakeys[i]]
        for j in range(5):
            boxX.append(box.get_xdata()[j])
            boxY.append(box.get_ydata()[j])
            boxCoords = zip(boxX,boxY)
            boxPolygon = Polygon(boxCoords, facecolor = col, linewidth=0)
            ax.add_patch(boxPolygon)


    for i in range(0, len(bp['boxes'])):
        col = colors[i % len(colors)] if not colordict else colordict[datakeys[i]]
        bp['boxes'][i].set_color(col)
        # we have two whiskers!
        bp['whiskers'][i*2].set_color(col)
        bp['whiskers'][i*2 + 1].set_color(col)
        bp['whiskers'][i*2].set_linewidth(2)
        bp['whiskers'][i*2 + 1].set_linewidth(2)
        # top and bottom fliers
        #bp['fliers'][i * 2].set(markerfacecolor=colors[i % len(colors)],
        #                        marker='o', alpha=0.75, markersize=6,
        #                        markeredgecolor='none')
        #bp['fliers'][i * 2 + 1].set(markerfacecolor=colors[i % len(colors)],
        #                            marker='o', alpha=0.75, markersize=6,
        #                            markeredgecolor='none')
        bp['fliers'][i].set(markerfacecolor=col,
                                marker='o', alpha=0.75, markersize=6,
                                markeredgecolor='none')
        bp['medians'][i].set_color('black')
        bp['medians'][i].set_linewidth(3)
        # and 4 caps to remove
        for c in bp['caps']:
            c.set_linewidth(0)
            
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    ax.tick_params(axis='x', direction='out')
    ax.tick_params(axis='y', length=0)

    ax.grid(axis='both', color="0.9", linestyle='-', linewidth=1)
    ax.set_axisbelow(True)
    ax.set_xticklabels(bp_name, rotation=40, ha='right')


    ax.set_ylim([y_min-0.01*(y_max-y_min),y_max+(y_max-y_min)*0.01])
    ax.set_ylabel(ylabel)
    
#    ax.set_title(title)
    plt.margins(0.2)
    plt.subplots_adjust(bottom=0.15)

    fig.savefig(filename+".pdf",bbox_inches="tight")
    fig.savefig(filename+".svg",bbox_inches="tight")

    # dict of statistical significance
    ss={} # content: 0: ([0,1,"**"], [1,2,"*"]), 1: ...
    # Adding statistical significance of the difference
    for i in range(len(bp_data)):
        for j in range(i+1,len(bp_data)):
            z,p = scipy.stats.mannwhitneyu(bp_data[i],bp_data[j])
            p_value = p * 2
            if (p_value>0.05):
                continue
            s = stars(p)
            ssl=0 #line in which to add the statistical significance
            added=False
            while(not(added)):
                if(ssl in ss.keys()):
                    ok=True
                    for ssij in ss[ssl]:
                        print("Comparing "+str(i)+", "+str(j)+" to "+str(ssij)+" ssl="+str(ssl))
                        if (i<=ssij[0]):
                            x1=i
                            x2=ssij[0]
                            y1=j
                            y2=ssij[1]
                        else:
                            x2=i
                            x1=ssij[0]
                            y2=j
                            y1=ssij[1]

                        if(y1>x2):
                            ok=False
                            ssl=ssl+1
                            break
                    if(ok):
                        print("Adding "+str((i,j,s))+" to "+str(ssl))
                        ss[ssl].append((i,j,s))
                        added=True
                else:
                    print("Adding "+str((i,j,s))+" to "+str(ssl))
                    ss[ssl]=[(i,j,s)]
                    added=True

    # we plot the lines
    for l in ss.keys():
        for ll in ss[l]:
            print("Adding stat significance: x1="+str(ll[0])+" x2="+str(ll[1])+" y="+str(y_max+l*abs(y_max - y_min)*0.1)+" l="+str(l)+" star: "+ll[2])
            ax.annotate("", xy=(ll[0]+1+0.01, y_max+l*abs(y_max - y_min)*0.05), xycoords='data',
                        xytext=(ll[1]+1-0.01, y_max+l*abs(y_max - y_min)*0.05), textcoords='data',
                        arrowprops=dict(arrowstyle="-", ec='#aaaaaa',
                                        connectionstyle="bar,fraction="+str(0.05/(ll[1]-ll[0]))))
            ax.text((ll[0]+ll[1])/2.0+1, y_max + l*abs(y_max - y_min)*0.05+0.15, ll[2],
                    horizontalalignment='center',
                    verticalalignment='center')

    y_max = y_max+max(ss.keys())*abs(y_max - y_min)*0.1

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    ax.tick_params(axis='x', direction='out')
    ax.tick_params(axis='y', length=0)

    ax.grid(axis='both', color="0.9", linestyle='-', linewidth=1)
    ax.set_axisbelow(True)
    ax.set_xticklabels(bp_name, rotation=40, ha='right')

    #ax.set_ylim([y_min-0.1*(y_max-y_min),y_max+(y_max-y_min)*0.1])
    ax.set_ylim([y_min-0.01*(y_max-y_min),y_max+(y_max-y_min)*0.01])
    ax.set_ylabel(ylabel)
    
#    ax.set_title(title)
    plt.margins(0.2)
    plt.subplots_adjust(bottom=0.15)


    fig.savefig(filename+"_stat.pdf",bbox_inches="tight")
    fig.savefig(filename+"_stat.svg",bbox_inches="tight")
