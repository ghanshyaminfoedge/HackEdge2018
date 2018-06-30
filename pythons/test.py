import numpy as np
from scipy.spatial import distance
def weightify(newInp):
        weighted = []
        for row in newInp:
            weighted.append(addWeights(row))

def addWeights(newInp):
	print newInp
        i = 0
        while i < len(newInp):
            newInp = newInp(i*5)
            newInp = newInp((i+1)*3)
            newInp = newInp((i+2)*2)
            i = i + 3

np.set_printoptions(suppress=True)
newInp = np.loadtxt("/data/current_attempt_test123_test123.txt", dtype='f', delimiter=',')
training = np.loadtxt("/data/training_test123_test123.txt", dtype='f', delimiter=',')
#wTraining = weightify(training)
#print(training)

#       newInp = np.loadtxt("/data/current_attempt_"+userName+"_"+keyPass+".txt", dtype='f', delimiter=',')
#       training = np.loadtxt("/data/training_"+userName+"_"+keyPass+".txt", dtype='f', delimiter=',')
np.absolute(newInp)
np.absolute(training)
meantrain= training.mean(axis=0)
meansize=meantrain.shape[0]
weight = list()
for i in range (meansize):
	weight.append(5)
        weight.append(4)
	weight.append(3)

we = np.asarray(weight)
print "euclidean {}".format(distance.euclidean(newInp,meantrain,we))
#cov = np.cov(training.T)
#invcov = np.linalg.inv(cov)
#print invcov
#row = newInp
#u = distance._validate_vector(row)
#v = distance._validate_vector(meantrain)
#VI = np.atleast_2d(invcov)
#delta = u - v
#m = np.dot(np.dot(delta, VI), delta)
#m = np.absolute(m)
#print "mahalanobis {}".format(np.sqrt(m))
#  m = np.dot(np.dot(row, meantrain), (row-meantrain))
#  print "mahalanobis {}".format(np.sqrt(np.absolute(m).mean(axis=0)))
#  print "euclidean {}".format(distance.euclidean(row,meantrain))

#    u = _validate_vector(u)
#    v = _validate_vector(v)
#    VI = np.atleast_2d(VI)
#    delta = u - v
#    m = np.dot(np.dot(delta, VI), delta)
#    return np.sqrt(m)
#tracov= np.cov(training.T)
#incov = np.linalg.inv(tracov)
#print newInp;
#meantrain= training.mean(axis=0)

#print distance.mahalanobis(meantrain,newInp,incov)
#print meantrain
#print "euclidean {}".format(distance.euclidean(newInp,meantrain))
#print "canberra {}".format(distance.canberra(newInp,meantrain))
#print "hamming {}".format(distance.canberra(newInp,meantrain))
#delta = meantrain - newInp
#m = np.dot(np.dot(delta, incov), delta)
#np.sqrt(m*-1)
