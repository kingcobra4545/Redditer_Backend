import pymysql,unicodedata,datetime,time,json
from flask import Flask, request, render_template, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import DeclarativeMeta
from collections import namedtuple

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@localhost:8889/prajwal'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class Developer(db.Model):
	__tablename__ = 'ArticlesReddit'
	id = db.Column('ID',db.Integer, primary_key=True)
	header = db.Column('HEADER',db.String(50))
	sub_header = db.Column('SUB_HEADER',db.String(50))
	description = db.Column('DESCRIPTION',db.String(255))
	header_icon_url = db.Column('HEADER_ICON_URL',db.String(200))
	main_image_url = db.Column('MAIN_IMAGE_URL',db.String(200))
	likes = db.Column('LIKES',db.Integer)
	dislikes = db.Column('DISLIKES',db.Integer)
	comments = db.Column('COMMENTS',db.Integer)
	time_posted_at = db.Column('TIME_POSTED_AT',db.String(50))
	source_form = db.Column('SOURCE_FROM',db.String(200))
	updated_time = db.Column('UPDATED_TIME',db.String(50))
	

	def __init__(self,  header, sub_header, description, header_icon_url,main_image_url, likes, dislikes,
		comments,source_form,time_posted_at, updated_time ):
		# self.id = id
		self.header = header
		self.header_icon_url = header_icon_url
		self.sub_header = sub_header
		self.time_posted_at = time_posted_at
		self.source_form = source_form
		self.description = description
		self.main_image_url = main_image_url
		self.likes = likes
		self.dislikes = dislikes
		self.comments = comments
		self.updated_time = updated_time


@app.route('/')
def index():

	#todos = Developer.query.all()
	return render_template('index.html')
@app.route('/addformjson', methods=['POST'])
def addformjson():
	try:
		data =  request.get_data("success")
		x = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
		itemInside = Developer(
			header = x.header, 
	    	sub_header = "u/HippyHunter7",
	    	description = x.description,
	    	header_icon_url = " ",
	    	main_image_url = " ",
	    	source_form = " ",
	    	likes = 0,
	    	dislikes = 0,
	    	comments = 0,
	    	time_posted_at = "6h",
	    	updated_time = datetime.datetime.now()
	    	)
		db.session.add(itemInside)
		db.session.commit()
	except:
			print 'Exception Caught'
			return  "{\"done\":\"failed\"}"
	return "{\"done\":\"done\"}"

@app.route('/addlikeordislike', methods=['POST'])
def addlikeordislike():
	try:
		data =  request.get_data("success")
		x = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
		if 'dislikes' in data:
			if x.dislikes=="1":
				item = Developer.query.filter_by(id=int(x.id)).first()
				item.likes = item.likes - 1
				p = item.likes
				db.session.commit()
				returnValue = "{\"id\":\""+ x.id +"\",\"dislikes\":"+"\""+str(p)+"\"}"
		else:
			if x.likes=="1":
				item = Developer.query.filter_by(id=int(x.id)).first()
				item.likes = item.likes + 1
				p = item.likes
				db.session.commit()
				returnValue =  "{\"id\":\""+ x.id +"\",\"likes\":"+"\""+str(p)+"\"}"
		
			# else:
			# 	if x.comments=="1":
			# 		item = Developer.query.filter_by(id=int(x.id)).first()
			# 		item.comments = item.comments + 1
			# 		db.session.commit()
			# 		returnValue = "{\"likes\":"+"\""+item.comments+"\"}"

	except:
			print 'Exception Caught'
			return  "{\"likes\":\"failed\"}"

	return returnValue

@app.route('/returnJsonForRedditTimeline', methods=['GET'])
def returnJsonForRedditTimeline():
    c = Developer.query.all()
    return json.dumps(c, cls=AlchemyEncoder)


class AlchemyEncoder(json.JSONEncoder):
	def default(self, obj):

	    if isinstance(obj.__class__, DeclarativeMeta):
	        # an SQLAlchemy class
	        fields = {}
	        for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
	            data = obj.__getattribute__(field)
	            try:
	                json.dumps(data) # this will fail on non-encodable values, like other classes
	                fields[field] = data
	            except TypeError:
	                fields[field] = None
	        # a json-encodable dict
	        return fields

	    return json.JSONEncoder.default(self, obj)

if __name__ == '__main__':
    app.run(debug = True)
