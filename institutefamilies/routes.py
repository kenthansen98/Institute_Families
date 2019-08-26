from flask import render_template, url_for, flash, redirect, request
from institutefamilies import app, db
from institutefamilies.forms import AddPocketForm, AddFamilyForm, AddIndividualForm, AddVisitForm, AddActivityForm
from institutefamilies.models import Pocket, Family, Individual, Visit, Activity

@app.route("/")
@app.route("/home")
def home():
	page = request.args.get('page', 1, type=int)
	pockets = Pocket.query.order_by(Pocket.name.asc()).paginate(page=page, per_page=8)
	return render_template('home.html', pockets=pockets)

@app.route("/pocket/<string:name>")
def pocket(name):
	pocket = Pocket.query.filter_by(name=name).first_or_404()
	page = request.args.get('page', 1, type=int)
	families = Family.query.filter_by(nhood=pocket).order_by(Family.surname.asc()).paginate(page=page, per_page=5)
	activities = Activity.query.filter_by(nhood=pocket)
	return render_template('pocket.html', title=name, name=name, families=families, activities=activities)

@app.route("/pocket/new", methods=['GET', 'POST'])
def add_pocket():
	form = AddPocketForm()
	if form.validate_on_submit():
		pocket = Pocket(name=form.name.data, pioneers=form.pioneers.data)
		db.session.add(pocket)
		db.session.commit()
		flash('Pocket Added!', 'success')
		return redirect(url_for('home'))
	return render_template('add_pocket.html', title='Add Pocket', form=form)

@app.route("/pocket/<string:name>/delete", methods=['POST'])
def delete_pocket(name):
	pocket = Pocket.query.filter_by(name=name).first_or_404()
	families = Family.query.filter_by(nhood=pocket)
	for family in families:
		db.session.delete(family)
	db.session.delete(pocket)
	db.session.commit()
	flash('Pocket deleted', 'success')
	return redirect(url_for('home'))

#@app.route("/pocket/<string:name/acivity/<string:activity_name")
#def activity(name, activity_name):


@app.route("/pocket/<string:name>/add_activity", methods=['GET', 'POST'])
def add_activity(name):
	form = AddActivityForm()
	if form.validate_on_submit():
		current_pocket = Pocket.query.filter_by(name=name).first_or_404()
		activity = Activity(name=form.name.data, type_activity=form.type_activity.data, facilitator=form.facilitator.data, nhood=current_pocket)
		db.session.add(activity)
		db.session.commit()
		flash('Acitivty added!', 'success')
		return redirect(url_for('pocket', name=name))
	return render_template('add_activity.html', title='Add Activity', form=form, legend='Add Activity')

@app.route("/pocket/<string:name>/<int:activity_id>/delete_activity", methods=['POST'])
def delete_activity(name, activity_id):
	activity = Activity.query.get_or_404(activity_id)
	db.session.delete(activity)
	db.session.commit()
	flash('Activity deleted', 'success')
	return redirect(url_for('pocket', name=name))

@app.route("/pocket/<string:name>/<int:activity_id>/update_activity", methods=['GET', 'POST'])
def update_activity(name, activity_id):
	activity = Activity.query.get_or_404(activity_id)
	form = AddActivityForm()
	if form.validate_on_submit():
		activity.name = form.name.data
		activity.type_activity = form.type_activity.data
		activity.facilitator = form.facilitator.data
		db.session.commit()
		flash('The activity has been updated', 'success')
		return redirect(url_for('pocket', name=name))
	elif request.method == 'GET':
		form.name.data = activity.name
		form.type_activity.data = activity.type_activity
		form.facilitator.data = activity.facilitator
	return render_template('add_activity.html', title='Update Activity', form=form, legend='Update Activity')

@app.route("/pocket/<string:name>/new_family", methods=['GET', 'POST'])
def add_family(name):
	form = AddFamilyForm()
	if form.validate_on_submit():
		current_pocket = Pocket.query.filter_by(name=name).first_or_404()
		family = Family(surname=form.surname.data, address=form.address.data, nhood=current_pocket)
		db.session.add(family)
		db.session.commit()
		flash('Family Added!', 'success')
		return redirect(url_for('pocket', name=name))
	return render_template('add_family.html', title='Add Family', form=form, legend='Add Family')

@app.route("/pocket/<string:name>/<int:family_id>")
def family(name, family_id):
	family = Family.query.get_or_404(family_id)
	individuals = Individual.query.filter_by(fam=family).order_by(Individual.first_name.asc())
	visits = Visit.query.filter_by(fam=family).order_by(Visit.date.desc())
	return render_template('family.html', title=family.surname, family=family, individuals=individuals, visits=visits)

@app.route("/pocket/<string:name>/<int:family_id>/delete", methods=['POST'])
def delete_family(name, family_id):
	family = Family.query.get_or_404(family_id)
	individuals = Individual.query.filter_by(fam=family)
	for individual in individuals:
		db.session.delete(individual)
	db.session.delete(family)
	db.session.commit()
	flash('Family deleted', 'success')
	return redirect(url_for('pocket', name=name))

@app.route("/pocket/<string:name>/<int:family_id>/update", methods=['GET', 'POST'])
def update_family(name, family_id):
	family = Family.query.get_or_404(family_id)
	form = AddFamilyForm()
	if form.validate_on_submit():
		family.surname = form.surname.data
		family.address = form.address.data
		db.session.commit()
		flash('The family has been updated', 'success')
		return redirect(url_for('family', name=name, family_id=family_id))
	elif request.method == 'GET':
		form.surname.data = family.surname
		form.address.data = family.address
	return render_template('add_family.html', title='Update Family', form=form, legend='Update Family')

@app.route("/pocket/<string:name>/<int:family_id>/new_member", methods=['GET', 'POST'])
def add_member(name, family_id):
	form = AddIndividualForm()
	pocket = Pocket.query.filter_by(name=name).first_or_404()
	form.activity.choices = [("", "---")]+[(activity.name, activity.name) for activity in Activity.query.filter_by(nhood=pocket).all()]
	if form.validate_on_submit():
		current_family = Family.query.filter_by(id=family_id).first_or_404()
		activity = Activity.query.filter_by(name=form.activity.data).first()
		individual = Individual(first_name=form.first_name.data, age=form.age.data, activity=form.activity.data, fam=current_family, act=activity)
		db.session.add(individual)
		db.session.commit()
		flash('Individual Added!', 'success')
		return redirect(url_for('family', name=name, family_id=family_id))
	return render_template('add_member.html', title='Add Individual', form=form, legend='Add Individual')

@app.route("/pocket/<string:name>/<int:family_id>/<int:individual_id>/update_member", methods=['GET', 'POST'])
def update_member(name, family_id, individual_id):
	individual = Individual.query.get_or_404(individual_id)
	form = AddIndividualForm()
	pocket = Pocket.query.filter_by(name=name).first_or_404()
	form.activity.choices = [("", "---")]+[(activity.name, activity.name) for activity in Activity.query.filter_by(nhood=pocket).all()]
	if form.validate_on_submit():
		individual.first_name = form.first_name.data
		individual.age = form.age.data
		individual.activity = form.activity.data
		individual.act = Activity.query.filter_by(name=form.activity.data).first()
		db.session.commit()
		flash('The individual has been updated', 'success')
		return redirect(url_for('family', name=name, family_id=family_id))
	elif request.method == 'GET':
		form.first_name.data = individual.first_name
		form.age.data = individual.age
		form.activity.data = individual.activity
	return render_template('add_member.html', title='Update Individual', form=form, legend='Update Individual')

@app.route("/pocket/<string:name>/<int:family_id>/<int:individual_id>/delete_member", methods=['POST'])
def delete_member(name, family_id, individual_id):
	individual = Individual.query.get_or_404(individual_id)
	db.session.delete(individual)
	db.session.commit()
	flash('Individual deleted', 'success')
	return redirect(url_for('family', name=name, family_id=family_id))

@app.route("/pocket/<string:name>/<int:family_id>/new_visit", methods=['GET', 'POST'])
def add_visit(name, family_id):
	form = AddVisitForm()
	if form.validate_on_submit():
		current_family = Family.query.filter_by(id=family_id).first_or_404()
		visit = Visit(date=form.date.data, description=form.description.data, next_steps=form.next_steps.data, fam=current_family)
		db.session.add(visit)
		db.session.commit()
		flash('Visit Added!', 'success')
		return redirect(url_for('family', name=name, family_id=family_id))
	return render_template('add_visit.html', title='Add Visit', form=form, legend='Add Visit')

@app.route("/pocket/<string:name>/<int:family_id>/<int:visit_id>", methods=['GET', 'POST'])
def visit(name, family_id, visit_id):
	visit = Visit.query.get_or_404(visit_id)
	return render_template('visit.html', visit=visit)

@app.route("/pocket/<string:name>/<int:family_id>/<int:visit_id>/delete", methods=['POST'])
def delete_visit(name, family_id, visit_id):
	visit = Visit.query.get_or_404(visit_id)
	db.session.delete(visit)
	db.session.commit()
	flash('Visit deleted', 'success')
	return redirect(url_for('family', name=name, family_id=family_id))

@app.route("/pocket/<string:name>/<int:family_id>/<int:visit_id>/update", methods=['GET', 'POST'])
def update_visit(name, family_id, visit_id):
	visit = Visit.query.get_or_404(visit_id)
	form = AddVisitForm()
	if form.validate_on_submit():
		visit.date = form.date.data
		visit.description = form.description.data
		visit.next_steps = form.next_steps.data
		db.session.commit()
		flash('The visit has been updated!', 'success')
		return redirect(url_for('visit', name=name, family_id=family_id, visit_id=visit_id))
	elif request.method == 'GET':
		#form.date.data = visit.date
		form.description.data = visit.description
		form.next_steps.data = visit.next_steps
	return render_template('add_visit.html', title='Update Visit', form=form, legend='Update Visit')





