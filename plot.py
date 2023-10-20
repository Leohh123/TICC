import numpy as np
from matplotlib import pyplot as plt

import sys

x_all = np.loadtxt(sys.argv[1], delimiter=",")

nvar, nsample = x_all.shape[1], x_all.shape[0]
print(x_all.shape)


def plot_scatter():
    '''Check variable correlations'''
    figs, axes = plt.subplots(nrows=nvar, ncols=nvar)
    for i in range(nvar):
        for j in range(nvar):
            ax = axes[i, j]
            ax.scatter(x_all[:, i], x_all[:, j], marker='.', alpha=0.5)
            ax.set_xlim(-4, 4)
            ax.set_ylim(-4, 4)
    plt.show()


# plot_scatter()


def plot_cov_and_inv(x: np.ndarray, i_cluster):
    '''Plot covariance matrix and inverse covariance matrix'''
    # cov = (xhat.T @ xhat) / nsample
    cov = np.cov(x.T)
    print(cov)
    pos = plt.matshow(cov, cmap='seismic', vmin=-4, vmax=4)
    plt.colorbar(pos)
    plt.title(f'Cov cluster={i_cluster}')
    plt.show()

    inv = np.linalg.inv(cov)
    print(inv)
    pos = plt.matshow(inv, cmap='seismic', vmin=-4, vmax=4)
    plt.colorbar(pos)
    plt.title(f'Inv cluster={i_cluster}')
    plt.show()


# plot_cov_and_inv(x_all)


# Plot cov & inv_cov matrix for each cluster
params = dict(map(lambda eq: eq.split('='),
              sys.argv[1].split('_')[1].split('&')))
cluster_list = list(map(int, params['cl'].split(',')))
segment_samples = int(params['ss'])
clusters = len(set(cluster_list))
xlist_cl = [[] for _ in range(clusters)]
for i, cl in enumerate(cluster_list):
    xlist_cl[cl].append(x_all[i*segment_samples:(i+1)*segment_samples, :])
print(xlist_cl)
x_cl = [np.concatenate(l) for l in xlist_cl]
for i, x in enumerate(x_cl):
    plot_cov_and_inv(x, i)
