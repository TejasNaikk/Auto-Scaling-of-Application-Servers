import csv
import random
import math
#from bson.son import SON
import requests
from flask import Flask, request,redirect,url_for
from flask_pymongo import PyMongo
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

app.config['MONGO_DBNAME'] = 'BMC'

mongo = PyMongo(app)

def loadCsv(filename):
	lines = csv.reader(open('/home/ubuntu/newdata.csv', "r"))
	dataset = list(lines)
	for i in range(len(dataset)):
		dataset[i] = [float(x) for x in dataset[i]]
	return dataset

def splitDataset(dataset, splitRatio):
	trainSize = int(len(dataset) * splitRatio)
	trainSet = []
	copy = list(dataset)
	while len(trainSet) < trainSize:
		index = random.randrange(len(copy))
		trainSet.append(copy.pop(index))
	return [trainSet, copy]

def separateByClass(dataset):
	separated = {}
	for i in range(len(dataset)):
		vector = dataset[i]
		if (vector[-1] not in separated):
			separated[vector[-1]] = []
		separated[vector[-1]].append(vector)
	return separated

def mean(numbers):
	return sum(numbers)/float(len(numbers))

def stdev(numbers):
	avg = mean(numbers)
	variance = sum([pow(x-avg,2) for x in numbers])/float(len(numbers)-1)
	return math.sqrt(variance)

def summarize(dataset):
	summaries = [(mean(attribute), stdev(attribute)) for attribute in zip(*dataset)]
	#print('Summaries: {0}%'.format(summaries))
	del summaries[-1]
	return summaries

def summarizeByClass(dataset):
	separated = separateByClass(dataset)
	#print('Separated: {0}'.format(separated.items()))
	summaries = {}
	for classValue, instances in separated.items():
		summaries[classValue] = summarize(instances)
      #  summaries={0.0: [(0.4035714285714286, 0.2387985035018546)], 1.0: [(0.687142857142857, 0.19328848791492878)]}     
	return summaries

def calculateProbability(x, mean, stdev):
	exponent = math.exp(-(math.pow(x-mean,2)/(2*math.pow(stdev,2))))
	return (1 / (math.sqrt(2*math.pi) * stdev)) * exponent

def calculateClassProbabilities(summaries, testSet):
	probabilities = {}
	#print('Summary: {0}%'.format(summaries.items()))
	for classValue, classSummaries in summaries.items():
		probabilities[classValue] = 1
		for i in range(len(classSummaries)):
			mean, stdev = classSummaries[i]
			x = testSet[i]
			probabilities[classValue] *= calculateProbability(x, mean, stdev)
	return probabilities
			
def predict(summaries, testSet):
	probabilities = calculateClassProbabilities(summaries, testSet)
	bestLabel, bestProb = None, -1
	for classValue, probability in probabilities.items():
		if bestLabel is None or probability > bestProb:
			bestProb = probability
			bestLabel = classValue
	return bestLabel

def getPredictions(summaries, testSet):
	predictions = []
	result = predict(summaries, testSet[0])
	predictions.append(result)
	return predictions

class Analysis(Resource):
	def get(self,mean,hostName):
			#mean1=request.args['mean1']
			#mean2=request.args['mean2']
			filename = 'newdata.csv'
			splitRatio = 1
			dataset = loadCsv(filename)
			trainingSet=dataset
			
				
			testSet=[[mean]]
			print mean;
			summaries = summarizeByClass(trainingSet)
			
			predictions = getPredictions(summaries, testSet)
			
			if(format(predictions)=='[0.0]'):
				#r = requests.get('http://127.0.0.1:5003/email')
				print('Prediction: {0}'.format(predictions))
				return 'Ok'
			else:
				r = requests.get('http://127.0.0.1:5003/email/%s'% (hostName))
				
				print('Prediction: {0}'.format(predictions))
				
				return 'not ok'

api.add_resource(Analysis, '/analysis/<float:mean>/<string:hostName>')
#api.add_resource(Analysis, '/analysis')


if __name__ == '__main__':
    app.run(debug=True,port=5001)

