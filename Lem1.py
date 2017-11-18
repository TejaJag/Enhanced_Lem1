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
new_Data = np.array(new_cols_list).T

# ---------- Calculating A* --------------------

def A_set(vectors):
    Attrs = vectors.tolist()
    A_set = []
    # unique_vecs = [vec for vec in set(tuple(x.tolist()) for x in Attrs)]
    vec_set = [list(vec) for vec in set(tuple(x) for x in Attrs)]
    for vec in vec_set:
        # print(vec)
        # A_set.append(np.where(np.prod(vectors==vec,axis=-1))[0])
        A_set.append([pos for pos, y in enumerate(Attrs) if y == vec])
    # print(A_set)

    # print("****Time for A_set: ", stop-A_build)
    print(A_set)
    return A_set


def D_set(concept_column):
    d_set = []
    d_set_dict = {}
    uniques =  np.unique(concept_column)
    for key in uniques:
        s_set = np.where(concept_column == key)[0]
        d_set.append(s_set)
        d_set_dict[key] = s_set
    print("d_set_dict: ", d_set_dict)
    print("d_set: ", d_set)
    return d_set, d_set_dict


A_star = A_set(new_Data)
d_set, d_set_dict = D_set(values[:, -1])
d_star = []
for item in d_set:
    d_star.append(list(item))
print(d_star)


def isSubset(list1, list2):
    for lis1 in list1:
        for lis2 in list2:
            flag = False
            if (set(lis1) <= set(lis2)):
                flag = True
                break
        if(flag == False):
            break
    return flag

# ---------Checking the consistency of decision table ---------------

outfilePossible = open(outFileName+".possible.r","w+")
# outfileCertain =  open(outFileName+".certain.r","wb")
if(isSubset(A_star, d_star)):
    str = "! Possible rule set is not shown since it is identical with the certain rule set"
    outfilePossible.writelines(str)
    outfilePossible.close()

# arr = d_set[1]
# print(type(arr))
# unique_rows = list(set(tuple(map(tuple, new_Data))))

# A_Star = []
# new_Data_list = (row for )
# for i in range(new_Data.shape[0]):

