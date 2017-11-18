import numpy as np
import pprint as pp
from io import StringIO
import re, timeit, collections, random, math, os


def read_dataset(path):
    print("Reading data...")
    in_path = str(path)+".txt"
    data_sets= []
    first_reg = re.sub(r'\<(.+?)\>|\!(.*?\n)','',open(in_path,'r').read(),flags=re.DOTALL)
    # print(first_reg)
    sec_reg = re.search(r'(\[(.+?)\])(.+?$)',first_reg,flags=re.DOTALL)
    # print(sec_reg)
    attr_d = list(filter(None, re.split(r'\s+',sec_reg.group(2),flags=re.DOTALL)))
    # print("attr_d: ", attr_d)
    data_sets.append(attr_d)  # first row of data_sets is its attris and decision
    elm_num = len(attr_d)		# elm_num = 16281
    mess_data = list(filter(None, re.split(r'\s+',sec_reg.group(3),flags=re.DOTALL)))
    set_num = int(len(mess_data)/elm_num)		#set_num = 68
    [data_sets.append(mess_data[i*elm_num:(i+1)*elm_num]) for i in range(0, set_num)]

    data = np.array(data_sets)  # change to ndarry type
    print(data)
    return data


all_files = os.listdir(os.curdir)
print("current: ", all_files)
InFilename = input("Enter the name of the input data file? For example: test\n")
while not "%s.txt"%InFilename in all_files:
    InFilename = input("The file is not in this directory, please check and input again!\n")
outFileName = input("Enter the output file name:")
# create two files for rules later
data = read_dataset(InFilename)
values = data[1:]  # removing column names vector
print(values)
cases_num = len(values[:, 0])  # count of data rows
attr_num = len(values[0, 0:-1])  # count of attributes


# --------- Dealing with numerical attributes -----------
