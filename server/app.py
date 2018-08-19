import os
import sys
from PIL import Image
from flask import Flask, request, jsonify
from flask_cors import CORS
from serve import get_model_api

UPLOAD_FOLDER = 'static'

def get_free_filename():
	n = len(os.listdir(UPLOAD_FOLDER))
	return "{}.jpg".format(n)
	
def save_file(img):
	path = '/'.join([UPLOAD_FOLDER, get_free_filename()])
	Image.fromarray(img).save(path)
	return path

app = Flask(__name__)
CORS(app)

model_api = get_model_api()

# API route
@app.route('/api', methods=['POST'])
def api():
	"""API function
	All model-specific logic to be defined in the get_model_api()
	function
	"""
	input_data = request.files['img']
	output_data = model_api(input_data)
	url = save_file(output_data)
	
	return jsonify({
		'url': url
	})

@app.route('/')
def index():
	return "Index API"

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