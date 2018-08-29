import sys

sys.path.append('..')
from model.base_model import BaseModel, draw_boxes
from img_utils import image_to_np_array


def get_model_api():
	model = BaseModel()

	def model_api(image_storage):
		image = image_to_np_array(image_storage)
		output = model.predict(image)
		image = draw_boxes(image, output, 0.8)
		return image

	return model_api