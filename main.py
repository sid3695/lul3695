from flask import Flask, render_template, url_for, session, request, redirect
app = Flask(__name__)

from utils import *

app.secret_key = "test"

@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/signup', methods = ['GET', 'POST'])
def signup():
	print("signup" + test())

	if request.method == 'POST':
		#if entered
		#check if already
		if user_exists(request.form['name']):
			return render_template("signup.html", flag = 2)

		#otherwise create
		else:
			create_new_user(request.form['name'], request.form['numberDevices'])
			#log in the user/session
			user_login(request.form['name'])
			return redirect(url_for("landing", name = request.form['name']))
	else:
		#landing on page
		return render_template("signup.html", flag = 0)

@app.route('/login', methods = ['GET', 'POST'])
def login():
	print("login" + test())

	if request.method == 'POST':
		#if entered
		#check if already
		if user_exists(request.form['name']):
			user_login(request.form['name'])
			return redirect(url_for("landing", name = request.form['name']))
		else:
			#log in the user/session
			return render_template("login.html", flag = 2)
	else:
		#landing on page
		return render_template("login.html", flag = 0)


@app.route('/landing/<name>',methods = ['GET', 'POST'])
def landing(name):
	if is_logged_in():
		userObj = user_search_by_name(name)
		print (userObj)
		if request.method == "GET":
			return render_template("landing.html", name = name, userObj = userObj)
		else:
			#POST
			#redirect
			#print(request.form['dayNumber'])
			#return "5"
			return redirect(url_for("daynumber", day = request.form['dayNumber']))
	else:
		return redirect(url_for("login"))

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