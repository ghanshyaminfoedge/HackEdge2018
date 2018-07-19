#!flask/bin/python
from flask import Flask
import numpy as np
from scipy.spatial import distance
from flask import request


def mahalanobis(userName,keyPass):
	np.set_printoptions(suppress=True)
	newInp = np.loadtxt("/data/current_attempt_"+userName+"_"+keyPass+".txt", dtype='f', delimiter=',')
	training = np.loadtxt("/data/training_"+userName+"_"+keyPass+".txt", dtype='f', delimiter=',')
	np.absolute(newInp)
	np.absolute(training)
	meantrain= training.mean(axis=0)
	cov = np.cov(training.T)
	invcov = np.linalg.inv(cov)
	row = newInp	
	u = distance._validate_vector(newInp.mean(axis=0))
	v = distance._validate_vector(meantrain)
	VI = np.atleast_2d(invcov)
	delta = u - v
	m = np.dot(np.dot(delta, VI), delta)
	m = np.absolute(m)
	result = np.sqrt(m)
	print(result)
	# number of keystroke
	normalizedRes = training.shape[0]/3 
	maxScore = 5000
	percentage = (normalizedRes*100)/maxScore
	return (100-percentage)

mahalanobis("ghan","ghan")
