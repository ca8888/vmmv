
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO, join_room, emit
from werkzeug.utils import secure_filename
import uuid
import pandas as pd
import json
import os,datetime


#configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)

socketio = SocketIO(app, async_mode='threading')

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'uploads')
DOWNLOAD_FOLDER = os.path.join(APP_ROOT, 'downloads')

try:
	os.mkdir( UPLOAD_FOLDER )
except:
	print("Cannot create a file when that file already exists")

try:
	os.mkdir( DOWNLOAD_FOLDER )
except:
	print("Cannot create a file when that file already exists")	
	
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.from_object(__name__)

# enable CORS
CORS(app)



#
def uploadS3(newFileName,):
    data = open(os.path.join(app.config['UPLOAD_FOLDER'], newFileName), 'rb')
    print(data)
    bucket.put_object(Key=newFileName,Body=data)

# AWS IoT --------------------------------------------------------------------

# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("Received a new message")
    print(message.payload)
    message_object = message.payload.decode("utf-8")
    print(message_object)
    message_string = json.dumps(message_object)
    print(message_string)
    message_object = json.loads(message_string)
    print(message_object)
    socketio.emit('mqtt_recieve', message_string, broadcast=True)

@socketio.on('mqtt_send')
def on_publish_message(data):
	print(data)
	str_bytes = json.dumps({"message": data}, ensure_ascii=False)
	print(str_bytes)
	myAWSIoTMQTTClient.publish("myTopic", str_bytes, 0)

identityPoolID = "ap-northeast-2:35fe7f77-ab96-4859-9cc7-cef69a14082b"
#identityPoolID = "ap-northeast-2:44344e93-866a-4fe2-ace9-4d109221b0b5"
region = "ap-northeast-2"
cognitoIdentityClient = boto3.client('cognito-identity', region_name=region)
print(cognitoIdentityClient)

temporaryIdentityId = cognitoIdentityClient.get_id(IdentityPoolId=identityPoolID)
identityID = temporaryIdentityId["IdentityId"]
print(identityID)

temporaryCredentials = cognitoIdentityClient.get_credentials_for_identity(IdentityId=identityID)
AccessKeyId = temporaryCredentials["Credentials"]["AccessKeyId"]
SecretKey = temporaryCredentials["Credentials"]["SecretKey"]
SessionToken = temporaryCredentials["Credentials"]["SessionToken"]
print(AccessKeyId)
print(SecretKey)
print(SessionToken)

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = AWSIoTMQTTClient(uuid.uuid4().hex, useWebsocket=True)

# AWSIoTMQTTClient configuration
myAWSIoTMQTTClient.configureEndpoint("a1ujn2kua1jvm.iot.ap-northeast-2.amazonaws.com", 443)
myAWSIoTMQTTClient.configureCredentials("./cert/VeriSign-Class 3-Public-Primary-Certification-Authority-G5.pem")
myAWSIoTMQTTClient.configureIAMCredentials(AccessKeyId, SecretKey, SessionToken)
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
myAWSIoTMQTTClient.subscribe("myTopic", 1, customCallback)

print("Success!!!!!!!!!!")

ROOMS = {}

BOOKS = [	
	{
		'id':uuid.uuid4().hex,
		'title':'On the Road',
		'author':'Jack Kerouac',
		'read':True
	},
	{
		'id':uuid.uuid4().hex,
		'title':'Harry Potter and the Philosopher\'s Stone',
		'author':'J. K. Rowling',
		'read':False
	},
	{
		'id':uuid.uuid4().hex,
		'title':'Green Eggs and Ham',
		'author':'Dr. seuss',
		'read':True
	}
]

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
	return jsonify('pong!')
	
user = 'aloncohn'
password = 'printstatBR8102'
host_product = 'BR-B-DB02.BIGREP.LOCAL'
#host_product = '192.168.246.53'
dbname = 'printstat'
port = '5432'
product = None
pc = None

try:
	product = psycopg2.connect(host=host_product, user=user, password=password, dbname=dbname)
	print(product)
	pc = product.cursor()
except:
	print("do not connect to the database")

@app.route('/print_report', methods=['GET'])
def all_print_reports():
	response_object = {'status':'success'}
	result_df = pd.read_sql("select * from print_report_temp", product)
	dict = result_df.to_dict(orient='records')
	jsonObj = json.dumps(dict)
	response_object['results'] = json.loads(jsonObj)
	return jsonify(response_object)

@app.route('/print_report/download', methods=['GET'])
def download_print_reports():
	filename = uuid.uuid4().hex+".csv"
	result_df = pd.read_sql("select * from print_report_temp", product)
	result_df.to_csv(DOWNLOAD_FOLDER+'/'+filename, encoding="utf-8", index=False)
	return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)
	
@app.route('/simplify3d', methods=['GET'])
def all_simplify3d():
	response_object = {'status':'success'}
	result_df = pd.read_sql("select * from bigrep_simplify3d", product)
	dict = result_df.to_dict(orient='records')
	jsonObj = json.dumps(dict)
	response_object['results'] = json.loads(jsonObj)
	return jsonify(response_object)	
	
@app.route('/books', methods=['GET', 'POST'])
def all_books():
	response_object = {'status':'success'}
	if request.method == 'POST':
		post_data = request.get_json()
		BOOKS.append({
			'id':uuid.uuid4().hex,
			'title':post_data.get('title'),
			'author':post_data.get('author'),
			'read':post_data.get('read')
		})
		response_object['message'] = 'Book added!'
	else:
		response_object['books'] = BOOKS
	return jsonify(response_object)
	
@app.route('/books/<book_id>', methods=['PUT', 'DELETE'])
def single_book(book_id):
	response_object = {'status':'success'}
	if request.method == 'PUT':
		post_data = request.get_json()
		remove_book(book_id)
		BOOKS.append({
			'id':uuid.uuid4().hex,
			'title':post_data.get('title'),
			'author':post_data.get('author'),
			'read':post_data.get('read')
		})
		response_object['message'] = 'Book updated!'
	if request.method == 'DELETE':
		remove_book(book_id)
		response_object['message'] = 'Book removed!'
	return jsonify(response_object)

#Upload
@app.route('/upload',methods=['GET','POST'])
def uploadFile():
    response_object = {'status':'success'}
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        print(filename)
        # Gen GUUID File Name
        fileExt = filename.split('.')[1]
        autoGenFileName = uuid.uuid4()
        newFileName = str(autoGenFileName) + '.' + fileExt
        print(newFileName)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], newFileName)    )
		#Upload AWS S3
        uploadS3(newFileName)
        return jsonify(response_object)
	
def remove_book(book_id):
	#print(book_id)
	for book in BOOKS:
		if book['id'] == book_id:
			BOOKS.remove(book)
			return True
	return False

@socketio.on('create')
def on_create(data):
	room = uuid.uuid4.hex
	ROOMS[room] = {}
	join_room(room)
	emit('join_room', {'room',room})

@socketio.on('hello_world')
def on_hello_world(data):
	print(data)
	emit('hello_world', 'Hello, World!')
	
if __name__ == '__main__':
	#app.run(debug=True)
	socketio.run(app, debug=True)