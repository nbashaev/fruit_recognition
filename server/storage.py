import os
import string
import random
from img_utils import save_img_multitype

class Storage:
	def __init__(self, path, id_len=6):
		self.upload_path = '/'.join(['static', path])
		self.id_len = id_len
		
		if not os.path.exists(self.upload_path):
			os.makedirs(self.upload_path)
	
	def get_random_id(self):
		chars = string.ascii_lowercase + string.digits
		return ''.join(random.choices(chars, k=self.id_len))
	
	def get_free_filename(self):
		filename = None
		
		while (filename is None or filename in os.listdir(self.upload_path)):
			filename = "{}.jpg".format(self.get_random_id())
		
		return filename
	
	def save_img(self, img):
		path = '/'.join([self.upload_path, self.get_free_filename()])
		save_img_multitype(img, path)
		
		return path