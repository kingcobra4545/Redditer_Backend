import pymysql
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# this userpass assumes you did not create a password for your database
# and the database username is the default, 'root'
userpass = 'mysql+pymysql://root:@'
basedir  = 'localhost:8889'
# change to YOUR database name, with a slash added as shown
dbname   = '/prajwal'
# this socket is going to be very different on a Windows computer
socket   = '?unix_socket=/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock'
dbname   = dbname + socket

# put them all together as a string that shows SQLAlchemy where the database is
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:8888/prajwal'#userpass + basedir + dbname

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# this variable, db, will be used for all SQLAlchemy commands
db = SQLAlchemy(app)

# this route will test the database connection and nothing more
@app.route('/')
def testdb():
    try:
    	#return userpass + basedir + dbname
  #   	me = User('root', 'root')
		# db.session.add(me)
		# db.session.commit()
        db.session.query("1").from_statement("SELECT 1").all()
        return '<h1>It works.</h1>'
    except:
        return '<h1>Something is broken...</h1>'

if __name__ == '__main__':
    app.run(debug=True)