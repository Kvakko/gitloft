from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, IntegerField, SelectField
from wtforms.validators import DataRequired
from datetime import datetime
from app.models import Forestilling

trekknr = [(1, 'LX 6'), (2, 'Tr 72'), (3, 'Tr 71'), (4, 'Tr 70'), (5, 'Tr 69'), (6, 'Tr 68'), (7, 'Tr 67'), 
(8, 'Tr 66'), (9, 'Tr 65'), (10, 'Tr 64'), (11, 'Tr 63'), (12, 'Tr 62'), (13, 'Tr 61'), (14, 'Tr 60'), 
(15, 'LX 5'), (16, 'Tr 59'), (17, 'Tr 58'), (18, 'Tr 57'), (19, 'Tr 56'), (20, 'Tr 55'), (21, 'Tr 54'), 
(22, 'Tr 53'), (23, 'Tr 52'), (24, 'Tr 51'), (25, 'Tr 50'), (26, 'Tr 49'), (27, 'Tr 48'), (28, 'Tr 47'), 
(29, 'Tr 46'), (30, 'LX 4'), (31, 'Tr 45'), (32, 'Tr 44'), (33, 'Tr 43'), (34, 'Tr 42'), (35, 'Tr 41'), 
(36, 'Tr 40'), (37, 'Tr 39'), (38, 'Tr 38'), (39, 'Tr 37'), (40, 'Tr 36'), (41, 'Tr 35'), (42, 'Tr 34'), 
(43, 'Tr 33'), (44, 'Tr 32'), (45, 'LX 3'), (46, 'Tr 29'), (47, 'Tr 28'), (48, 'Tr 27'), (49, 'Tr 26'), 
(50, 'Tr 25'), (51, 'Tr 24'), (52, 'Tr 23'), (53, 'Tr 22'), (54, 'Tr 21'), (55, 'Tr 20'), (56, 'Tr 19'), 
(57, 'Tr 18'), (58, 'Tr 17'), (59, 'Tr 16'), (60, 'LX 2'), (61, 'Tr 13'), (62, 'Tr 12'), (63, 'Tr 11'), 
(64, 'Tr 10'), (65, 'Tr 9'), (66, 'Tr 8'), (67, 'Tr 7'), (68, 'Tr 6'), (69, 'Tr 5'), (70, 'Tr 4'), (71, 'Tr 3'),
 (72, 'Tr 2'), (73, 'Tr 1'), (74, 'Utr 3'), (75, 'Utr 2')]



class LoginForm(FlaskForm):
    username = StringField('Brukernavn', validators=[DataRequired()])
    password = PasswordField('Passord', validators=[DataRequired()])
    remember_me = BooleanField('Husk meg')
    submit = SubmitField('Logg inn')

class RegisrerForestillingForm(FlaskForm):
	forestilling_navn=StringField('<strong>Forestillingens navn</strong>', validators=[DataRequired()])
	premiere = DateField('<b>premieredato </b> <small>årår-mm-dd</small>')
	prod_nr = IntegerField('<b>prod.nr</b>', default=0)
	submit = SubmitField('registrer!')

class RedigerForestilling(FlaskForm):
	forestilling_navn=StringField('<strong>Forestillingens navn</strong>', validators=[DataRequired()])
	premiere = DateField('<b>premieredato </b> <small>årår-mm-dd</small>')
	prod_nr = IntegerField('<b>prod.nr</b>')
	submit = SubmitField('Oppdater!')




	
class RegLoftElement(FlaskForm):
	element_navn = StringField('hva skal henges?', validators=[DataRequired()])
	trekk_id =SelectField('Trekk', choices=trekknr, validators=[DataRequired()], coerce=int)
	posisjon = StringField('posisjon på trekket')
	paaskjot =StringField('påskjøt')
	ekstra_info =StringField('kommentar')
	submit = SubmitField('legg til')
	delete = SubmitField('slett')

class KraesjListe(FlaskForm):
	forestilling1=SelectField(coerce=int)
	forestilling2=SelectField(coerce=int)
	forestilling3=SelectField(coerce=int)
	forestilling4=SelectField(coerce=int) 
	submit = SubmitField('lag Kræsj')


class NyttElementKnapp(FlaskForm):
	trekk_nr =StringField('nummer')
	submit= SubmitField('Legg til ')

class RedigerKnapp(FlaskForm):
	submit= SubmitField('Rediger')


class SlettForestilling(FlaskForm):
	submit=SubmitField('slett forestilling')


class AktuellKraesj(FlaskForm):
	submit =SubmitField('Sett aktuell Kræsj')

