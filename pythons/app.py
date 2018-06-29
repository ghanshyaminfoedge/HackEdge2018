#!flask/bin/python
from flask import Flask
import numpy as np
from scipy.spatial import distance

app = Flask(__name__)



def euclDistance(): 
	np.set_printoptions(suppress=True)
	newInp = np.loadtxt("current_attempt.txt", dtype='f', delimiter=',')
	training = np.loadtxt("training_data.txt", dtype='f', delimiter=',')
	
	tracov= np.cov(training.T)
	incov = np.linalg.inv(tracov)
	meantrain= training.mean(axis=0)
	
	print meantrain
	return distance.euclidean(newInp,meantrain)



@app.route('/')
def index():
    res = euclDistance()
    return "{}".format(res)

if __name__ == '__main__':
    app.run(debug=True)

