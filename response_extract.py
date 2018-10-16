#!/usr/bin/env python3
"""
Import and clean original spreadsheet
    - keep only rows that contain at least one answer
"""
import glob, os
import pandas as pd
fname = glob.glob("dat/*.xlsx")
df0 = pd.read_excel(fname[0])
# remove first row and last column
df0 = df0.drop(labels = "Samlet status",axis=1)
df0 = df0.drop(0)
df0 = df0.reset_index(drop=True)
# remove non-response
idx_nan = df0.isnull()
n_nan = list()
for index, row in idx_nan.iterrows():
    n_nan.append(row.sum())
idxs = [i < df0.shape[1] for i in n_nan]
df1 = df0[idxs].reset_index(drop=True)
df1.to_csv("dat/response.csv",index=False)
