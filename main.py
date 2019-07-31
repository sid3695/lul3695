from flask import Flask, render_template, url_for, session, request, redirect

from flask_sqlalchemy import SQLAlchemy
import os
import json

#project_dir = os.path.dirname(os.path.abspath(__file__))
#database_file = "sqlite:///{}".format(os.path.join(project_dir, "events.db"))




app = Flask(__name__)



from datetime import datetime
import time
#app.secret_key = "test"
#app.config["SQLALCHEMY_DATABASE_URI"] = database_file

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from models import *
from utils import *

#db.drop_all()
#db.create_all()

#@app.route('/')
#def hello_world():
#    return render_template("index.html")

@app.route('/logout',methods = ['GET', 'POST'])
def logout():
	if is_logged_in():
		del session['empId']
	return redirect(url_for("signup"))

@app.route('/', methods = ['GET', 'POST'])
def signup():
	if request.method == 'POST':
		#if entered
		#check if already, no need to create
		if is_logged_in():
			print(session['empId'])
			empId = session['empId']
			return redirect(url_for("landing", empId = empId))
		if user_exists_db(request.form['empId']):
			print("Signup : Existing user")
			user_login(request.form['empId'])
			empId = session['empId']
			return redirect(url_for("landing", empId = empId))
			#return render_template("signup.html", flag = 2)

		#otherwise create
		else:
			print("Signup : New user")
			create_new_user_db(request.form['name'], request.form['empId'])
			#log in the user/session
			user_login(request.form['empId'])
			empId = session['empId']
			return redirect(url_for("landing", empId = empId))
	else:
		#landing on page
		if is_logged_in():
			print(session['empId'])
			empId = session['empId']
			return redirect(url_for("landing", empId = empId))
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
		userObj = user_search_by_empid_db(empId)

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
		userObj = user_search_by_empid_db(empId)
		#useroj = username and empid
		
		datefromDB = (Date.query.filter_by(emp_id = empId, date = datetime(int(year),int(month),int(date)).date()).first())

		timetable = {
		}
		#sort dayData.events and arrange into 24 hours
		for i in range(0,25):
			timetable[i] = [];
		print(timetable)
		try:
			dayIdfromDB = datefromDB.day_id
		except:
			dayIdfromDB = -1
		print("day id " + str(dayIdfromDB) + "of emp " + str(empId))
		

		#devices = (Devices.query.filter_by(emp_id = empId).all())
		#fixed
		devices = ["Living Room Speaker", "Bed Room Speaker", "Living Room TV", "Bed Room TV", "Family Hub", "Mobile", "Living Room AC", "Bed Room AC"]


		eventsfromDB = Events.query.filter_by(day_id  = dayIdfromDB)
		print("ithe")
		for i in eventsfromDB:
			convTime = i.timestamp
			print("LOL")
			print(convTime)
			tempStr = {
			"timestamp" : convTime.strftime('%H:%M'),
			"eventId": i.event_id,
            "action": i.action,
            "value": i.value,
            "devicename_source": i.devicename_source,
            "devicename_dest": i.devicename_dest
			}
			timetable[convTime.hour].append(tempStr)
		
		scenarios = [
                         "Search <content name> on youtube.com",
						"Search <product name> on amazon.com",
						"Play <music name>",
						"Play <movie name>",
						"Search <recipe name>",
						"Search <movie name>",
						"Search <tv show name>",
						"Search <sports match name>",
						"Show me the weather for <day or date or time>",
						"Increase the brightness",
						"Show me the camera stream",
						"Show me inside of refrigerator"

		]

		literal_times = ["12 AM", "1 AM", "2 AM", "3 AM", "4 AM", "5 AM", "6 AM", "7 AM", "8 AM", "9 AM", "10 AM", "11 AM", "12 PM", "1 PM", "2 PM", "3 PM", "4 PM", "5 PM", "6 PM", "7 PM", "8 PM", "9 PM", "10 PM", "11 PM", "12 AM"]
		print(timetable)
		print('ssdsd ' + literal_times[5])
		literal_times_pass = {}
		#sort all arrays
		for i in range(0,25):
			#sort each
			templist = []
			if(i<24):
				slot_string = literal_times[i]+"- "+literal_times[i+1]
				literal_times_pass[i] = slot_string
			templist = sorted(timetable[i], key=lambda k: k['timestamp'])
			timetable[i] = templist
		print(timetable)
		print(literal_times_pass)
		return render_template("date2.html", year = year, month= month, date = date, scenarios = scenarios, literal = literal_times_pass , timetable = timetable, dayId = dayIdfromDB, devices = devices)
	else:
		return redirect(url_for("signup"))


@app.route('/addevent/<dayId>/<year>/<month>/<date>', methods = ['GET', 'POST'])
def addevent(dayId, year, month, date):
	#pick username from session
	#return "henlo" + request.form['timestamp'] + request.form['value'] + request.form['action'] + request.form['devicename']
	if is_logged_in():

		#for that day_id make an entry
		print(Date.query.filter_by(day_id = dayId).all())
		if request.method == "POST":
			#handle addition to json
			'''newEvent = {
			'action' : request.form["action"],
			'devicename' : request.form["devicename"],
			'timestamp' : request.form['timestamp'],
			'value': request.form['value'],
			'eventId' : dayData['eventIndex']
			}'''
			#check if daydata
			#if yes then add event




			if Date.query.filter_by(day_id = dayId).first():
				print("YAHA")
				if(request.form["action"]):
					#create on-off
					timestr = request.form["hrs"]+":"+request.form["mins"]
					newEvent = Events(day_id = dayId, action = request.form["action"], devicename_source = request.form["devicename_source"], devicename_dest = request.form["devicename_dest"],value = "on",timestamp =  datetime.strptime(timestr,'%H:%M').time())
					db.session.add(newEvent)
					db.session.commit()
					# newEvent = Events(day_id = dayId, action = request.form["action"] + "_off", devicename_source = request.form["devicename_source"], devicename_dest = request.form["devicename_dest"], value= request.form['value'],timestamp =  datetime.strptime(request.form['timestamp2'],'%H:%M').time())
					# db.session.add(newEvent)
					# db.session.commit()
				# else:
				# 	newEvent = Events(day_id = dayId, action = "color", devicename = request.form["devicename"], value= request.form['value'],timestamp =  datetime.strptime(request.form['timestamp'],'%H:%M').time())
				# 	db.session.add(newEvent)
				# 	db.session.commit()
			else:
				#-1 comes here
				#create date
				print('here')
				newDate = Date(emp_id = session['empId'], date = datetime(int(year),int(month),int(date)).date()) 
				db.session.add(newDate)
				db.session.commit()
				print(newDate)
				if request.form["action"]:
					timestr = request.form["hrs"]+":"+request.form["mins"]
					newEvent = Events(day_id = newDate.day_id, action = request.form["action"], devicename_source = request.form["devicename_source"], devicename_dest = request.form["devicename_dest"], value= "on",timestamp =  datetime.strptime(timestr,'%H:%M').time())
					db.session.add(newEvent)
					db.session.commit()
					# newEvent = Events(day_id = newDate.day_id, action = request.form["action"] + "_off", devicename_source = request.form["devicename_source"], devicename_dest = request.form["devicename_dest"], value= request.form['value'],timestamp =  datetime.strptime(request.form['timestamp2'],'%H:%M').time())
					# db.session.add(newEvent)
					# db.session.commit()
				# else:
				# 	newEvent = Events(day_id = newDate.day_id, action = "switch", devicename = request.form["devicename"], value= request.form['value'],timestamp =  datetime.strptime(request.form['timestamp'],'%H:%M').time())
				# 	db.session.add(newEvent)
				# 	db.session.commit()

				

			return redirect(url_for("landingdate",year = year, month = month, date= date))
		else:
			#display form
			return "henlo"
			return render_template("addevent.html", day = day)
	else:
		return redirect(url_for("signup"))

@app.route('/delevent/<eventId>/<year>/<month>/<date>', methods = ['GET', 'POST'])
def delevent(eventId, year, month, date):
	if is_logged_in():
		#check if event user_exists
		event = Events.query.filter_by(event_id = eventId).first()
		if event:
			db.session.delete(event)
			db.session.commit()
		else:
			print("notvalid")
		return redirect(url_for("landingdate",year = year, month = month, date= date))

@app.route('/devicedetails', methods = ['GET', 'POST'])
def devicedetails():
	if is_logged_in():
		empId = session['empId']
		x = User.query.filter_by(emp_id = empId).first()
		if x.first_login:
			if request.method == "POST":
				#set user login default
				
				if x.first_login == True:
					x.first_login = False	
					db.session.commit()
				#all devices in db
				if request.form["name"]:
					dname = Devices(emp_id = empId, devicename = request.form["name"])
					db.session.add(dname)
				for i in range(0,20):
					if "name" + str(i) in request.form:
						dname = Devices(emp_id = empId, devicename = request.form["name" + str(i)])
						db.session.add(dname)
				db.session.commit()

				return redirect(url_for("landing", empId = empId))
			else:
				return render_template("devicedetails.html")
		else:
			return redirect(url_for("landing", empId = empId))
	else:
		return 'henlo'

@app.route('/userdump')
def userdump():
	q = db.session.query(User,Date,Events).join(Date).join(Events).order_by(Date.date).order_by(Events.timestamp).all()
	#qq = db.session.query(Events).join(q, Events.day_id == q.day_id)
	#print (qq.all())
	user_dict = {}
	for i in q:
		val = str(i.Date.date) + "," + str(i.Events.timestamp) + "," + i.Events.action + "," + i.Events.devicename_source + "," + i.Events.devicename_dest + ","
		val1 = {
		"date" : str(i.Date.date),
		"timestamp" : str(i.Events.timestamp),
		"scenario" : i.Events.action,
		"source device" : i.Events.devicename_source,
		"dest device" : i.Events.devicename_dest
		}
		if i.User.emp_id in user_dict:
			user_dict[i.User.emp_id].append(val1)
		else:
			user_dict[i.User.emp_id] = [val1]
	print(user_dict)
	return json.dumps(user_dict,indent=4, sort_keys=True)

@app.route('/drag')
def drag():
	return render_template("drag.html")


@app.route('/dbreset')
def dbreset():
	db.drop_all()
	db.create_all()
	if is_logged_in():
		del session['empId']
	return 'db reset done'
if __name__ == '__main__':
    app.run()