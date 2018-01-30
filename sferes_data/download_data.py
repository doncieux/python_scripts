#!/usr/bin/python

import os
import subprocess

def download_results_variants(data_node, data_dir, data_filename, lvariants):
    """Download results on the data_node computer and in the data_dir directory. Searches for the data_filename files in the listed variants, which is a list of strings (sferes variants names to look for). The value returned is a dictionary associating a list of files to a variant.
    """
    data_files={}
    for variant in lvariants:
        print("\tVariant: "+variant)
        if (not(os.path.isdir(variant))):
            os.mkdir(variant)
        os.chdir(variant)
        ls = subprocess.Popen(['ssh',data_node, 'find',data_dir+"/"+variant+"/","-iname",data_filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err =  ls.communicate()
        #print out
        files=str(out).split("\n")
        data_files_variant=[]
        #print(str(files))
        data_files_variants=[]
        for exp_file in files:
            print("Exp file: "+exp_file)
            ed=filter(lambda x: x.startswith("exp"),exp_file.split("/"))
            if(len(ed)==0):
                continue
            exp_dir=ed[0]
            if (not(os.path.isdir(exp_dir))):
                os.mkdir(exp_dir)
            os.system('scp "%s:%s" "%s"' % (data_node, exp_file, exp_dir) )
            data_files_variants.append(variant+"/"+exp_dir+"/"+data_filename)
        os.chdir("..")
        data_files[variant]=data_files_variants
    return data_files

def download_results_structured_variants(data_node, data_dir, data_filename, mvariants):
    """Download results on the data_node computer and in the data_dir directory. Searches for the data_filename files in the listed variants, which is a dictionary of lists. A map is used in order to structure the list of variants into categories. The value returned is a dictionary associating to each variant category a dictionary associating a variant name to a list of files. 
    """
    data_files={}
    for setup in mvariants.keys():
        print("Setup: "+setup)
        if (not(os.path.isdir(setup))):
            os.mkdir(setup)
        os.chdir(setup)
        df=download_results_variants(data_node, data_dir, data_filename, mvariants[setup])
        for v in df.keys():
            df[v]=map(lambda x:setup+"/"+x,df[v])
        data_files[setup]=df
        os.chdir("..")
    return data_files
