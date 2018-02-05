###cluster.py
import scipy
import scipy.cluster.hierarchy as sch
from scipy.cluster.vq import vq,kmeans,whiten
import numpy as np
import matplotlib.pylab as plt
from sklearn.decomposition import PCA


def  kmeans_with_hierachical_clustering(points):
    '''
     perform kmeans over multi-dimensional points
    :param points: N*F [n_samples,n_features]
    :return:
    '''
    #calculate distance
    disMat = sch.distance.pdist(points,'euclidean')
    #hierachical clustering:
    Z=sch.linkage(disMat,method='average')
    cluster= sch.fcluster(Z, t=1, criterion='inconsistent')

    print "Original cluster by hierarchy clustering:\n",cluster

    #2. k-means
    data=whiten(points)
    centroid=kmeans(data,max(cluster))[0]

    label=vq(data,centroid)[0]

    print "Final clustering by k-means:\n",label

    return  label


def pca_decompostion(data,n_components,if_copy=True,if_whiten=False):
    pca=PCA(n_components=n_components, copy=if_copy, whiten=if_whiten)
    newData = pca.fit_transform(data)
    return  newData,pca