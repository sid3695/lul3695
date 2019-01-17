#to store/update/retrieve data
import json
from flask import session, escape
def test():
	return "hello"

def user_login(name):
	session['name'] = escape(name)

def is_logged_in():
	if 'name' in session:
		return True
	return False 

def user_exists(name):
	userAlreadyExists = False
	#load file
	with open("data.json") as f:
		data = json.load(f)
		for i in data:
			if(i["username"] == name):
				userAlreadyExists = True
	return userAlreadyExists

def create_new_user(name, numberDevices):
	#read whole json
	#load file
	data = []
	with open("data.json") as f:
		data = json.load(f)
	newUser = {
	'username' : name,
	'numberDevices' : numberDevices
	}
	data.append(newUser)
	with open("data.json", "w") as f:
		json.dump(data,f,indent=4)
	return "hue" + name + numberDevices

def user_search_by_name(name):
	user = {}
	with open("data.json") as f:
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
	with open("data.json") as f:
		data = json.load(f)

	for i in data:
		if(i["username"] == userObj['username']):
			for j in i['dayData']:
				if(j['dayId'] == dayNumber):
					j['events'] = events
	
	with open("data.json", "w") as f:
		json.dump(data,f,indent=4)	