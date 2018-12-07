from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, join_room, emit
import os
import threading
import uuid
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO, join_room, emit
from werkzeug.utils import secure_filename
import uuid
import pandas as pd
import json
import os,datetime


DEBUG = True

app = Flask(__name__, static_url_path='',
	static_folder='client/dist')
#socketio = SocketIO(app, async_mode='threading')

app.config.from_object(__name__)

CORS(app)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'uploads')
DOWNLOAD_FOLDER = os.path.join(APP_ROOT, 'client/dist/downloads')

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
		'id':"123",
		'title':'Green Eggs and Ham',
		'author':'Dr. seuss',
		'read':True
	}
]

@app.route('/')
def root():
	return app.send_static_file('index.html')

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
	return jsonify('pong!')

@app.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book added!'
    else:
        response_object['books'] = BOOKS
    return jsonify(response_object)

@app.route('/books/<book_id>', methods=['GET', 'POST'])
def one_book(book_id):
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book added!'
    else:
        for book in BOOKS:
            if book['id'] == book_id:
                print(book)
                response_object['books'] = book
    print(response_object)
    return jsonify(response_object)


# @app.route('/books/<book_id>', methods=['PUT', 'DELETE'])
# def single_book(book_id):
#     response_object = {'status': 'success'}
#     if request.method == 'PUT':
#         post_data = request.get_json()
#         remove_book(book_id)
#         BOOKS.append({
#             'id': uuid.uuid4().hex,
#             'title': post_data.get('title'),
#             'author': post_data.get('author'),
#             'read': post_data.get('read')
#         })
#         response_object['message'] = 'Book updated!'
#     if request.method == 'DELETE':
#         remove_book(book_id)
#         response_object['message'] = 'Book removed!'
#     return jsonify(response_object)

def remove_book(book_id):
	#print(book_id)
	for book in BOOKS:
		if book['id'] == book_id:
			BOOKS.remove(book)
			return True
	return False




if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)