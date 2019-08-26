from institutefamilies import db
from datetime import datetime

class Pocket(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), unique=True, nullable=False)
	pioneers = db.Column(db.Boolean, nullable=False)
	families = db.relationship('Family', backref='nhood', lazy=True)
	activities = db.relationship('Activity', backref='nhood', lazy=True)

	def __repr__(self):
		return f"Pocket('{self.name}')"

class Activity(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	type_activity = db.Column(db.String(20), nullable=False)
	facilitator = db.Column(db.String(50), nullable=False)
	pocket_id = db.Column(db.Integer, db.ForeignKey('pocket.id'), nullable=False)

class Family(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	surname = db.Column(db.String(20), nullable=False)
	address = db.Column(db.String(50), nullable=False)
	pocket_id = db.Column(db.Integer, db.ForeignKey('pocket.id'), nullable=False)
	individuals = db.relationship('Individual', backref='fam', lazy=True)
	visits = db.relationship('Visit', backref='fam', lazy=True)

	def __repr__(self):
		return f"Family('{self.surname}', '{self.address}')"

class Individual(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(20), nullable=False)
	age = db.Column(db.String(10), nullable=False)
	activity = db.Column(db.String(20), nullable=False)
	family_id = db.Column(db.Integer, db.ForeignKey('family.id'), nullable=False)

	def __repr__(self):
		return f"Individual('{self.first_name}', '{self.age}')"

class Visit(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	description = db.Column(db.Text, nullable=False)
	next_steps = db.Column(db.Text, nullable=False)
	family_id = db.Column(db.Integer, db.ForeignKey('family.id'), nullable=False)

	def __repr__(self):
		return f"Visit('{self.date}')"