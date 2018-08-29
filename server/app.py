import os
import sys
import time
from flask import Flask, request, jsonify, render_template, url_for, redirect, session
from flask_cors import CORS

sys.path.append('..')
from model.labels import categories
from save_labels import store_info
from serve import get_model_api
from storage import Storage


app = Flask(__name__)
CORS(app)

app.config['BATCH_SIZE'] = 3
app.config['DATA_FOLDER'] = os.path.join('..', 'data')
app.config['SECRET_KEY'] = b'J\x9dU\x0c\xde\xa2aE\x9b\x0b\xc0W\x17\xcfX\xea'

images_after_inference = Storage('inference')
ulabeled_images = Storage('raw')
model_api = get_model_api()


def get_v():
	return int(time.time())

# Pages
@app.route('/')
def index():
	return render_template('index.html', v=get_v())

@app.route('/label', methods=['GET'])
def label():
	if ('raw_img_url' not in session or session['raw_img_url'] is None):
		return redirect(url_for('index'))
	
	return render_template('label.html', passed_url=session['raw_img_url'], categories=categories, v=get_v())

# API
@app.route('/api/inference', methods=['POST'])
def inference():
	if 'img' not in request.files:
		return user_error('You should upload an image')
	
	input_data = request.files['img']
	output_data = model_api(input_data)
	url = images_after_inference.save_img(output_data)
	
	return jsonify({
		'url': url
	})

@app.route('/api/raw_upload', methods=['POST'])
def raw_upload():
	if 'img' not in request.files:
		return user_error('You should upload an image')
	
	input_data = request.files['img']
	raw_img_url = ulabeled_images.save_img(input_data)
	session['raw_img_url'] = raw_img_url
	
	return redirect(url_for('label'))

@app.route('/api/labeled_upload', methods=['POST'])
def labeled_upload():
	if ('raw_img_url' not in session or session['raw_img_url'] is None):
		return user_error('You should upload an image')
	
	if 'labels' not in request.json:
		return user_error('You should upload your labels')
	
	store_info({
		'path': session['raw_img_url'],
		'labels': request.json['labels']
	})
	
	session['raw_img_url'] = None
	
	return redirect(url_for('index'))

# Errors handlers
def user_error(text):
	return jsonify({
		'error': text
	})

@app.errorhandler(404)
def url_error(e):
	return """
	Wrong URL!
	<pre>{}</pre>""".format(e), 404


@app.errorhandler(500)
def server_error(e):
	return """
	An internal error occurred: <pre>{}</pre>
	See logs for full stacktrace.
	""".format(e), 500


if __name__ == '__main__':
	# This is used when running locally.
	app.run(host='0.0.0.0', debug=True)