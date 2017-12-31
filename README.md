# Auto-Scaling-of-Application-Servers
This project demonstrates the automatic spawning of an application server (Upscaling) in cases of consistent heavy server load (eg: Heavy load on Amazon servers during festives seasons and flash sale)

Using the methodology of micro-service architecture and Flask Interface, micro-services were written.
These micro-services were used to fetch real time data (CPU Load, Swap usage, Root Partition etc.) from Nagios Monitoring Tool, to generate a machine learning model, to analyze the data, to spawn a new server (in cases of consistent high load on server) and to notify the administrator via email or text message.     
Technologies used: Amazon Web Services, Machine Learning, Python 2.7, Nagios Monitoring Tool, Flask Interface, Micro-service Architecture, MongoDB.

Project Demo Link: https://goo.gl/8cmD3B 
