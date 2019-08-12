from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, IntegerField, BooleanField, SelectField, DateField
from wtforms.validators import DataRequired, ValidationError
from institutefamilies.models import Pocket, Family

class AddPocketForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired()])
	num_activities = IntegerField('Number of Core Activities', validators=[DataRequired()])
	pioneers = BooleanField('Do pioneers live in this pocket?')
	submit = SubmitField('Add')

	def validate_name(self, name):
		pocket = Pocket.query.filter_by(name=name.data).first()
		if pocket:
			raise ValidationError('That pocket is already in the system.')

class AddFamilyForm(FlaskForm):
	surname = StringField('Surname', validators=[DataRequired()])
	address = StringField('Address/Unit Number', validators=[DataRequired()])
	submit = SubmitField('Add')

	def validate_address(self, address):
		family = Family.query.filter_by(address=address.data).first()
		if family:
			raise ValidationError('That address is already associated with a family.')

class AddIndividualForm(FlaskForm):
	first_name = StringField('First Name', validators=[DataRequired()])
	activity = SelectField('Core Activity', choices=[('no', 'None'), ('sc','Study Circle'), ('cc', 'Childrens Class'), ('jyg', 'Junior Youth Group'), ('dv', 'Devotional')])
	submit = SubmitField('Add')

class AddVisitForm(FlaskForm):
	date = DateField('Date of Visit', validators=[DataRequired()], format='%Y-%m-%d')
	description = TextAreaField('Description', validators=[DataRequired()])
	next_steps = TextAreaField('Next Steps', validators=[DataRequired()])
	submit = SubmitField('Add')