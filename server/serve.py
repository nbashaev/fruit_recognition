#from model.ner_model import NERModel
#from model.config import Config

import io
import sys
import numpy as np

sys.path.append('..')
from model.base_model import BaseModel, draw_boxes
import cv2

def image_to_np_array(img):
	in_memory_file = io.BytesIO()
	img.save(in_memory_file)
	data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
	return cv2.imdecode(data, 1)[:, :, ::-1]

def get_model_api():
	model = BaseModel()

	def model_api(image_storage):
		image = image_to_np_array(image_storage)
		output = model.predict(image)
		image = draw_boxes(image, output, 0.3)
		return image

	return model_api