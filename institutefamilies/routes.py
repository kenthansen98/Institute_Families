from flask import render_template, url_for, flash, redirect
from institutefamilies import app, db
from institutefamilies.forms import AddPocketForm, AddFamilyForm, AddIndividualForm, AddVisitForm
from institutefamilies.models import Pocket, Family, Individual, Visit

@app.route("/")
@app.route("/home")
def home():
	pockets = Pocket.query.all()
	return render_template('home.html', pockets=pockets)

@app.route("/pocket/<string:name>")
def pocket(name):
	pocket = Pocket.query.filter_by(name=name).first_or_404()
	families = Family.query.filter_by(nhood=pocket)
	return render_template('pocket.html', name=name, families=families)

@app.route("/pocket/new", methods=['GET', 'POST'])
def add_pocket():
	form = AddPocketForm()
	if form.validate_on_submit():
		pocket = Pocket(name=form.name.data, num_activities=form.num_activities.data, pioneers=form.pioneers.data)
		db.session.add(pocket)
		db.session.commit()
		flash('Pocket Added!', 'success')
		return redirect(url_for('home'))
	return render_template('add_pocket.html', title='Add Pocket', form=form)

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
	return render_template('add_family.html', title='Add Family', form=form)

@app.route("/pocket/<string:name>/<int:family_id>")
def family(name, family_id):
	family = Family.query.get_or_404(family_id)
	individuals = Individual.query.filter_by(fam=family)
	visits = Visit.query.filter_by(fam=family)
	return render_template('family.html', title=family.surname, family=family, individuals=individuals, visits=visits)

@app.route("/pocket/<string:name>/<int:family_id>/delete", methods=['POST'])
def delete_family(name, family_id):
	family = Family.query.get_or_404(family_id)
	individuals = Individual.query.filter_by(family_id)
	for individual in individuals:
		db.session.delete(individual)
	db.session.delete(family)
	db.session.commit()
	flash('Family deleted', 'success')
	return redirect(url_for('pocket', name=name))

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

@app.route("/pocket/<string:name>/<int:family_id>/new_member", methods=['GET', 'POST'])
def add_member(name, family_id):
	form = AddIndividualForm()
	if form.validate_on_submit():
		current_family = Family.query.filter_by(id=family_id).first_or_404()
		individual = Individual(first_name=form.first_name.data, activity=form.activity.data, fam=current_family)
		db.session.add(individual)
		db.session.commit()
		flash('Individual Added!', 'success')
		return redirect(url_for('family', name=name, family_id=family_id))
	return render_template('add_member.html', title='Add Individual', form=form)

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
	return render_template('add_visit.html', title='Add Visit', form=form)

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





