import numpy as np
from scipy.spatial import distance


np.set_printoptions(suppress=True)
newInp = np.loadtxt("current_attempt.txt", dtype='f', delimiter=',')
training = np.loadtxt("training_data.txt", dtype='f', delimiter=',')

meantrain= training.mean(axis=0)

for row in newInp:
  print "euclidean {}".format(distance.euclidean(row,meantrain))


