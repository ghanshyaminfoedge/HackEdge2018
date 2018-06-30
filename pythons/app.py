#!flask/bin/python
from flask import Flask
import numpy as np
from scipy.spatial import distance
from flask import request

app = Flask(__name__)


def mahalanobis(userName,keyPass):
	print "{} {}".format(userName,keyPass)
	np.set_printoptions(suppress=True)
	newInp = np.loadtxt("current_attempt_"+userName+"_"+keyPass+".txt", dtype='f', delimiter=',')
	training = np.loadtxt("training_"+userName+"_"+keyPass+".txt", dtype='f', delimiter=',')
	np.absolute(newInp)
	np.absolute(training)
	meantrain= training.mean(axis=0)
	cov = np.cov(training.T)
	invcov = np.linalg.inv(cov)
	row = newInp	
	u = distance._validate_vector(row)
	v = distance._validate_vector(meantrain)
	VI = np.atleast_2d(invcov)
	delta = u - v
	m = np.dot(np.dot(delta, VI), delta)
	m = np.absolute(m)
	return np.sqrt(m)

@app.route('/keystroke/api/score', methods=['GET'])
def getScore():
	res = mahalanobis(request.args.get('userName'), request.args.get('keyPass'))
	print "result ============ {}".format(res)
	return str(int(res))

if __name__ == '__main__':
    app.run(debug=True)

