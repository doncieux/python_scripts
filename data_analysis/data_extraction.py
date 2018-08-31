#!/usr/bin/python

import os

def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)

def data_extraction(filename, lcol_num, not_num_ignore=False):
    """Extracts a list of columns from a given file and returns a list of lists (list of the data for each line).file->[[<data of line 1>][<data of line 2>]...]"""
    f=open(filename,'r')
    lines=list(filter(lambda x:x.lstrip()[0]!='#',f.readlines())) # we remove the comments
    data=[]
    for l in lines:
        ls=l.split()
        data_line=[]
        to_ignore=False
        for c in lcol_num:
            if (c > len(ls)):
                print "WARNING: not enough data on this line: ignored..."
                to_ignore=True
                break
            else:
                try:
                    x=num(ls[c])
                    
                except ValueError:
                    if (not_num_ignore):
                        to_ignore=True
                    else:
                        x=0
                data_line.append(x)
        if (not(to_ignore)):
            #print("extracted: "+str(data_line)+" from "+filename)
            data.append(data_line)
    f.close()
    #print("Data extracted from "+filename+": "+str(len(data))+" lines")
    return data

def data_extraction_max(filename, lcol_num, not_num_ignore=False):
    """Extracts a list of columns from a given file and returns a list of lists (list of the data for each line). Keeps the max so far, instead of just the values. file->[[<data of line 1>][<data of line 2>]...]"""
    f=open(filename,'r')
    lines=list(filter(lambda x:x.lstrip()[0]!='#',f.readlines())) # we remove the comments
    data=[]
    max_data=[]
    for l in lines:
        ls=l.split()
        data_line=[]
        to_ignore=False
        for c in lcol_num:
            if (c > len(ls)):
                print "WARNING: not enough data on this line: ignored..."
                to_ignore=True
                break
            else:
                try:
                    x=num(ls[c])
                    
                except ValueError:
                    if (not_num_ignore):
                        to_ignore=True
                    else:
                        x=0
                data_line.append(x)
        if (not(to_ignore)):
            #print("extracted: "+str(data_line)+" from "+filename)
            if (not max_data):
                data.append(data_line)
                max_data=data_line
            else:
                old_max=max_data
                for i in range(len(max_data)):
                    max_data[i]=max(data_line[i],max_data[i])
                if (max_data != data_line):
                    print("Data_ex_max: dataline="+str(data_line)+" maxdata="+str(old_max)+" new maxdata="+str(max_data))
                data.append(max_data)
    f.close()
    #print("Data extracted from "+filename+": "+str(len(data))+" lines")
    return data

def data_filter(data, col_num, values):
    """Keeps only the data having a value in the list of values on the given column number. data is a list of lists (list of lines, each corresponding to a list of column values).[[<data of line 1>][<data of line 2>]...]->[[<data of line X>][<data of line Y>]...] where line X, Y and others respect the filter values."""
    
    ndata=list(filter(lambda x:len(x)>col_num,data))
    ndata=list(filter(lambda x:x[col_num] in values,ndata))
    #print("Filtering data: going from "+str(len(data))+" lines to "+str(len(ndata))+" lines, values="+str(values))
    return ndata


 
