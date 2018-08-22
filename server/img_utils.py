from PIL import Image
import numpy as np
import cv2
import io

def image_to_np_array(img):
	in_memory_file = io.BytesIO()
	img.save(in_memory_file)
	data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
	return cv2.imdecode(data, 1)[:, :, ::-1]

def save_img_multitype(img, path):
	if type(img) is np.ndarray:
		Image.fromarray(img).save(path)
	else:
		img.save(path)