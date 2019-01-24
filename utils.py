#to store/update/retrieve data
import json
from flask import session, escape
from main import db
from models import *
#constants
filename = "data1.json"






########DB


def create_new_user_db(name, empId):
	new_user = User(username = name, emp_id = empId)
	db.session.add(new_user)
	db.session.commit()
	print(User.query.all())

def user_search_by_empid_db(empId):
	user = {}
	x = User.query.filter_by(emp_id = empId).first()
	print("X")
	print(x)
	return {
	'username' : x.username,
	'empId' : x.emp_id
	}

def user_exists_db(empId):
	userAlreadyExists = False
	#load file
	if(User.query.filter_by(emp_id = empId).first()):
		userAlreadyExists = True
	return userAlreadyExists






##########







def test():
	return "hello"

def user_login(empId):
	session['empId'] = escape(empId)

def is_logged_in():
	if 'empId' in session:
		return True
	return False 

def user_exists(empId):
	userAlreadyExists = False
	#load file
	with open("data1.json") as f:
		data = json.load(f)
		for i in data:
			if(i["empId"] == empId):
				userAlreadyExists = True
	return userAlreadyExists

def create_new_user(name, empId):
	#read whole json
	#load file
	data = []
	with open("data1.json") as f:
		data = json.load(f)
	newUser = {
	"username" : name,
	"empId" : empId,
	"userData": {
            "dayCount": "0"
        },
        "dayData": [
        ]
	}
	data.append(newUser)
	with open("data1.json", "w") as f:
		json.dump(data,f,indent=4)
	return "created user " + name + " " + empId

def user_search_by_empid(empId):
	user = {}
	with open("data1.json") as f:
		data = json.load(f)
		for i in data:
			if(i["empId"] == empId):
				user = i
				break
	return user

def user_search_by_name(name):
	user = {}
	with open("data1.json") as f:
		data = json.load(f)
		for i in data:
			if(i["username"] == name):
				user = i
	return user

def events_specific_day(userObj, dayNumber):
	#returns a list of events for the day
	events = []
	for i in userObj['dayData']:
		if(i['dayId']==dayNumber):
			events = i['events']
	return events

def insert_event(userObj, dayNumber, newEvent):
	events = []
	for i in userObj['dayData']:
		if(i['dayId']==dayNumber):
			events = i['events']
	events.append(newEvent)
	#read file
	data = []
	with open("data1.json") as f:
		data = json.load(f)

	for i in data:
		if(i["username"] == userObj['username']):
			for j in i['dayData']:
				if(j['dayId'] == dayNumber):
					j['events'] = events
	
	with open("data1.json", "w") as f:
		json.dump(data,f,indent=4)	