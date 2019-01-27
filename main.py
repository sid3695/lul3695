from flask import Flask, render_template, url_for, session, request, redirect

from flask_sqlalchemy import SQLAlchemy
import os


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
			return redirect(url_for("devicedetails"))
		if user_exists_db(request.form['empId']):
			print("Signup : Existing user")
			user_login(request.form['empId'])
			return redirect(url_for("devicedetails"))
			#return render_template("signup.html", flag = 2)

		#otherwise create
		else:
			print("Signup : New user")
			create_new_user_db(request.form['name'], request.form['empId'])
			#log in the user/session
			user_login(request.form['empId'])
			return redirect(url_for("devicedetails"))
	else:
		#landing on page
		if is_logged_in():
			print(session['empId'])
			return redirect(url_for("devicedetails"))
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
		

		devices = (Devices.query.filter_by(emp_id = empId).all())
		
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
            "devicename": i.devicename
			}
			timetable[convTime.hour].append(tempStr)
		

		print(timetable)
		#sort all arrays
		for i in range(0,25):
			#sort each
			templist = []
			templist = sorted(timetable[i], key=lambda k: k['timestamp'])
			timetable[i] = templist
		print(timetable)
		return render_template("date.html", year = year, month= month, date = date, timetable = timetable, dayId = dayIdfromDB, devices = devices)
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
				newEvent = Events(day_id = dayId, action = request.form["action"], devicename = request.form["devicename"], value= request.form['value'],timestamp =  datetime.strptime(request.form['timestamp'],'%H:%M').time())
				db.session.add(newEvent)
				db.session.commit()
			else:
				#-1 comes here
				#create date
				print('here')
				newDate = Date(emp_id = session['empId'], date = datetime(int(year),int(month),int(date)).date()) 
				db.session.add(newDate)
				db.session.commit()
				print(newDate)
				newEvent = Events(day_id = newDate.day_id, action = request.form["action"], devicename = request.form["devicename"], value= request.form['value'],timestamp =  datetime.strptime(request.form['timestamp'],'%H:%M').time())
				
				db.session.add(newEvent)
				db.session.commit()

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


if __name__ == '__main__':
    app.run()