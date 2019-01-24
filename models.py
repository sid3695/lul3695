from main import db
from datetime import datetime

class User(db.Model):
	username = db.Column(db.String(40), nullable=False)
	emp_id = db.Column(db.Integer, nullable = False, primary_key = True)
	first_login = db.Column(db.Boolean, nullable = False, default = True)
	def __repr__(self):
		return '<User %r>' % self.username

class Date(db.Model):
	date = db.Column(db.Date, nullable=False)
	day_id = db.Column(db.Integer, nullable = False, primary_key = True)

	emp_id = db.Column(db.Integer, db.ForeignKey('user.emp_id'),nullable=False)
	user = db.relationship('User',backref=db.backref('dates', lazy=True))


	def __repr__(self):
		return '<Date %r>' % self.day_id

class Events(db.Model):
	event_id = db.Column(db.Integer, nullable = False, primary_key = True)
	action = db.Column(db.String(10), nullable = False)
	value = db.Column(db.String(10), nullable = False)
	devicename = db.Column(db.String(20), nullable = False)
	timestamp = db.Column(db.Time, nullable=False)

	day_id = db.Column(db.Integer, db.ForeignKey('date.day_id'),nullable=False)
	date = db.relationship('Date',backref=db.backref('events', lazy=True))


	def __repr__(self):
		return '<Event %r>' % self.event_id

class Devices(db.Model):
	devicename = db.Column(db.String(20), nullable = False)
	device_id = db.Column(db.Integer, nullable = False, primary_key = True)
	emp_id = db.Column(db.Integer, db.ForeignKey('user.emp_id'),nullable=False)
	user = db.relationship('User',backref=db.backref('devices', lazy=True))


	def __repr__(self):
		return '<Device %r>' % self.devicename