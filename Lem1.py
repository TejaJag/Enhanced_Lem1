import numpy as np
import pprint as pp
from io import StringIO
import re, timeit, collections, random, math, os


def read_dataset(path):
    print("Reading data...")
    in_path = str(path)+".txt"
    data_sets = []
    first_reg = re.sub(r'\<(.+?)\>|\!(.*?\n)','',open(in_path,'r').read(),flags=re.DOTALL)
    sec_reg = re.search(r'(\[(.+?)\])(.+?$)',first_reg,flags=re.DOTALL)
    attr_d = list(filter(None, re.split(r'\s+',sec_reg.group(2),flags=re.DOTALL)))
    data_sets.append(attr_d)  # first row of data_set is its attributes and decision
    elm_num = len(attr_d)
    mess_data = list(filter(None, re.split(r'\s+',sec_reg.group(3),flags=re.DOTALL)))
    set_num = int(len(mess_data)/elm_num)
    [data_sets.append(mess_data[i*elm_num:(i+1)*elm_num]) for i in range(0, set_num)]
    data = np.array(data_sets)  # change to ndarry type
    # print(data)
    return data


def col_cutpoints(column,j):
    column = column.astype(np.float)
    cases_cnt = len(column)
    sorted_element = []  # all unique elements in the column
    sorted_element = sorted(np.unique(column))
    start_value = sorted_element[0]
    end_value = sorted_element[-1]
    cp_list = []  # cut point list
    for i in range(0, len(sorted_element) - 1):
        cut_point = round((np.float(sorted_element[i]) + np.float(sorted_element[i + 1])) / 2, 4)
        cp_list.append(cut_point)
    new_cols = []
    for cp in cp_list:
        col = []
        for val in column:
            if (val >= start_value) & (val < cp):
                col.append("%s..%s"%(start_value, cp))
            elif (val > cp) & (val <= end_value):
                col.append("%s..%s" % (cp, end_value))
        new_cols.append(col)
    # print(new_cols)
    return new_cols
        # print(np.where((column >= start_value) & (column < cp))[0])





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
# print(type(values)) ndarray
col_cutpoints(values[:, 0], 0)
# --------- Dealing with numerical attributes -----------
new_cols_list = []
for i in range(0, attr_num):
    col = values[:, i]
    try:
        float(col[0])
        new_cols_list.extend(col_cutpoints(col, i))
    except ValueError:
        new_cols_list.extend(list(col))
new_data = np.array(new_cols_list).T
#         col_av_dict = col_av(col, i)
#         t_total_av.extend(col_av_dict)