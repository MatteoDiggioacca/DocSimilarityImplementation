import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import umap
import copy
from sklearn.decomposition import PCA

def our_umap(Matrix):
    np.random.seed(42)
    data = copy.copy(Matrix)
    for i in range(len(data)):
        data[i] = list(data[i])
    fit = umap.UMAP(n_neighbors=2, metric = "jaccard")
    u = fit.fit_transform(data)
    return u

def pca_e_umap(Matrix):
    np.random.seed(42)
    data = copy.copy(Matrix)
    for i in range(len(data)):
        data[i] = list(data[i])
    pca = PCA(n_components=10)
    pca = pca.fit_transform(Matrix)
    fit = umap.UMAP(n_neighbors=2)
    u = fit.fit_transform(pca)
    return u

def print_umap(u, pdfs = [], path = "umap.pdf"):
    fig = plt.figure()
    #plt.scatter(u[:,0], u[:,1])
    fig, ax = plt.subplots()
    #ax.scatter(u[:, 0], u[:, 1], c=list(range(int(len(u)/2)))*2)
    ax.scatter(u[:, 0], u[:, 1])
    for i in range(len(pdfs)):
        ax.annotate(pdfs[i], (u[i,0], u[i,1]))
    #plt.show()
    fig.savefig(path)


def couples(u, distance = 0.2):
    list = []
    for i in range(len(u)):
        list.append((i,set()))
        for j in range(len(u)):
            if abs(u[i][0] - u[j][0]) < distance and abs(u[i][1] - u[j][1]) < distance and i != j:
                list[i][1].add(j)
    return list

