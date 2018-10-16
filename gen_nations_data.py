#!/usr/bin/env python3
"""
Generate nation-specific data sets
"""
import pandas as pd

fname = "dat/response.csv"
df = pd.read_csv(fname)
meta = pd.read_csv("dat/metadata_coded.csv")
nations = meta["nation"].tolist()
nation_set = sorted(list(set(nations)))
nations_data = list()
for nation in nation_set:
    idxs = [i for i, x in enumerate(nations) if x == nation]
    nation_df = df.iloc[idxs,:].reset_index(drop=True)
    nation_df.to_csv("dat/nation/{}.csv".format(nation),index=False)
    nations_data.append((len(idxs),nation))

### qd pie distribution
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams.update({'text.usetex': False,
                    'font.family': 'serif',
                    'font.serif': 'cmr10',
                    'font.weight':'bold',
                    'mathtext.fontset': 'cm',
                    'axes.unicode_minus'  : False
                    })

fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
data = [x[0] for x in nations_data]
labels = [x[1].upper() for x in nations_data]
idxs = sorted(range(len(data)),key=data.__getitem__)
data = [data[idx] for idx in idxs]
labels = [labels[idx] for idx in idxs]

def func(pct, allvals):
    absolute = int(pct/100.*np.sum(allvals))
    return "{:.1f}%".format(pct)

ax.pie(data,labels=labels, autopct=lambda pct: func(pct, data))
ax.set_title("Participating Nations")

plt.savefig("fig/nations.png")
plt.close()
