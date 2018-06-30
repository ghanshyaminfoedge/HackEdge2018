import numpy as np
from scipy.spatial import distance
np.set_printoptions(suppress=True)
newInp = np.loadtxt("current_attempt.txt", dtype='f', delimiter=',')
training = np.loadtxt("training_data.txt", dtype='f', delimiter=',')

#tracov= np.cov(training.T)
#incov = np.linalg.inv(tracov)

meantrain= training.mean(axis=0)

#print distance.mahalanobis(meantrain,newInp,incov)
print meantrain
print "euclidean {}".format(distance.euclidean(newInp,meantrain))
#delta = meantrain - newInp
#m = np.dot(np.dot(delta, incov), delta)
#np.sqrt(m*-1)
