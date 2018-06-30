import numpy as np
from scipy.spatial import distance


np.set_printoptions(suppress=True)
newInp = np.loadtxt("current_attempt.txt", dtype='f', delimiter=',')
training = np.loadtxt("training_test123_gha.txt", dtype='f', delimiter=',')

meantrain= training.mean(axis=0)

for row in newInp:
  print "row" . row
  print "mean" . meantrain
  print "euclidean {}".format(distance.euclidean(row,meantrain))


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
