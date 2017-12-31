from flask import Flask, request
from flask_pymongo import PyMongo
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)
app.config['MONGO_DBNAME'] = 'BMC'

mongo = PyMongo(app)

parser = reqparse.RequestParser()
parser.add_argument('serviceOutput', type=str)
parser.add_argument('hostName', type=str)
parser.add_argument('serviceDesc', type=str)


class Insert(Resource):
    def get(self):
        return 'OK'

    def post(self):
	args = parser.parse_args()
        #if args['hostName']=='vm':
	if args['serviceDesc']=="Current Load":
			thisline=args['serviceOutput'].split(" ")
			mongo.db.CurrentLoad.insert({'hostname':args['hostName'],'Current_Load':{'load1':float(thisline[4].replace(",","")),'load5':float(thisline[5].replace(",","")),'load15':float(thisline[6].replace("OK",""))}})
		    
	elif args['serviceDesc']=="Root Partition":
			thisline=args['serviceOutput'].split(" ")
			mongo.db.RootPartition.insert({'hostname':args['hostName'],"Disk Space Avaliable":thisline[6]})
		    
	elif args['serviceDesc']=="Swap Usage":
			thisline=args['serviceOutput'].split(" ")
			mongo.db.SwapUsage.insert({'hostname':args['hostName'],'Swap_Usage':thisline[3].replace("%","")})

	elif args['serviceDesc']=="Total Processes":
			thisline=args['serviceOutput'].split(" ")
			mongo.db.TotalProcesses.insert({'hostname':args['hostName'],'Total_Processes':int(thisline[2])})
	return 'OK'

api.add_resource(Insert, '/nagios')



if __name__ == '__main__':
    app.run(debug=True,port=5000)
