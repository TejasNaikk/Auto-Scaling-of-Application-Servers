
from bson.son import SON
import requests
from flask import Flask, request,redirect,url_for
from flask_pymongo import PyMongo
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

app.config['MONGO_DBNAME'] = 'BMC'

mongo = PyMongo(app)
class Retrieve(Resource):

	def get(self,hostname):

	    pipe=[{'$sort':SON({"_id":-1})},{'$match':{'hostname':hostname}},{'$limit':2},{'$group':{'_id':"$hostname",'total': {'$avg':"$Current_Load.load1"}}},{'$match':{'_id':hostname}}]
	    pipe1=[{'$sort':SON({"_id":-1})},{'$limit':2},{'$group':{'_id':"$hostname",'total': {'$avg':"$Swap_Usage"}}}]
	    pipe2=[{'$sort':SON({"_id":-1})},{'$limit':2},{'$group':{'_id':"$hostname",'total': {'$avg':"$Total_Processes"}}}]

	    load1_average=mongo.db.CurrentLoad.aggregate(pipeline=pipe)
	    swap_usage_average=mongo.db.SwapUsage.aggregate(pipeline=pipe1)
	    total_processes_average=mongo.db.TotalProcesses.aggregate(pipeline=pipe2)
	   
	    for doc in load1_average:
	    	temp=doc[u'total']
	    """for doc in swap_usage_average:
	    	print(doc[u'total'])
	    for doc in total_processes_average:
	    	temp1=doc[u'total']	
	   """ 
	    #return redirect(url_for('/analysis',mean1=temp,mean2=temp1))
	    r = requests.get('http://127.0.0.1:5001/analysis/%f/%s'% (temp,hostname) )
	    return "Ok"

api.add_resource(Retrieve, '/retrieve/<string:hostname>')

if __name__ == '__main__':
    app.run(debug=True,port=5002)
