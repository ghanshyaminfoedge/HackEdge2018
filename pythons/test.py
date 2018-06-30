import numpy as np
from scipy.spatial import distance


np.set_printoptions(suppress=True)
newInp = np.loadtxt("current_attempt.txt", dtype='f', delimiter=',')
training = np.loadtxt("training_test123_sona.txt", dtype='f', delimiter=',')
np.absolute(newInp)
np.absolute(training)
meantrain= training.mean(axis=0)
cov = np.cov(training.T)
invcov = np.linalg.inv(cov)
#print invcov
for row in newInp:
  u = distance._validate_vector(row)
  v = distance._validate_vector(meantrain)
  VI = np.atleast_2d(invcov)
  delta = u - v
  m = np.dot(np.dot(delta, VI), delta)
  m = np.absolute(m)
  print "mahalanobis {}".format(np.sqrt(m))
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
