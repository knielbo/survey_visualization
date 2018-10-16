#!/usr/bin/env python3
"""
Solution for embedded items 5x5 matrices
    - plot data as grid and average response in each category (col 0)
    - compare with random/no-structure model (col 1)
    - compare with user-specified model (col 2)
"""
# core
import csv, os, re
# data management
import pandas as pd
# scientific computing
import numpy as np
from scipy import linalg, mat, dot
from scipy.stats import norm
# vis
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib as mpl
# progress bar
from tqdm import tqdm

def mat2grid(M):
    """ transform response dataframe to grid response
    """
    X = np.zeros([5,5])

    ### frequency of response
    for j, x in enumerate(X):
        col = M[:,j]
        for jj in col:
            if np.isnan(jj) == False:
                X[int(jj)-1,j] += 1

    ### relative frequency of response
    for k in range(X.shape[0]):
        X[:,k] = X[:,k]/sum(X[:,k])

    return X

def addnoise(mdl,step=2):
    """ add integer noise to model respoinses
        - +/- step noise
    """
    # noise in tange -1
    noise = np.random.randint(-1-step, high=step+1, size=mdl.shape)
    mdlnoise = mdl + noise

    # floor & roof on values
    for j, vec in enumerate(mdlnoise):
        for jj, val in enumerate(vec):
            if val < 1:
                mdlnoise[j,jj] = 1
            elif val > 5:
                mdlnoise[j,jj] = 5

    return mdlnoise

def geom_dist_mat(M1,M2):
    """average cosine distance for columns in M1 and M2
    """
    delta_mat = list()
    for i, m1 in enumerate(M1.T):
        m2 = M2[:,i]
        delta = dot(m1,m2.T)/linalg.norm(m1)/linalg.norm(m2)
        delta_mat.append(1 - delta)

    return np.mean(delta_mat)

def mdl2plot(M,mdl,q_str,filename="embed_plt.png",outname="embed_data.txt"):
    # create matrices
    ## data
    X = mat2grid(M)

    ## random model
    mdl0 = np.random.randint(1, high=6, size=M.shape)

    ## contrast model
    mdl1 = np.array([mdl for row in M])

    ## number of samples from model
    n = 1000

    dim1_str = ["Nothing", "Plans", "Locally","Strategy","Portfolio"]
    dim2_str = ["No","Yes"]

    mdl_spc = [mdl0, mdl1]
    mdl_strs = ["Random model","Contrast model"]
    mdl_spc_size = len(mdl_spc)

    # figure properties
    fig, ax = plt.subplots(2,mdl_spc_size+1,dpi=300)
    fig.set_size_inches(9,6)
    fig.subplots_adjust(wspace = .6, hspace = .25)

    # data model
    pl = ax[0,0].pcolormesh(X,cmap = plt.cm.Spectral_r,edgecolor='k',shading='gouraud')
    ax[0,0].axis('image')
    ax[0,0].set_title(q_str)
    ax[0,0].set_xticks(range(0,5))
    ax[0,0].set_xticklabels(dim1_str)
    ax[0,0].set_yticks([0.5,3.5])
    ax[0,0].set_yticklabels(dim2_str)
    for tick in ax[0,0].get_xticklabels():
        tick.set_rotation(45)
        divider = make_axes_locatable(ax[0,0])
        cax = divider.append_axes("right", size="5%", pad=0.05)
        cbar = fig.colorbar(pl,cax=cax)


    # central tendencies for data
    y = np.nanmean(M,axis=0)
    error = [val/np.sqrt(M.shape[0]) for val in np.nanstd(M,axis=0)]
    xpos = range(0,len(y))
    ax[1,0].bar(xpos, y, yerr=error, align='center',alpha=0.5, color="r", ecolor='blue',capsize=0)
    ax[1,0].set_xticks(range(0,5))
    ax[1,0].set_xticklabels(dim1_str)
    ax[1,0].set_ylabel("$Mean$")
    for tick in ax[1,0].get_xticklabels():
        tick.set_rotation(45)

    # plot random and user-specified model
    out = list(); out.append(X)
    for i, mdl in enumerate(mdl_spc):
        mdl_noise = mat2grid(addnoise(mdl))
        out.append(mdl_noise)
        pl = ax[0,i+1].pcolormesh(mdl_noise,cmap = plt.cm.Spectral_r,edgecolor='k',shading='gouraud')
        ax[0,i+1].axis('image')
        ax[0,i+1].set_title(mdl_strs[i])
        ax[0,i+1].set_xticks(range(0,5))
        ax[0,i+1].set_xticklabels(dim1_str)
        ax[0,i+1].set_yticks([0.5,3.5])
        ax[0,i+1].set_yticklabels(dim2_str)
        for tick in ax[0,i+1].get_xticklabels():
            tick.set_rotation(45)
            divider = make_axes_locatable(ax[0,i+1])
            cax = divider.append_axes("right", size="5%", pad=0.05)
            cbar = fig.colorbar(pl,cax=cax)
        dat = list()
        for ii in range(n):
            Y = mat2grid(addnoise(mdl))
            dat.append(geom_dist_mat(X,Y))
        dat = np.asarray(dat)
        # write simulation data to file
        np.savetxt("{}_{}_simulation.txt".format(outname.split(".")[0],mdl_strs[i].replace(" ","_").lower()),dat)
        # histograms for simualtions
        mu, std = norm.fit(dat)
        # Plot the histogram.
        ax[1,i+1].hist(dat, bins=25, density=True, alpha=0.6, color='r')

        # Plot the PDF.
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 1000)
        p = norm.pdf(x, mu, std)
        ax[1,i+1].plot(x, p, 'b', linewidth=2)
        ax[1,i+1].set_xlim([mu-.1,mu+.1])
        ax[1,i+1].set_xlabel("$\delta(data,model)$\n$\mu = %.2f,\sigma^2 = %.2f$" % (mu, std))

    # write matrices to file
    with open(outname, 'w') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerows(out)

    # write visualiation to file
    plt.savefig(filename)

def main():
    # visualiation parameters
    mpl.rcParams.update({'text.usetex': False,
                        'font.family': 'serif',
                        'font.serif': 'cmr10',
                        'font.weight':'bold',
                        'mathtext.fontset': 'cm',
                        'axes.unicode_minus'  : False
                        })

    ## data
    fname = "dat/response.csv"
    df = pd.read_csv(fname)

    ## items
    items = pd.read_csv("dat/items_expand.csv")

    ### embedded items indices
    init_idxs = [5, 11]
    for i in tqdm(init_idxs):
        ii = (i + 4) + 1
        q_str = items["Short-form"].iloc[i]

        ### data dataframe
        M = np.array(df.iloc[:,i:ii])

        ### specification of comparison model
        mdl_max = [1,1,5,5,5]
        mdl_med = [1,3,3,3,2]
        mdl_min = [5,1,1,1,1]
        MDLS = [mdl_max,mdl_med,mdl_min]
        MDLS_labels = ["yeswecan","bland","nighmare"]

        for j, mdl in enumerate(MDLS):
            fname = "{}_{}".format(re.sub(" ","",q_str.lower()),MDLS_labels[j])
            mdl2plot(M,mdl,q_str,filename="fig/{}.png".format(fname),outname="dat/export/{}.txt".format(fname))

if __name__ == '__main__':
    main()
