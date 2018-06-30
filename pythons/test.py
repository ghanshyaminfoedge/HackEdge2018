import numpy as np
from scipy.spatial import distance
import sklearn
from sklearn.cluster import DBSCAN
import math


def euclieanDis(currentfile, trainfile):
	np.set_printoptions(suppress=True)
	newInp = np.loadtxt(currentfile, dtype='f', delimiter=',')
	training = np.loadtxt(trainfile, dtype='f', delimiter=',')
	
	np.absolute(newInp)
	np.absolute(training)
	meantrain= training.mean(axis=0)
	meansize=(meantrain.shape)[0]/3
	weight = list()
	for i in range (meansize):
		weight.append(50)
	        weight.append(20)
		weight.append(40)
	weight.append(50)
	
	we = np.asarray(weight)
	
	res = list()
	for row in newInp:
		curres = distance.euclidean(row,meantrain,we);
		res.append(curres)
	return res
res = euclieanDis("training_test123_gha.txt","training_test123_gha.txt")
dbinput = np.asarray(res)
dbinput = [[x,1] for x in dbinput]
stdv = math.ceil(np.std(dbinput))
model  = DBSCAN(eps=int(stdv), min_samples=3).fit(dbinput)

clust = list()
i=0
for row in model.labels_:
	if row == 0 : 
		clust.append(res[i])
	i=i+1
resnew= euclieanDis("current_attempt.txt","training_test123_gha.txt")

newstd=np.std(np.asarray(clust))
newmean=np.mean(np.asarray(clust))
print resnew
