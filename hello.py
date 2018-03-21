import pymysql
from flask import Flask, request, render_template, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@localhost:8889/prajwal'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# class User(db.Model):
#     id = db.Column(db.Integer(5), unique=True)
#     tester = db.Column(db.String(80))

class Developer(db.Model):
	__tablename__ = 'sample2'
	id = db.Column('id',db.Integer, primary_key=True)
	tester = db.Column('tester',db.String(20))


    

	def __init__(self,  tester):
		# self.id = id
		self.tester = tester
        
        # self.hireDate = datetime.datetime.strptime(hireDate, "%d%m%Y").date()
        

@app.route('/')
def index():

	todos = Developer.query.all()
	return render_template('index.html', todos=todos)
@app.route('/addform', methods=['POST'])
def addform():
    todo = Developer( tester=request.form['todoitem'])
    db.session.add(todo)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/add', methods=['GET'])
def add():
	dev = Developer( tester = 'tusspataki')
	db.session.add(dev)
	db.session.commit()
	return '<html><body><h1>Hello World</h1></body></html>'
@app.route('/readAll', methods=['GET'])
def readAll():
	dev = Developer.query.all()
	# db.session.add(dev)
	# db.session.commit()
	return dev.jsonify
@app.route('/read', methods=['GET'])
def read():

	db = SQLAlchemy()
	summary_cursor = db.query.all()#('SELECT * FROM sample1 ')
	summary = summary_cursor.fetchall()
	data = map(list, summary)
	print data
	if request.args['type'] == 'json':
		return jsonify(summary = data)
	else:
		return 'Failure'

# @app.route('/articles', methods=['GET', 'POST'])
# def articles():
# 	if request.method == 'GET':
# 		return jsonify('PRAJWAL')
if __name__ == '__main__':
    app.run(debug = True)
