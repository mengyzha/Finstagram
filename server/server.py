import uuid
from flask import Flask, jsonify, request, session
from flask_cors import CORS
import pymysql.cursors
import datetime
# import pymysql.err
# from flask_session import Session


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
# SESSION_TYPE = 'redis'
app.config.from_object(__name__)
# sess = Session()

# enable CORS
CORS(app)

# Configure MySQL
conn = pymysql.connect(host='localhost',
                       port=8889,
                       user='root',
                       password='root',
                       db='Finstagram',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

@app.route('/login', methods=['POST'])
def login():
	response_object = {'status': 'success'}
	# grabs information from the forms
	post_data = request.get_json()
	# cursor = conn.cursor()
	query = 'SELECT * FROM Person WHERE username = %s and password = %s'
	print(post_data.get('username'))
	print(post_data.get('password'))
	try:
		with conn.cursor() as cursor:
			cursor.execute(query, (post_data.get('username'), post_data.get('password')))	
		# cursor.execute(query, (post_data.get('username'), post_data.get('password')))
		data = cursor.fetchone()
		# cursor.close()
	# except pymysql.err.InternalError as error:
	except Exception as error:
		print(error.args)
		errmsg = error.args
		# errmsg = error.args
		response_object['errmsg'] = errmsg
		return jsonify(response_object)

	if (data):
		response_object['errno'] = 0
	else:
		response_object['errno'] = 401
		response_object['errmsg'] = 'Invalid login or username'
	return jsonify(response_object) 


@app.route('/register', methods=['POST'])
def register():
	response_object = {'status': 'success'}
	post_data = request.get_json()
	# cursor = conn.cursor()
	query = 'INSERT INTO Person VALUES (%s, %s, %s, %s, %s, %s, %s)'
	with conn.cursor() as cursor:
		cursor.execute(query, (post_data.get('username'),
			post_data.get('password'),
			post_data.get('fName'),
			post_data.get('lName'),
			post_data.get('avatar'),
			post_data.get('bio'),
			post_data.get('isPrivate')))
	# cursor.close()
	response_object['message'] = 'Person registered'
	return jsonify(response_object)

# sanity check route
@app.route('/', methods=['GET', 'POST'])
def all_photos():
	response_object = {'status': 'success'}
	# cursor = conn.cursor()
	if (request.method == 'POST'):
		post_data = request.get_json()

		username = post_data.get('username')
		timestamp = datetime.datetime.now()
		filePath = post_data.get('filePath')
		caption = post_data.get('caption')
		allFollowers = post_data.get('allFollowers')
		groupName = post_data.get('groupName')
		groupOwner = post_data.get('groupOwner')
		print(groupName)
		print(groupOwner)

		# cursor used to send queries
		ins = 'INSERT INTO Photo (photoOwner, timestamp, filePath, caption, allFollowers) VALUES (%s, %s, %s, %s, %s)'
		with conn.cursor() as cursor:
			cursor.execute(ins, (username, timestamp, filePath, caption, allFollowers))
			conn.commit()

		# if specifies a group
		if (groupName):
			# first find photoID
			query = 'SELECT max(photoID) AS max_ID FROM Photo'
			with conn.cursor() as cursor:
				cursor.execute(query)
				result = cursor.fetchone()
			photoID = result['max_ID']
			print(photoID)

			# then insert into share
			query = 'INSERT INTO Share (groupName, groupOwner, photoID) VALUES (%s, %s, %s)'
			with conn.cursor() as cursor:
				cursor.execute(query, (groupName, groupOwner, photoID))
				conn.commit()

		response_object['message'] = 'Photo added!'
	else:
		# Problem: when username is null, have keyerror 
		username = request.args['username']
		if (username):
			# query = 'SELECT * FROM Photo WHERE photoOwner = %s ORDER BY timestamp'
			query = '''SELECT DISTINCT * FROM Photo 
			WHERE photoID IN 
				(SELECT photoID FROM share NATURAL JOIN belong NATURAL JOIN Photo WHERE belong.username = %s) 
			OR photoID IN 
				(SELECT photoID FROM Follow JOIN Photo ON (Follow.followeeUsername = Photo.photoOwner) 
				 WHERE followerUsername = %s AND acceptedFollow = true AND allFollowers = true)
			ORDER BY timestamp DESC'''
			# try:
			cursor = conn.cursor()

			# with conn.cursor() as cursor:
			cursor.execute(query, (username, username))
			photos = cursor.fetchall()
			response_object['errno'] = 0
			response_object['photos'] = photos
			cursor.close()

			return jsonify(response_object)
		response_object['errno'] = 403
		response_object['errmsg'] = 'You need to login first'
		return jsonify(response_object)

	cursor.close()
	return jsonify(response_object)

@app.route('/search', methods = ['GET'])
def searchByPoster():
	if (request.method =='GET'):
		response_object = {'status': 'success'}
		# post_data = request.get_json()
		username = request.args['username']
		photoOwner = request.args['poster']
		query = '''SELECT DISTINCT *
				   FROM Photo
				   WHERE photoOwner = %s
				   AND (photoID IN
				   		(SELECT photoID 
						FROM share NATURAL JOIN belong NATURAL JOIN Photo
						WHERE belong.username = %s) 
						OR photoID IN 
						(SELECT photoID
						FROM Follow JOIN Photo ON (Follow.followeeUsername = Photo.photoOwner)
						WHERE followerUsername = %s AND acceptedFollow = true AND allFollowers = true))
				   ORDER BY timestamp DESC'''
		try:
			with conn.cursor() as cursor:
				cursor.execute(query, (photoOwner, username, username))
				photos = cursor.fetchall()
			response_object['errno'] = 0
			response_object['photos'] = photos
		except Exception as error:
			errno, errmsg = error.args
			response_object['errno'] = errno
			response_object['errmsg'] = errmsg
	
	return jsonify(response_object)

@app.route('/follow', methods = ['GET','POST', 'PUT'])
def follow():
	response_object = {'status': 'success'}
	# cursor = conn.cursor()
	if (request.method == 'POST'):
		# Todo: can a person follow hisself?
		post_data = request.get_json()
		followerUsername = post_data.get('followerUsername')
		followeeUsername = post_data.get('followeeUsername')
		acceptedFollow = False

		query = 'INSERT INTO Follow (followerUsername, followeeUsername, acceptedfollow) VALUES (%s, %s, %s)'
		
		try:
			with conn.cursor() as cursor:
				cursor.execute(query, (followerUsername, followeeUsername, acceptedFollow))
				conn.commit()
			# conn.commit()
			# cursor.close()
		except Exception as error:
			conn.rollback()
			errno, errmsg = error.args
			if (errno == 1062):
				response_object['message'] = 'Already followed this user'
			elif (errno == 1452):
				response_object['message'] = 'User does not exist'
			return jsonify(response_object)

		response_object['message'] = 'follow request sent'
		return jsonify(response_object)

	if (request.method == 'GET'):
		username = request.args['username']
		if (username):
			query = 'SELECT * FROM Follow WHERE followeeUsername = %s'
			with conn.cursor() as cursor:
				cursor.execute(query, username)
			followRequests = cursor.fetchall()
			response_object['errno'] = 0
			response_object['follows'] = followRequests
		else:
			response_object['errno'] = 403
			response_object['message'] = 'You need to login first'
		# cursor.close()
		return jsonify(response_object)

	if (request.method == 'PUT'):
		post_data = request.get_json()
		followerUsername = post_data.get('followerUsername')
		followeeUsername = post_data.get('followeeUsername')
		acceptedFollow = post_data.get('acceptedfollow')

		query = 'UPDATE Follow SET acceptedfollow = %s WHERE followerUsername = %s AND followeeUsername = %s'
		try:
			with conn.cursor() as cursor:
				cursor.execute(query, (acceptedFollow, followerUsername, followeeUsername))
				conn.commit()
			# cursor.close()
		except Exception as error:
			conn.rollback()
			errno, errmsg = error.args
			response_object['message'] = errmsg
			return jsonify(response_object)
		response_object['message'] = 'Follow Updated!'
		return jsonify(response_object)

@app.route('/unfollow/<follower_username>/<followee_username>', methods = ['DELETE'])
def unfollow(follower_username, followee_username):
	response_object = {'status': 'success'}
	# cursor = conn.cursor()
	query = 'DELETE FROM Follow WHERE followerUsername = %s AND followeeUsername = %s'

	try:
		with conn.cursor() as cursor:
			cursor.execute(query, (follower_username, followee_username))
			conn.commit()
		# cursor.close()
	except Exception as error:
		conn.rollback()
		errno, errmsg = error.args
		response_object['message'] = errmsg
		return jsonify(response_object)
	
	response_object['message'] = 'Follow Request refused'
	return jsonify(response_object)

@app.route('/tag', methods = ['POST', 'GET', 'PUT'])
def tag():
	response_object = {'status': 'success'}
	# cursor = conn.cursor()
	if (request.method == 'POST'):
		post_data = request.get_json()
		username = post_data.get('username')
		photoID = post_data.get('photoID')
		acceptedTag = False
		print(photoID)

		query = 'INSERT INTO Tag (username, photoID, acceptedTag) VALUES (%s, %s, %s)'
		
		try:
			with conn.cursor() as cursor:
				cursor.execute(query, (username, photoID, acceptedTag))
				conn.commit()
			# cursor.close()
		except Exception as error:
			conn.rollback()
			errno, errmsg = error.args
			response_object['errno'] = errno

			if (errno == 1062):
				response_object['message'] = 'Already tagged this user'
			elif (errno == 1452):
				response_object['message'] = 'User does not exist'
			return jsonify(response_object)

		
		response_object['message'] = 'Tag request sent!'

	if (request.method == 'GET'):
		username = request.args['username']
		# query = 'SELECT * FROM Tag WHERE username = %s'
		query = 'SELECT photoOwner, photoID, acceptedTag FROM Tag NATURAL JOIN Photo WHERE username = %s'
		
		with conn.cursor() as cursor:
			cursor.execute(query, username)
		tagRequests = cursor.fetchall()
		# cursor.close()
		
		response_object['Tags'] = tagRequests

	if (request.method == 'PUT'):
		post_data = request.get_json()
		username = post_data.get('username')
		photoID = post_data.get('photoID')
		acceptedTag = post_data.get('acceptedTag')
		print(acceptedTag)

		query = 'UPDATE Tag SET acceptedTag = %s WHERE username = %s AND photoID = %s'
		try:
			with conn.cursor() as cursor:
				cursor.execute(query, (acceptedTag, username, photoID))
				conn.commit()
			# cursor.close()
		except Exception as error:
			conn.rollback()
			errno, errmsg = error.args
			response_object['errno'] = errno
			response_object['message'] = errmsg
			return jsonify(response_object)

		response_object['message'] = 'Tag Request updated!'

	return jsonify(response_object)

@app.route('/tag/<username>/<photo_id>', methods = ['DELETE'])
def unTag(username, photo_id):
	# cursor = conn.cursor()
	response_object = {'status': 'success'}
	query = 'DELETE FROM Tag WHERE username = %s AND photoID = %s'

	try:
		with conn.cursor() as cursor:
			cursor.execute(query, (username, photo_id))
			conn.commit()
		# cursor.close()
	except Exception as error:
		conn.rollback()
		errno, errmsg = error.args
		response_object['errno'] = errno
		response_object['message'] = errmsg
		return jsonify(response_object)

	response_object['message'] = 'Tag declined!'
	return jsonify(response_object)

@app.route('/taglist', methods = ['GET'])
def getTagList():
	response_object = {'status': 'success'}
	photoID = request.args['photoID']
	query = 'SELECT username FROM Tag WHERE photoID = %s AND acceptedTag = 1'

	# cursor = conn.cursor()
	with conn.cursor() as cursor:
		cursor.execute(query, photoID)
	results = cursor.fetchall()
	response_object['tagees'] = results;
	return jsonify(response_object)


@app.route('/group', methods = ['POST', 'PUT', 'GET'])
def all_groups():
	response_object = {'status': 'success'}
	if (request.method == 'POST'):
		# only groupOwner can add group
		post_data = request.get_json()
		username = post_data.get('username')
		groupName = post_data.get('groupName')

		query = 'INSERT INTO CloseFriendGroup (groupName, groupOwner) VALUES (%s, %s)'

		try:
			with conn.cursor() as cursor:
				cursor.execute(query, (groupName, username))
				conn.commit()
			# cursor.close()
		except Exception as error:
		# Q: how to catch other errors? except pymysql.InternalError as error:
			errno, errmsg = error.args
			conn.rollback()
			response_object['errno'] = errno
			response_object['message'] = 'Group already existed'
			return jsonify(response_object)

		# groupOwner belongs to its own group
		query = 'INSERT INTO Belong (groupName, groupOwner, username) VALUES (%s, %s, %s)'
		with conn.cursor() as cursor:
			cursor.execute(query, (groupName, username, username))
			conn.commit()
		response_object['message'] = 'Group added!'

	if (request.method == 'GET'):
		username = request.args['username']
		print(username)

		query = 'SELECT groupName, groupOwner FROM Belong WHERE username = %s'
		try:
			with conn.cursor() as cursor:
				cursor.execute(query, username)
				groups = cursor.fetchall()
				response_object['groups'] = groups
		except Exception as error:
			errmsg = error.args
			print(errmsg)
			# conn.rollback()
			# response_object['errno'] = errno
			# response_object['message'] = errmsg

		
		# cursor.close()

	return jsonify(response_object)

@app.route('/group/add', methods = ['POST'])
def addUser():
	response_object = {'status': 'success'}
	post_data = request.get_json()
	username = post_data.get('username')
	groupName = post_data.get('groupName')
	groupOwner = post_data.get('groupOwner')

	query = 'INSERT INTO Belong (groupName, groupOwner, username) VALUES (%s, %s, %s)'
	# cursor = conn.cursor()
	try:
		with conn.cursor() as cursor:
			cursor.execute(query, (groupName, groupOwner, username))
			conn.commit()
		# cursor.close()
	except Exception as error:
		conn.rollback()
		errno, errmsg = error.args

		if (errno == 1062):
			response_object['message'] = 'User already in the group'
		elif (errno == 1452):
			response_object['message'] = 'User does not exist'
		return jsonify(response_object)
	
	response_object['message'] = 'User added!'
	return jsonify(response_object)

@app.route('/group/<group_name>/<group_owner>/<username>', methods = ['DELETE'])
def removeUser(group_name, group_owner, username):
	response_object = {'status': 'success'}
	print(group_name)
	print(group_owner)
	print(username)
	# cursor = conn.cursor()
	# check if the user is inside the group
	query = 'SELECT * FROM Belong WHERE username = %s AND groupName = %s AND groupOwner = %s'
	with conn.cursor() as cursor:
		cursor.execute(query, (username, group_name, group_owner))
	user = cursor.fetchall()
	if (not user):
		response_object['message'] = 'User does not exist'
		return jsonify(response_object)

	query = 'DELETE FROM Belong WHERE groupName = %s AND groupOwner = %s AND username = %s'
	
	try:
		with conn.cursor() as cursor:
			cursor.execute(query, (group_name, group_owner, username))
			conn.commit()
		# cursor.close()
	except Exception as error:
		conn.rollback()
		errno, errmsg = error.args
		response_object['message'] = errmsg
		return jsonify(response_object)
	response_object['message'] = 'User removed from the group'
	return jsonify(response_object)

@app.route('/like', methods = ['POST'])
def likePhoto():
	response_object = {'status': 'success'}
	post_data = request.get_json()
	username = post_data.get('username')
	photoID = post_data.get('photoID')
	timestamp = datetime.datetime.now()

	query = 'INSERT INTO Liked (username, photoID, timestamp) VALUES (%s, %s, %s)'

	try:
		with conn.cursor() as cursor:
			cursor.execute(query, (username, photoID, timestamp))
			conn.commit()
		message = 'Successfully liked the photo ' + str(photoID)
	except Exception as error:
		conn.rollback()
		errno, message = error.args

		if errno == 1062:
			message = 'You have already liked this photo ' + str(photoID)

	response_object['message'] = message
	return jsonify(response_object)


@app.route('/logout', methods = ['PUT'])
def logout():
	# session.pop('username')
	response_object = {'status': 'success'}
	response_object = {'errno': 0}
	return jsonify(response_object)

if __name__ == '__main__':
	app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
	# app.config['SESSION_TYPE'] = 'filesystem'

	# sess.init_app(app)
	app.run()
	# app.run('127.0.0.1/api', 8080, debug=True)





