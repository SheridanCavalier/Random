#!/usr/bin/env python3

'''Chunk large fastqs or fastas into smaller files, set -t to targeted number of reads for each file'''

import os
import sys
import mappy as mm
from tqdm import tqdm
import multiprocessing as mp
import shutil
from glob import glob
import math
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-r', '--input_file', type=str)
parser.add_argument('-o', '--output_path', type=str)
parser.add_argument('-t', '--groupsize', type=str)

args = parser.parse_args()
input_file=args.input_file
path=args.output_path
groupsize = args.groupsize


def make_chunks(input_file, groupsize):
    read_dict={}
    target=int(groupsize)
    rootname=input_file.split('.')[0]
    linenum=1
    for line in open(input_file):
            if linenum%4 == 1:
                name=((line.rstrip()).split(' ')[0])[1:]
                read_dict[name]=[]
            if linenum%4 == 2:
                seq=line.rstrip()
                read_dict[name].append(seq)
            if linenum%4 == 3:
                strand=line.rstrip()
                read_dict[name].append(strand)
            if linenum%4 == 0:
                qual=line.rstrip()
                read_dict[name].append(qual)
            linenum+=1
    iters=math.ceil(len(read_dict)/target)
    for iter in range(1, iters+1):
        iteration=iter
        iterate(iter,target,read_dict, rootname)


def iterate(iteration, target, read_dict, rootname):
    keys=list(read_dict)
    split_fq = rootname + '_' + str(iteration)+'.fastq'
    write_fastq = open(split_fq, 'w+')
    if ((iteration*target)-target)== 0:
        for i in range(0,(iteration*target)):
            print(keys[i])
            write_fastq.write('@%s\n%s\n%s\n%s\n' %(keys[i],read_dict[keys[i]][0],read_dict[keys[i]][1],read_dict[keys[i]][2]))
        write_fastq.close()
    
        
    else:
        for i in range(((iteration*target)-target),iteration*target):
            write_fastq.write('@%s\n%s\n%s\n%s\n' %(keys[i],read_dict[keys[i]][0],read_dict[keys[i]][1],read_dict[keys[i]][2]))
            if i == len(read_dict)-1:
                break
        write_fastq.close()


make_chunks(input_file, groupsize)


#tmp_fa = tmp_dir + 'tmp_for_blat.fasta'
#tmp_fa_fh = open(tmp_fa, 'w+')
 


 #if len(read_dict)== target:
            #iteration+=1



    #for entry in read_dict:
        #write_fasta.write('>%s\n%s\n' %(entry, read_dict[entry][0]))
    #return read_dict
     

