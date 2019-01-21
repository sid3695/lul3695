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
		if is_logged_in():
			print(session['empId'])
			return redirect(url_for("landing", empId = session['empId']))
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
		if is_logged_in():
			print(session['empId'])
			return redirect(url_for("landing", empId = session['empId']))
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
		dayId = i['dayId']
		print("dayIdDDDDDDDDDDD " + dayId)
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
		return render_template("date.html", year = year, month= month, date = date, timetable = timetable, dayId = dayId)
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

@app.route('/addevent/<dayId>/<year>/<month>/<date>', methods = ['GET', 'POST'])
def addevent(dayId, year, month, date):
	#pick username from session
	#return "henlo" + request.form['timestamp'] + request.form['value'] + request.form['action'] + request.form['devicename']
	if is_logged_in():
		empId = session['empId']
		userObj = user_search_by_empid(empId)

		#get to the user first
		dayData= {}
		#increment eventIndex
		for i in userObj['dayData']:
			if(i['dayId'] == dayId):
				dayData = i
				break
		currIndex = 0
		try:
			dayData['eventIndex'] = dayData['eventIndex'] + 1
			currIndex = dayData['eventIndex']
		except:
			print("new")
			currIndex = 1
		#events = events_specific_day(userObj, day)
		if request.method == "POST":
			#handle addition to json
			newEvent = {
			'action' : request.form["action"],
			'devicename' : request.form["devicename"],
			'timestamp' : request.form['timestamp'],
			'value': request.form['value'],
			'eventId' : dayData['eventIndex']
			}
			#insert_event(userObj,day,newEvent)
			events = []
			if currIndex > 1:
				for i in userObj['dayData']:
					if(i['dayId']==dayId):
						events = i['events']
						break
				events.append(newEvent)
				for i in userObj['dayData']:
					if(i['dayId'] == dayId):
						i['events'] = events


				#fill in events of daydata
				#userObj['dayData']
			else:
				str_date = year+ "-" + month+ '-' + date
				userObj['userData']['dayCount']= str(int(userObj['userData']['dayCount']) + 1)
				fillDay = {
				'dayId' : currIndex,
				'date' : str_date,
				'eventIndex' : currIndex,
				'events' : [newEvent
				]
				}
				userObj['dayData'].append(fillDay)

			data = []
			with open("data1.json") as f:
				data = json.load(f)
			for i in data:
				if i['empId'] == session['empId']:
					i = userObj

			with open("data1.json", "w") as f:
				json.dump(data,f,indent=4)

			return redirect(url_for("landingdate",year = year, month = month, date= date))
		else:
			#display form
			return "henlo"
			return render_template("addevent.html", day = day)
	else:
		return redirect(url_for("login"))