import csv
import random
import math
from bson.son import SON
import requests
from flask import Flask, request,redirect,url_for
from flask_pymongo import PyMongo
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

app.config['MONGO_DBNAME'] = 'BMC'

mongo = PyMongo(app)


class Hostname(Resource):

	def get(self):
		var=mongo.db.CurrentLoad.distinct('hostname')
	
		for doc in var:
	
			print doc
			r = requests.get('http://127.0.0.1:5002/retrieve/%s'% (doc))
			
		return "Ok"

api.add_resource(Hostname, '/hostname')

if __name__ == '__main__':
    app.run(debug=True,port=5004)
