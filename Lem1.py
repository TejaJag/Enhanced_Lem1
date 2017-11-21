import numpy as np
import pprint as pp
from io import StringIO
import re, timeit, collections, random, math, os
import pandas as pd

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
    if(len(sorted_element) == 1):
        new_cols.append(["%s..%s"%(sorted_element[0], sorted_element[0]) for _ in range(column.shape[0])])
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

# ---------- Calculating A* --------------------


def A_set(vectors):
    # print(vectors)
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
    # print("A star:",A_set)
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


def lower(d_dict, A):	#vectors-contain decisions
    d_star_dict = d_dict
    lower_dict = {}
    lower_set = []
    conflict = False
    BigA = A
    #print("A: ", A)
    for key,value in d_star_dict.items():
        lower_pd = []		#lower_set for per d_set
        for sub_A in BigA:
            if set(sub_A) == set(np.intersect1d(sub_A, value)):
                #print("sub_A: ", sub_A)
                #print("value: ", value)
                lower_set.extend(sub_A)
                lower_pd.extend(sub_A)
        lower_dict[key] = lower_pd

    return lower_dict		#conflict, conflictSet 	#lower = diff conflictSet

def upper(d, A):
	d_star_dict = d
	upper_dict = {}
	BigA = A
	for key,value in d_star_dict.items():
		upper_pd = []
		for sub_A in BigA:
			if np.in1d(value,sub_A).any()==True:
				upper_pd.extend(sub_A)
		upper_dict[key] = upper_pd
	return upper_dict

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


# --------- Dealing with numerical attributes -----------
new_Data_attributeNames = []
new_cols_list = []
for i in range(0, attr_num):
    col = values[:, i]
    try:
        float(col[0])
        new_cols = col_cutpoints(col, i)
        new_Data_attributeNames.extend(["%s_%s"%(data[0,i],j) for j in range(len(new_cols))])
        new_cols_list.extend(new_cols)
    except ValueError:
        new_cols_list.append(list(col))
        new_Data_attributeNames.append(data[0, i])
new_Data_attributeNames = np.array(new_Data_attributeNames)
#----------------------------
print(" new at names:", new_Data_attributeNames)
print(np.array(new_cols_list).shape)
arr = np.array(new_cols_list)
print("--", arr[0:1, :])
print(type(new_cols_list))
#----------------
new_Data = np.array(new_cols_list).T
# print(new_Data[0:5,])
new_Data.shape = (len(new_cols_list[0]), len(new_Data_attributeNames))
new_Data_df = pd.DataFrame(new_Data)
print(new_Data_df.shape)
print(len(new_Data_attributeNames))
print(len(new_cols_list))
new_Data_df.columns = list(new_Data_attributeNames)
print(new_Data_df)
# ------------- A* d*--------------
A_star = A_set(new_Data)
d_set, d_set_dict = D_set(values[:, -1])
d_star = []
for item in d_set:
    d_star.append(list(item))
print(d_star)




# ---------Checking the consistency of decision table ---------------


outfileCertain = open(outFileName+".certain.r","w+")
outfilePossible = open(outFileName + ".possible.r", "w+")

allConcepts_Lower = lower(d_set_dict, A_star)






decision_str = data[0, -1]
rules = set()
for concept in allConcepts_Lower:
    # for each concept finding the certain rules
    # print("concept:", concept)
    # print("newTnames:", new_Data_attributeNames)
    rule_covering = {}
    concept_d_star = []  # adding special attribute value for every concept
    concept_d_star_dict = {}
    concept_cases = allConcepts_Lower.get(concept)  # list of cases for a single concept
    concept_d_star_dict[concept] = allConcepts_Lower.get(concept)
    concept_d_star.append(concept_cases)
    lis = []
    print("???",concept_cases)
    for i in range(cases_num):
        if i not in concept_cases:
            lis.append(i)
    print("fucking listttttttttttttttttttt",lis)
    concept_d_star.append(lis)
    concept_d_star_dict['special'] = lis
    print("concept dict:", concept_d_star_dict)

    temp_data = new_Data
    flag = True
    retained_att = list(new_Data_attributeNames)

    attribute_names = list(data[0, 0:-1])
    # print("at names:", retained_att)
    # print(isSubset(A_set(np.delete(temp_data, 0, axis=1)), concept_d_star))
    # print(temp_data.shape[1])

    while(flag):
        idx = 0
        while(temp_data.shape[1]>0 and flag ==True and idx < temp_data.shape[1]):
            if(isSubset(A_set(np.delete(temp_data, idx, axis=1)), concept_d_star)):
                # print("idx:", idx)

                del retained_att[idx]
                # print("ret att:", retained_att)
                temp_data = np.delete(temp_data,idx, axis=1)
                # print("drop col", temp_data)
                break
            else:
                # print("not dropped")
                idx = idx + 1
        if idx == temp_data.shape[1]:
            flag = False
            break
    print("att:", retained_att)

    #  extracting columns for retained attributes
    ret_att_data = new_Data_df[retained_att]
    # print(ret_att_data)
    ret_att_data_rows = ret_att_data.iloc[concept_d_star_dict[concept]]
    unique_rows = set([tuple(x) for x in ret_att_data_rows.to_records(index=False)])
    ruleset = {}
    for tup in unique_rows:
        print("tup:", tup)
        cond_str = []
        dropped_att = []
        intersect_cases = []
        dropped_count = 0
        if len(retained_att) >= 1:
            for i, value in enumerate(retained_att):  # checking for dropping conditions
                # set(np.where(ret_att_data[value] == tup[0])[0])
                df_list = []
                updated_df = ret_att_data
                for j, att in enumerate(retained_att):
                    if retained_att.index(att) != retained_att.index(value) and att not in dropped_att: # or i != j
                        print("i - j",i," ",j," ", tup[j])
                        print("heeeeeeeeeeereeeeeeeeeeeeee",att)
                        print(np.where(updated_df[att] == tup[j]))
                        df_list.append(set(np.where(updated_df[att] == tup[j])[0]))
                        print(df_list)
                        # updated_df = ret_att_data.iloc[new_df_list]
                        # print("updated_df:", updated_df)
                if len(df_list)!=0:
                    new_df_list = set.intersection(*df_list)
                else:
                    new_df_list = []
                print("new_df_list:", new_df_list)
                print(set(new_df_list) <= set(concept_d_star_dict[concept]))
                if (not set(new_df_list) <= set(concept_d_star_dict[concept])) or (len(retained_att) - dropped_count == 1) : # means cannot be dropped
                    print("UFFFOOOOOOOOOOOO")
                    print(set(list(np.where(ret_att_data[value] == tup[i])[0])))
                    intersect_cases.append(set(list(np.where(ret_att_data[value] == tup[i])[0])))
                    cond_str.append("(%s, %s)"%(value, tup[i]))
                else:
                    print("dropped")
                    dropped_count = dropped_count + 1
                    dropped_att.append(value)

                #     print(new_df_list)
        # print(set.intersection(*intersect_cases))
        ruu = ' & '.join(cond_str) + " -> " + "(%s, %s)"%(decision_str,concept)
        print(intersect_cases)
        print(set.intersection(*intersect_cases))
        rule_covering[ruu] = set.intersection(*intersect_cases)
        print(cond_str, "------------------------------------ ", concept)
    print("length::::::::::::::::::::::::::::::::::::::::::::::::", len(rule_covering.keys()))
    for i, rule in enumerate(rule_covering.keys()):
        print(rule)
        covering = rule_covering[rule]
        flag = 0
        for j, cases in enumerate(rule_covering.values()):
            if i != j:
                if covering <= cases:
                    flag = 1
                    break
        if flag == 0:
            rules.add(rule)
    print("len_after::::::::::::::::::::::::::::::::::::::::::::::",len(rules))
for rule in rules:
    strr = rule+"\n"
    outfileCertain.write(strr)


# -------------------------- Upper ------------------------- changes "rule_covering" allConcepts_Lower
print("upper start")
if(not isSubset(A_star, d_star)):
    allConcepts_Upper = upper(d_set_dict, A_star)

    rules2 = set()
    for concept in allConcepts_Upper:
        # for each concept finding the certain rules
        # print("concept:", concept)
        # print("newTnames:", new_Data_attributeNames)
        rule_covering2 = {}
        concept_d_star = []  # adding special attribute value for every concept
        concept_d_star_dict = {}
        concept_cases = allConcepts_Upper.get(concept)  # list of cases for a single concept
        concept_d_star_dict[concept] = allConcepts_Upper.get(concept)
        concept_d_star.append(concept_cases)
        lis = []
        print("???", concept_cases)
        for i in range(cases_num):
            if i not in concept_cases:
                lis.append(i)
        print("fucking listttttttttttttttttttt", lis)
        concept_d_star.append(lis)
        concept_d_star_dict['special'] = lis
        print("concept dict:", concept_d_star_dict)

        temp_data = new_Data
        flag1 = True
        retained_att = list(new_Data_attributeNames)

        attribute_names = list(data[0, 0:-1])
        # print("at names:", retained_att)
        # print(isSubset(A_set(np.delete(temp_data, 0, axis=1)), concept_d_star))
        # print(temp_data.shape[1])

        while (flag1):
            idx = 0
            while (temp_data.shape[1] > 0 and flag1 == True and idx < temp_data.shape[1]):
                print("RRRRRRRRRRRR",A_set(np.delete(temp_data, idx, axis=1)))
                print(concept_d_star)
                if (isSubset(A_set(np.delete(temp_data, idx, axis=1)), concept_d_star)):
                    # print("idx:", idx)
                    print("deleted att:",retained_att[idx])
                    del retained_att[idx]
                    # print("ret att:", retained_att)
                    temp_data = np.delete(temp_data, idx, axis=1)
                    # print("drop col", temp_data)
                    break
                else:
                    # print("not dropped")
                    idx = idx + 1
            if idx == temp_data.shape[1]:
                flag1 = False
                break
        print("att:", retained_att)

        #  extracting columns for retained attributes
        ret_att_data = new_Data_df[retained_att]
        # print(ret_att_data)
        ret_att_data_rows = ret_att_data.iloc[concept_d_star_dict[concept]]
        unique_rows = set([tuple(x) for x in ret_att_data_rows.to_records(index=False)])
        ruleset = {}
        for tup in unique_rows:
            print("tup:", tup)
            cond_str = []
            dropped_att = []
            intersect_cases = []
            dropped_count = 0
            if len(retained_att) >= 1:
                for i, value in enumerate(retained_att):  # checking for dropping conditions
                    # set(np.where(ret_att_data[value] == tup[0])[0])
                    df_list = []
                    updated_df = ret_att_data
                    for j, att in enumerate(retained_att):
                        if retained_att.index(att) != retained_att.index(value) and att not in dropped_att:  # or i != j
                            print("i - j", i, " ", j, " ", tup[j])
                            print("heeeeeeeeeeereeeeeeeeeeeeee", att)
                            print(np.where(updated_df[att] == tup[j]))
                            df_list.append(set(np.where(updated_df[att] == tup[j])[0]))
                            print(df_list)
                            # updated_df = ret_att_data.iloc[new_df_list]
                            # print("updated_df:", updated_df)
                    if len(df_list)!=0:
                        new_df_list = set.intersection(*df_list)
                    else:
                        new_df_list = []
                    print("new_df_list:", new_df_list)
                    print(set(new_df_list) <= set(concept_d_star_dict[concept]))
                    if (not set(new_df_list) <= set(concept_d_star_dict[concept])) or (len(retained_att) - dropped_count == 1):  # means cannot be dropped
                        print("UFFFOOOOOOOOOOOO")
                        print(set(list(np.where(ret_att_data[value] == tup[i])[0])))
                        intersect_cases.append(set(list(np.where(ret_att_data[value] == tup[i])[0])))
                        cond_str.append("(%s, %s)" % (value, tup[i]))
                    else:
                        print("dropped")
                        dropped_count = dropped_count + 1
                        dropped_att.append(value)

                        #     print(new_df_list)
            # print(set.intersection(*intersect_cases))
            ruu = ' & '.join(cond_str) + " -> " + "(%s, %s)" % (decision_str, concept)
            print(intersect_cases)
            print(set.intersection(*intersect_cases))
            rule_covering2[ruu] = set.intersection(*intersect_cases)
            print(cond_str, "------------------------------------ ", concept)

        for i, rule in enumerate(rule_covering2.keys()):
            print("shit:", rule)
            covering = rule_covering2[rule]
            print("covering:", covering)
            flag = 0
            for j, cases in enumerate(rule_covering2.values()):
                if i != j:
                    print("cases:", cases)
                    if covering <= cases:
                        print("flagged")
                        flag = 1
                        break
            if flag == 0:
                rules2.add(rule)

    for rule in rules2:
        strr = rule + "\n"
        print("rules added:", rule)
        outfilePossible.write(strr)

else:
    str = "! Possible rule set is not shown since it is identical with the certain rule set"
    outfilePossible.writelines(str)





