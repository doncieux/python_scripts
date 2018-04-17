#!/usr/bin/python

import os
import subprocess

def download_results_variants(data_node, data_dir, data_filename, lvariants, no_download=False, initial_data_files = None):
    """Download results on the data_node computer and in the data_dir directory. Searches for the data_filename files in the listed variants, which is a list of strings (sferes variants names to look for). The value returned is a dictionary associating a list of files to a variant.
    """
    data_files={}  if not initial_data_files else dict(initial_data_files)
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
        data_files_variants=list(data_files[variant]) if variant in data_files else []
        for exp_file in files:
            print("Exp file: "+exp_file)
            ed=filter(lambda x: x.startswith("exp"),exp_file.split("/"))
            if(len(ed)==0):
                continue
            exp_dir=ed[0]
            out_exp_dir = exp_dir
            outfile = variant+"/"+out_exp_dir+"/"+data_filename
            outfile_index = 1
            while(outfile in data_files_variants):
              print("WARNING: Would have overwritten %s" % outfile)
              outfile_index += 1
              out_exp_dir = exp_dir+"-"+str(outfile_index)
              outfile = variant+"/"+out_exp_dir+"/"+data_filename
            if (not(os.path.isdir(out_exp_dir))):
                os.mkdir(out_exp_dir)
            if(not no_download):
                os.system('scp "%s:%s" "%s"' % (data_node, exp_file, out_exp_dir) )
            data_files_variants.append(variant+"/"+out_exp_dir+"/"+data_filename)
        os.chdir("..")
        data_files[variant]=data_files_variants
    return data_files

def download_results_structured_variants(data_node, data_dir, data_filename, mvariants,no_download=False, dfiles_dict = None):
    """Download results on the data_node computer and in the data_dir directory. Searches for the data_filename files in the listed variants, which is a dictionary of lists. A map is used in order to structure the list of variants into categories. The value returned is a dictionary associating to each variant category a dictionary associating a variant name to a list of files. 
    """
    data_files= {} if not dfiles_dict else dict(dfiles_dict)
    for setup in mvariants.keys():
        print("Setup: "+setup)
        if (not(os.path.isdir(setup))):
            os.mkdir(setup)
        os.chdir(setup)
        df_init = {}
        if(setup in data_files):
          for v in data_files[setup].keys():
            df_init[v] = map(lambda x:x.split("/",1)[1],data_files[setup][v])
          print("Initial df_init[v]: "+str(df_init[v]))
        df=download_results_variants(data_node, data_dir, data_filename, mvariants[setup], no_download, initial_data_files = df_init)
        for v in df.keys():
            df[v]=map(lambda x:setup+"/"+x,df[v])
#        if setup not in data_files.keys():
        data_files[setup]=df
#        else:
#            for v in df.keys():
#                if v in data_files[setup].keys():
#                    data_files[setup][v] += df[v]
#                else:
#                    data_files[setup][v] = df[v]
        #print df
        os.chdir("..")
    return data_files
