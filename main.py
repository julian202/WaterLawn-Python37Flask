# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_render_template]
'''
import datetime
from darksky import forecast
from datetime import date, timedelta
from datetime import datetime as dt
'''
from flask import Flask, render_template
import requests
from pprint import pprint
app = Flask(__name__)


def getData(url, date):
	endPoint = url + "," + str(date) + "?exclude=currently,flags,hourly"
	r = requests.get(endPoint)
	jsondata = r.json()
	#pprint(jsondata["daily"])
	return 24 * jsondata["daily"]["data"][0]["precipIntensity"]

@app.route('/')
def root():
	url = "https://api.darksky.net/forecast/8b19ff2840cd837d214d2bfce73426b8/34.277215,-77.836957"
	'''
		t = dt(2018, 10, 28, 1)
		#t = dt(2018, 11, 4, 1).isoformat()
		day = timedelta(days=1)
		t_minus1 = (t-day).isoformat()
	'''
	date = 1540732849
	day = 24 * 60 * 60
	dateMinus1 = date - day
	dateMinus2 = date - 2*day
	dateMinus3 = date - 3*day
	dateMinus4 = date - 4*day
	a = getData(url, date)
	b = getData(url, dateMinus1)
	c = getData(url, dateMinus2)
	d = getData(url, dateMinus3)
	e = getData(url, dateMinus4)
	a = "{:.2f}".format(a)
	b = "{:.2f}".format(b)
	c = "{:.2f}".format(c)
	d = "{:.2f}".format(d)
	e = "{:.2f}".format(e)
	# For the sake of example, use static information to inflate the template.
	# This will be replaced with real information in later steps.
	dummy_times = [a, b, c, d, e]
	return render_template('index.html', times=dummy_times)

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
