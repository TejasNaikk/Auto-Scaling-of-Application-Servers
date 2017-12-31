#!/usr/bin/python
#from bson.son import SON
import requests
import boto.ec2
from flask import Flask, request,redirect,url_for
from flask_pymongo import PyMongo
from flask_restful import reqparse, abort, Api, Resource
import smtplib


app = Flask(__name__)
api = Api(app)

app.config['MONGO_DBNAME'] = 'BMC'

mongo = PyMongo(app)
class Email(Resource):
	def get(self,hostName):
		gmail_user =  'bsaautoscaling@gmail.com' 
		gmail_password = 'Magic@123456789'

		from1 = gmail_user  
		to = ['sarvanan91295@gmail.com']  
		subject = 'Autoscale'  
		body = hostName + ' health is low .Please spawn a new VM'

		email_text = """\  
		From: %s  
		To: %s  
		Subject: %s

		%s
		""" % (from1, ", ".join(to), subject, body)
		
		
		try:  
			server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
			server.ehlo()
			server.login(gmail_user, gmail_password)
			server.sendmail(from1, to, email_text)
			server.close()
			conn = boto.ec2.connect_to_region("ap-south-1",aws_access_key_id='AKIAI7IELWDQU3EYCUPQ',aws_secret_access_key='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')	
			print conn
			conn.run_instances('ami-ce3f4fa1',instance_type='t2.micro',key_name='test',security_groups=['launch-wizard-1'])
			print 'Email sent!'
			
		except Exception as e:  
			print 'Something went wrong'
			print e

api.add_resource(Email, '/email/<string:hostName>')


if __name__ == '__main__':
    app.run(debug=True,port=5003)
