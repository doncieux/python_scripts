#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Alexandre Coninx
    ISIR CNRS/UPMC
    05/02/2018
""" 

import numpy as np


from matplotlib import *
use('Agg')
import matplotlib.pyplot as plt

max_fitness = 10
n_containers = 10

def load_data_percondition(fname):
	dict_out = {}
	with open(fname,'r') as fd:
		fd.next() # header
		for line in fd:
			data = line.strip().split(";")
			condition = data[0]
			exp = data[1]
			container_id = int(data[2])
			counts = [int(data[i]) for i in range(3,3+max_fitness+1)]
			if condition not in dict_out.keys():
				dict_out[condition] = {}
			if container_id not in dict_out[condition].keys():
				dict_out[condition][container_id] = []
			dict_out[condition][container_id].append(counts)
	return dict_out
	
	
def compute_mean_std(countdata):
	dict_out = {}
	for condition in countdata.keys():
		dict_out[condition] = {}
		for i in range(n_containers):
			datapoints = np.array(countdata[condition][i])
			avg = np.mean(datapoints, axis=0)
			std = np.std(datapoints, axis=0)
			dict_out[condition][i] = (avg, std)
	return dict_out
	
	
def plot_histos(data,names={}):
	for condition in data.keys():
		for i in range(n_containers):
			mean, std = data[condition][i]
			#fancyname = condition if condition not in names.keys() else names[condition]
			filename = "%s_container%d" % (condition, i)
			plot_discretehisto(mean, std, filename)





def plot_discretehisto(mean, std, name,logscale=False):
	fig=plt.figure()
	if(logscale):
		plt.yscale('log')
	ax=fig.add_subplot(111)
	barplot = ax.bar(np.arange(max_fitness+1)+0.5, mean, width=0.5, yerr=std)
	ax.set_ylim([0,np.max(mean+std)*1.01])
	ax.set_xlim([0,max_fitness+1])
	ax.set_xlabel("Fitness")
	ax.set_ylabel("Occurences")
	ax.xaxis.set_ticks(np.arange(0, max_fitness+1)+0.5)
	ax.set_xticklabels(range(max_fitness+1))
	plt.margins(0.2)
	plt.subplots_adjust(bottom=0.15)
	fig.savefig(name+".pdf",bbox_inches="tight")
	fig.savefig(name+".svg",bbox_inches="tight")


