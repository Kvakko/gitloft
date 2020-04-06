from app import app, db
from app.models import Trekk, LoftElement, Forestilling

@app.shell_context_processor
def make_shell_context():
	return {'db':db, 'Trekk':Trekk, 'LoftElement':LoftElement, 'Forestilling':Forestilling}