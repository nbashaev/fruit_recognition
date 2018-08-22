import os
import sys
import time
from flask import Flask, request, jsonify, render_template, url_for, redirect, session
from flask_cors import CORS
from save_labels import store_info, create_tf_record
from serve import get_model_api
from storage import Storage

sys.path.append('..')
from model.labels import categories

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = b'J\x9dU\x0c\xde\xa2aE\x9b\x0b\xc0W\x17\xcfX\xea'

model_api = get_model_api()

images_after_inference = Storage('inference')
ulabeled_images = Storage('raw')

# Index
@app.route('/')
def index():
	return render_template('index.html')

# API
@app.route('/api/inference', methods=['POST'])
def inference():
	input_data = request.files['img']
	output_data = model_api(input_data)
	url = images_after_inference.save_img(output_data)
	
	return jsonify({
		'url': url
	})

@app.route('/api/raw_upload', methods=['POST'])
def raw_upload():
	input_data = request.files['img']
	raw_img_url = ulabeled_images.save_img(input_data)
	session['raw_img_url'] = raw_img_url
	
	return redirect(url_for('label'))

@app.route('/api/labeled_upload', methods=['POST'])
def labeled_upload():
	store_info({
		'path': session['raw_img_url'],
		'labels': request.json['labels']
	})
	
	session['raw_img_url'] = None
	
	return redirect(url_for('label'))

# Label images page
@app.route('/label', methods=['GET'])
def label():
	if (not 'raw_img_url' in session or session['raw_img_url'] is None):
		return render_template('choose_image.html')
	
	return render_template('label.html', passed_url=session['raw_img_url'], categories=categories, v=int(time.time()))

# HTTP Errors handlers
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