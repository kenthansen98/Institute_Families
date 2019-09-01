from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, IntegerField, BooleanField, SelectField, DateField
from wtforms.validators import DataRequired, ValidationError, Optional
from institutefamilies.models import Pocket, Family, Activity

class AddPocketForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired()])
	pioneers = BooleanField('Do pioneers live in this pocket?')
	submit = SubmitField('Add')

	def validate_name(self, name):
		pocket = Pocket.query.filter_by(name=name.data).first()
		if pocket:
			raise ValidationError('That pocket is already in the system.')

class AddActivityForm(FlaskForm):
	name = StringField('Activity Name', validators=[DataRequired()])
	type_activity = SelectField('Core Activity', choices=[('None', 'None'), ('Study Circle','Study Circle'), ('Childrens Class', 'Childrens Class'), ('Junior Youth Group', 'Junior Youth Group'), ('Devotional', 'Devotional')])
	facilitator = StringField('Tutor/Teacher/Animator/Host', validators=[DataRequired()])
	submit = SubmitField('Add')

	def validate_name(self, name):
		activity = Activity.query.filter_by(name=name.data).first()
		if activity:
			raise ValidationError('That activity is already in the system.')

class AddFamilyForm(FlaskForm):
	surname = StringField('Surname', validators=[DataRequired()])
	address = StringField('Address/Unit Number', validators=[DataRequired()])
	submit = SubmitField('Add')

class AddIndividualForm(FlaskForm):
	first_name = StringField('First Name', validators=[DataRequired()])
	age = StringField('Age (if unknown specify age category)', validators=[DataRequired()])
	activity = SelectField('Activity', choices=[], coerce=str, validators=[Optional()])
	submit = SubmitField('Add')

class AddVisitForm(FlaskForm):
	date = DateField('Date of Visit', validators=[DataRequired()], format='%Y-%m-%d')
	description = TextAreaField('Description', validators=[DataRequired()])
	next_steps = TextAreaField('Next Steps', validators=[DataRequired()])
	submit = SubmitField('Add')

class AddReflectionForm(FlaskForm):
	date = DateField('Date of Reflection', validators=[DataRequired()], format='%Y-%m-%d')
	description = TextAreaField('Reflections', validators=[DataRequired()])
	submit = SubmitField('Add')

class AddMeetingForm(FlaskForm):
	date = DateField('Date of Meeting', validators=[DataRequired()], format='%Y-%m-%d')
	description = TextAreaField('Meeting', validators=[DataRequired()])
	submit = SubmitField('Add')


