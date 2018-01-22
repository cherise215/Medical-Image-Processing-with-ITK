###cluster.py
#导入相应的包
import scipy
import scipy.cluster.hierarchy as sch
from scipy.cluster.vq import vq,kmeans,whiten
import numpy as np
import matplotlib.pylab as plt


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

    #使用vq函数根据聚类中心对所有数据进行分类,vq的输出也是两维的,[0]表示的是所有数据的label
    label=vq(data,centroid)[0]

    print "Final clustering by k-means:\n",label

    return  label