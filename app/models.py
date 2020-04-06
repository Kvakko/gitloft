from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

trekknr = [
'LX 6', 'Tr 72', 'Tr 71', 'Tr 70', 'Tr 69', 'Tr 68', 'Tr 67', 'Tr 66', 'Tr 65', 'Tr 64', 'Tr 63', 'Tr 62', 'Tr 61', 'Tr 60', 'LX 5', 'Tr 59', 'Tr 58',
'Tr 57', 'Tr 56', 'Tr 55', 'Tr 54', 'Tr 53', 'Tr 52', 'Tr 51', 'Tr 50', 'Tr 49', 'Tr 48', 'Tr 47', 'Tr 46', 'LX 4', 'Tr 45', 'Tr 44', 'Tr 43', 'Tr 42', 'Tr 41', 'Tr 40', 'Tr 39',
'Tr 38', 'Tr 37', 'Tr 36', 'Tr 35', 'Tr 34', 'Tr 33', 'Tr 32', 'LX 3', 'Tr 29', 'Tr 28', 'Tr 27', 'Tr 26', 'Tr 25', 'Tr 24', 'Tr 23', 'Tr 22', 'Tr 21', 'Tr 20', 'Tr 19', 'Tr 18',
'Tr 17', 'Tr 16', 'LX 2', 'Tr 13', 'Tr 12', 'Tr 11', 'Tr 10', 'Tr 9', 'Tr 8', 'Tr 7', 'Tr 6', 'Tr 5', 'Tr 4', 'Tr 3', 'Tr 2', 'Tr 1', 'Utr 3', 'Utr 2']


class Forestilling(db.Model):
	id= db.Column(db.Integer, primary_key=True)
	forestilling_navn = db.Column(db.String(120), index = True)
	premiere = db.Column(db.DateTime, index=True)
	prod_nr = db.Column(db.Integer, index=True)
	aktuell = db.Column(db.Boolean, default = False, index = True)

	elementer = db.relationship('LoftElement', backref='tilhorer_forestilling', lazy = True, cascade="all, delete-orphan")

	def __repr__(self):
		return '< {} >'.format(self.forestilling_navn)


class Trekk(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	trekknummer = db.Column(db.String(64), index = True, unique = True)
	elementer = db.relationship('LoftElement', backref ='loftpos', lazy =True)

	def __repr__(self):
		return '<{}>'.format(self.trekknummer)

class LoftElement(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	element_navn = db.Column(db.String(64), index = True)
	trekk_id = db.Column(db.Integer, db.ForeignKey('trekk.id'))
	posisjon = db.Column(db.String(140))
	paaskjot = db.Column(db.String(120))
	ekstra_info = db.Column(db.String(140))
	forestilling_id = db.Column(db.Integer, db.ForeignKey('forestilling.id'))


	def __repr__(self):
		return '<LoftElement {}>'.format(self.element_navn)


class User(UserMixin, db.Model):
	id =db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique= True)
	email = db.Column(db.String(120), index= True, unique= True)
	password_hash = db.Column(db.String(128))

	def __repr__(self):
		return '<user {}>'.format(self.username)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
	return User.query.get(int(id))