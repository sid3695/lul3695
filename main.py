from flask import Flask, render_template, url_for, session, request, redirect
app = Flask(__name__)

from utils import *
from datetime import datetime
import time
app.secret_key = "test"

#@app.route('/')
#def hello_world():
#    return render_template("index.html")


@app.route('/', methods = ['GET', 'POST'])
def signup():
	if request.method == 'POST':
		#if entered
		#check if already, no need to create
		if user_exists(request.form['empId']):
			print("Signup : Existing user")
			user_login(request.form['empId'])
			return redirect(url_for("landing", empId = request.form['empId']))
			#return render_template("signup.html", flag = 2)

		#otherwise create
		else:
			print("Signup : New user")
			create_new_user(request.form['name'], request.form['empId'])
			#log in the user/session
			user_login(request.form['empId'])
			return redirect(url_for("landing", empId = request.form['empId']))
	else:
		#landing on page
		return render_template("signup.html", flag = 0)

#@app.route('/login', methods = ['GET', 'POST'])
#def login():
#	print("login" + test())
#
#	if request.method == 'POST':
#		#if entered
#		#check if already
#		if user_exists(request.form['name']):
#			user_login(request.form['name'])
#			return redirect(url_for("landing", name = request.form['name']))
#		else:
#			#log in the user/session
#			return render_template("login.html", flag = 2)
#	else:
#		#landing on page
#		return render_template("login.html", flag = 0)


@app.route('/landing/<empId>',methods = ['GET', 'POST'])
def landing(empId):
	if is_logged_in():
		userObj = user_search_by_empid(empId)
		print (userObj)
		if request.method == "GET":
			return render_template("landing.html", name = userObj['username'], userObj = userObj)
		else:
			#POST
			#redirect
			#print(request.form['dayNumber'])
			#return "5"
			return redirect(url_for("daynumber", day = request.form['dayNumber']))
	else:
		return redirect(url_for("signup"))

@app.route('/landing/date/<year>/<month>/<date>',methods = ['GET', 'POST'])
def landingdate(year, month, date):
	if is_logged_in():
		empId = session['empId']
		userObj = user_search_by_empid(empId)
		#print (userObj)
		eventList = []
		dayData = {}
		print(userObj['dayData'])
		for i in userObj['dayData']:
			if(datetime(int(year),int(month),int(date)).date() == datetime.strptime(i['date'], '%Y-%m-%d').date()):
				#entry found
				dayData = i
				print(i)
				break
			else:
				print("GLGLLG")
		timetable = {
		}
		#sort dayData.events and arrange into 24 hours
		for i in range(0,25):
			timetable[i] = [];
		print(timetable)
		try:
			for i in dayData['events']:
				#print(i)
				convTime = (datetime.strptime(i['timestamp'], "%H:%M").time())
				tempStr = {
				"timestamp" : convTime,
				"eventId": i['eventId'],
                "action": i['action'],
                "value": i['value'],
                "devicename": i['devicename']
				}
				print (tempStr)
				#TO ADD BOUNDARY CHECK
				timetable[convTime.hour].append(tempStr) 
		except:
			print("khaali")
		print(timetable)
		#sort all arrays
		for i in range(0,25):
			#sort each
			templist = []
			templist = sorted(timetable[i], key=lambda k: k['timestamp'])
			timetable[i] = templist
		print(timetable)
		return render_template("date.html", year = year, month= month, date = date, timetable = timetable)
	else:
		return redirect(url_for("signup"))

@app.route('/daynumber/<day>', methods = ['GET', 'POST'])
def daynumber(day):
	#pick username from session
	if is_logged_in():
		username = session['name']
		userObj = user_search_by_name(username)
		events = events_specific_day(userObj, day)
		return render_template("events.html", events = events, day = day, userObj = userObj)
	else:
		return redirect(url_for("login"))

@app.route('/addevent/<day>', methods = ['GET', 'POST'])
def addevent(day):
	#pick username from session
	if is_logged_in():
		username = session['name']
		userObj = user_search_by_name(username)
		events = events_specific_day(userObj, day)
		if request.method == "POST":
			#handle addition to json
			newEvent = {
			'action' : request.form["action"],
			'deviceId' : request.form["deviceId"],
			'timestamp' : "17-01-2019"
			}
			insert_event(userObj,day,newEvent)
			return redirect(url_for("daynumber", day = day))
		else:
			#display form
			print("here")
			return render_template("addevent.html", day = day)
	else:
		return redirect(url_for("login"))