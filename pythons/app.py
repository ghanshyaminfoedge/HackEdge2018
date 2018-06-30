#!flask/bin/python
from flask import Flask
import numpy as np
from scipy.spatial import distance
from flask import request
import sklearn
from sklearn.cluster import DBSCAN
import math

app = Flask(__name__)


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


def isValid(username,keypass):
	res = euclieanDis("/data/training_"+username+"_"+keypass+".txt","/data/training_"+username+"_"+keypass+".txt")
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
	resnew= euclieanDis("/data/current_attempt_"+username+"_"+keypass+".txt","/data/training_"+username+"_"+keypass+".txt")
	newstd=np.std(np.asarray(clust))
	newmean=np.mean(np.asarray(clust))
	print "resnew {} newstd {} newmean {}".format(resnew,newstd,newmean)
	thresoldpos = newmean+newstd*1.5 
	thresoldnew = newmean-newstd*1.5
	if np.mean(resnew) > thresoldpos or np.mean(resnew) < thresoldnew:
		return 0
	return 1


@app.route('/keystroke/api/score', methods=['GET'])
def getScore():
	res = isValid(request.args.get('userName'), request.args.get('keyPass'))
	print "result ============ {}".format(res)
	return str(int(res))

if __name__ == '__main__':
    app.run(debug=True)

