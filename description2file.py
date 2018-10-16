#!/usr/bin/env python3
"""
Descriptive statistics of each item
"""
import os
import pandas as pd
fname = "dat/response.csv"
df1 = pd.read_csv(fname)

fobj = open("descriptive_stats.txt","w")
for i, column in enumerate(df1):
    res = df1[column].describe()
    fobj.write("column {}\n{}\n ********** \n".format(i,res))
fobj.close()
