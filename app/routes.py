from app import app, db
from flask import render_template, flash, redirect, url_for, request 
from app.forms import RedigerKnapp, AktuellKraesj, KraesjListe, LoginForm, RegisrerForestillingForm, RedigerForestilling, RegLoftElement, NyttElementKnapp, SlettForestilling, trekknr
from app.models import Trekk, LoftElement, Forestilling, User
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form=LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('feil navn eller passord')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html', title ='log inn', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))


@app.route('/')
@app.route('/index')
def index():
	forestillinger = Forestilling.query.all()
	return render_template('index.html', title = 'forestillinger', forestillinger=forestillinger)


@app.route('/index/<forestilling_navn>', methods =['GET', 'POST'])
def forestilling(forestilling_navn):
	form = NyttElementKnapp()
	form2 = SlettForestilling()	
	form3 =RedigerForestilling()
	form4 = RedigerKnapp()

	
	forestilling = Forestilling.query.filter_by(forestilling_navn=forestilling_navn).first_or_404()
	
	
	if form3.validate_on_submit():		
		forestilling.forestilling_navn=form3.forestilling_navn.data
		forestilling.prod_nr=form3.prod_nr.data
		forestilling.premiere = form3.premiere.data
		db.session.commit()
		return redirect(url_for('forestilling', forestilling_navn= forestilling.forestilling_navn))

	elif request.method == "GET":
		form3.forestilling_navn.data = forestilling.forestilling_navn
		form3.prod_nr.data = forestilling.prod_nr
		form3.premiere.data = forestilling.premiere
		
		
	if form.validate_on_submit():
			return redirect(url_for('regloftelement/{{form.forestilling_id.data}}'))	
	
	trekkliste = Trekk.query.all()
	elementliste = LoftElement.query.filter_by(forestilling_id=forestilling.id).all()
	return render_template('forestilling.html', form=form, form2=form2, form3=form3, form4 = form4, title = forestilling_navn, forestilling=forestilling, trekkliste=trekkliste, elementliste=elementliste)

@app.route('/slett/<forestilling_navn>', methods =['POST'])
@login_required
def slett(forestilling_navn):
	form2 = SlettForestilling()
	forestilling = Forestilling.query.filter_by(forestilling_navn=forestilling_navn).first_or_404()
	if request.method == 'POST':
		db.session.delete(forestilling)
		db.session.commit()
		return redirect(url_for('index'))


@app.route('/regforestilling', methods=['GET', 'POST'])
@login_required
def regforestilling():
	form = RegisrerForestillingForm()
	if form.validate_on_submit():
		forestilling=Forestilling(forestilling_navn=form.forestilling_navn.data, premiere=form.premiere.data, aktuell = False, prod_nr =form.prod_nr.data)
		db.session.add(forestilling)
		db.session.commit()
		flash('grattis')
		return redirect(url_for('forestilling', forestilling_navn= forestilling.forestilling_navn))

	return render_template('regforestilling.html', title= 'registrer forestilling', form=form)

@app.route('/regloftelement/<id>/<trekk_id>', methods=['GET', 'POST'])
@login_required
def regloftelement(id, trekk_id):
	form = RegLoftElement()
	forestilling = Forestilling.query.filter_by(id=id).first()
	if form.validate_on_submit():
		ting= LoftElement(element_navn = form.element_navn.data,  posisjon= form.posisjon.data, paaskjot=form.paaskjot.data, ekstra_info=form.ekstra_info.data, trekk_id=form.trekk_id.data, forestilling_id=id)		
		db.session.add(ting)
		db.session.commit()
		return redirect(url_for('forestilling', forestilling_navn = forestilling.forestilling_navn))
		
	form.trekk_id.data = int(trekk_id)		
	return render_template('/regloftelement.html', title ='registrer element', form=form)



@app.route('/oppdaterloftelement/<id>/<trekk_id>', methods = ['GET', 'POST'])
@login_required
def oppdaterloftelement(id, trekk_id):
	form = RegLoftElement()
	forestilling = Forestilling.query.filter_by(id=id).first()
	element=LoftElement.query.filter_by(id = trekk_id).first()
		
	if form.validate_on_submit():
		if form.submit.data:
			element.element_navn = form.element_navn.data
			element.posisjon = form.posisjon.data
			element.paaskjot = form.paaskjot.data
			element.trekk_id = form.trekk_id.data
			element.ekstra_info = form.ekstra_info.data
			db.session.commit()
		elif form.delete.data:
			db.session.delete(element)
			db.session.commit()

		return redirect(url_for('forestilling', forestilling_navn = forestilling.forestilling_navn))
	
	form.element_navn.data = element.element_navn
	form.posisjon.data = element.posisjon
	form.paaskjot.data = element.paaskjot
	form.trekk_id.data = element.trekk_id
	form.ekstra_info.data = element.ekstra_info
	return render_template('/oppdaterloftelement.html', title ='oppdater element', form=form)

@app.route('/kraesj', methods = ['POST', 'GET'])
def kraesj():
	form = KraesjListe()	

	if form.submit.data:
		forestilling1 = form.forestilling1.data
		forestilling2 = form.forestilling2.data
		forestilling3 = form.forestilling3.data
		forestilling4 = form.forestilling4.data

		return redirect(url_for('nykraesj', id1 = forestilling1, id2 = forestilling2, id3 = forestilling3, id4 = forestilling4))
	


	form.forestilling1.choices = [(f.id, f.forestilling_navn) for f in Forestilling.query.all()]
	form.forestilling2.choices = [(f.id, f.forestilling_navn) for f in Forestilling.query.all()]
	form.forestilling3.choices = [(f.id, f.forestilling_navn) for f in Forestilling.query.all()]
	form.forestilling4.choices = [(f.id, f.forestilling_navn) for f in Forestilling.query.all()]


	return render_template('/kraesj.html', title = 'KRÆSJ', form=form, )

@app.route('/nykraesj/<id1>/<id2>/<id3>/<id4>', methods = ['POST', 'GET'])
def nykraesj(id1, id2, id3, id4):
	trekkliste = Trekk.query.all()
	form = AktuellKraesj()
	forest1= Forestilling.query.filter_by(id=id1).first_or_404()
	forest2= Forestilling.query.filter_by(id=id2).first_or_404()
	forest3 = Forestilling.query.filter_by(id=id3).first_or_404()
	forest4 = Forestilling.query.filter_by(id=id4).first_or_404()
	if form.submit.data:
		alle = Forestilling.query.all()
		for f in alle:
			f.aktuell = False
		
		forest1.aktuell = True
		forest2.aktuell = True
		forest3.aktuell = True
		forest4.aktuell = True
		db.session.commit()
		return redirect(url_for('aktuellkraesj'))


	
	elementliste1 = LoftElement.query.filter_by(forestilling_id =forest1.id).all()
	elementliste2 = LoftElement.query.filter_by(forestilling_id =forest2.id).all()
	elementliste3 = LoftElement.query.filter_by(forestilling_id =forest3.id).all()
	elementliste4 = LoftElement.query.filter_by(forestilling_id =forest4.id).all()

	return render_template('/nykraesj.html', trekkliste=trekkliste, form = form, elementliste1 = elementliste1, elementliste2 = elementliste2, elementliste3 = elementliste3, elementliste4 = elementliste4, forest1=forest1, forest2 = forest2, forest3 = forest3, forest4= forest4, title = 'Kræsj')

@app.route('/aktuellkraesj')
def aktuellkraesj():
	
	elementliste =[]
	forestillingsliste=[]
	trekkliste = Trekk.query.all()
	forestillinger = Forestilling.query.all()
	loftelementer = LoftElement.query.all()
	for f in forestillinger:
		if f.aktuell==True:
			forestillingsliste.append(f)
			for element in loftelementer:
				if element.forestilling_id == f.id:
					elementliste.append(element)


	


	return render_template('aktuellkraesj.html', trekkliste=trekkliste, elementliste=elementliste, forestillingsliste = forestillingsliste, title = 'aktuell kræsj')





