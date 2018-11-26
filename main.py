# [START gae_python37_render_template]
'''
import datetime
from darksky import forecast
from datetime import date, timedelta
from datetime import datetime as dt
'''
from flask import Flask, render_template
import requests
import time
from pprint import pprint
import geoip2.database
from flask import request
from flask import jsonify
import json

#from google.cloud import storage

#reader = geoip2.database.Reader('/gs/waterlawn-222200.appspot.com/GeoLite2-City.mmdb')
#response = reader.city('128.101.101.101')

app = Flask(__name__)

def getWeather(lat, lon):
	#print("GOT WEATHER")
	url = "https://api.darksky.net/forecast/8b19ff2840cd837d214d2bfce73426b8/"+lat+","+lon
	global a,b,c,d,e,date,precip1,precip2,precip3,precip4,precip5
	date = int(time.time()) # 1540732849
	day = 24 * 60 * 60
	dateMinus1 = date - day
	dateMinus2 = date - 2*day
	dateMinus3 = date - 3*day
	dateMinus4 = date - 4*day	
	precip1 = getData(url, date)
	precip2 = getData(url, dateMinus1)
	precip3 = getData(url, dateMinus2)
	precip4 = getData(url, dateMinus3)
	precip5 = getData(url, dateMinus4)
	precip1 = "{:.2f}".format(precip1)
	precip2 = "{:.2f}".format(precip2)
	precip3 = "{:.2f}".format(precip3)
	precip4 = "{:.2f}".format(precip4)
	precip5 = "{:.2f}".format(precip5)
	
def getData(url, date):
	endPoint = url + "," + str(date) + "?exclude=currently,flags,hourly"
	#print("ENDPONT: " +endPoint)
	r = requests.get(endPoint)
	jsondata = r.json()
	#pprint(jsondata["daily"])
	return 24 * jsondata["daily"]["data"][0]["precipIntensity"]

@app.route('/', methods=["GET"])
def root():
	'''
	print('#######################1')
	yourIP = request.environ['REMOTE_ADDR']
	print(yourIP)
	print('#######################2')
	url = "https://api.darksky.net/forecast/8b19ff2840cd837d214d2bfce73426b8/34.277215,-77.836957"
	'''
	#precip = ['0.0', '0.0', '0.0', '0.0', '0.0']
	precip = ['-','-','-','-','-']
	return render_template('index.html', initialPrecip=precip)
	
@app.route('/ajax_info', methods=["GET"])
def rootajax():
	latitude = request.args.get('latitude')
	longitude = request.args.get('longitude')
	getWeather(latitude, longitude)
	return json.dumps({'a':precip1,'b':precip2,'c':precip3,'d':precip4,'e':precip5})

	
if __name__ == '__main__':
	# This is used when running locally only. When deploying to Google App
	# Engine, a webserver process such as Gunicorn will serve the app. This
	# can be configured by adding an `entrypoint` to app.yaml.
	# Flask's development server will automatically serve static files in
	# the "static" directory. See:
	# http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
	# App Engine itself will serve those files as configured in app.yaml.
	app.run(host='127.0.0.1', port=8080, debug=True)
# [START gae_python37_render_template]
