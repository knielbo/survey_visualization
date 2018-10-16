#!/usr/bin/env python3
"""
Export item content
"""
import pandas as pd
fname = "dat/response.csv"
df = pd.read_csv(fname)
items = df.columns.tolist()
out = pd.DataFrame()
out["long-form"] = items
out.to_csv("dat/items.csv")
