#!/usr/bin/python

import data_extraction as de

def from_file_to_data(files,lcol_num,col_num_main,filter_values):
    """From a list of files corresponding to the results from different runs of a same experience which are the files to analyse, extract the values and put them in a data structure. files is the list of files, lcol_num the columns to extract, col_num_main the column number of the main dimension (X-axis), filter_values, the values to keep along the main dimension. The returned value is a list of the data extracted from each file. The files that do not contain enigh data are ignored.
    """
    if (col_num_main not in lcol_num):
        lcol_num.insert(0,col_num_main)

    col_num_main_relative=lcol_num.index(col_num_main)
    #print "from_file_to_data: extracting columns "+str(lcol_num)+" main: "+str(col_num_main)+" relative: "+str(col_num_main_relative)
    data=[]

    for file in files:
        fdata=de.data_extraction(file,lcol_num)
        fdata=de.data_filter(fdata,col_num_main_relative, filter_values)
        print("Extracted "+str(len(fdata))+" in the file (len="+str(len(filter_values))+")")
        if (len(fdata)==len(filter_values)):
            data.append(fdata)
            #print "Extracted "+str(len(fdata))+" lines from "+file+" "+str(fdata)
    print("From "+str(len(files))+" files, "+str(len(data))+" allowed to extract data")
    return data

def merge_run_data(data,col_num_main=0):
    """Restructure the data from a list of data corresponding to a set of files into a structure that merges the data for each file. The returned value is a dictionary that associates a list of values to each main col value.
    """

    nb_cols=len(data[0][0])
    ndata={}
    for col in range(nb_cols):
        if (col == col_num_main):
            continue
        ndata[col]={}

        for f in range(len(data)):
            for l in range(len(data[f])):
                if (data[f][l][col_num_main] in ndata[col].keys()):
                    ndata[col][data[f][l][col_num_main]].append(data[f][l][col])
                else:
                    ndata[col][data[f][l][col_num_main]]=[data[f][l][col]]

    return ndata
        
def aggregate_col_max(data,values_to_aggregate):
    """Aggregate different values with a max. The data argument is a list of lists. The returned value is a list of list in which the values to aggregate have been replaced by the max in the list.""" 
    ndata=[]
    for d in data:
        r=list(range(len(d)))
        #print "aggregate col max. r="+str(r)+" val to aggregate="+str(values_to_aggregate)
        for va in values_to_aggregate:
            r.remove(va)
        nd=[d[i] for i in r]
        nd.append(max([d[i] for i in values_to_aggregate]))
        ndata.append(nd)
    return ndata
