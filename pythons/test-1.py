import numpy as np
from scipy.spatial import distance
import sklearn
from sklearn.cluster import DBSCAN
import math


np.set_printoptions(suppress=True)
newInp = np.loadtxt("current_attempt.txt", dtype='f', delimiter=',')
training = np.loadtxt("training_test123_gha.txt", dtype='f', delimiter=',')

np.absolute(newInp)
np.absolute(training)
meantrain= training.mean(axis=0)
meansize=(meantrain.shape)[0]/3
weight = list()
print meansize
for i in range (meansize):
	weight.append(50)
        weight.append(20)
	weight.append(40)
weight.append(50)

we = np.asarray(weight)
print we
print we.shape
print newInp.shape
print meantrain.shape

res = list()
for row in newInp:
	curres = distance.euclidean(row,meantrain,we);
	res.append(curres)
	print "euclidean {}".format(curres)

dbinput = np.asarray(res)
dbinput = [[x,1] for x in dbinput]
print dbinput
stdv = math.ceil(np.std(dbinput))
print stdv
model  = DBSCAN(eps=int(stdv), min_samples=3).fit(dbinput)
print model.labels_

clust = list()
i=0
for row in model.labels_:
	if row == 0 : 
		clust.append(res[i])
	i=i+1

print clust
