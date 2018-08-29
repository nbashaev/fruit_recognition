import os
import sys
import numpy as np

import tensorflow as tf
from utils import visualization_utils as vis_util
from model.labels import category_index

def get_model_name():
	fin = open(PATH_TO_VERSION, 'r')
	name = '{}.pb'.format(fin.readline())
	fin.close()
	
	return name


dirname = os.path.dirname(os.path.realpath(__file__))
PATH_TO_VERSION = os.path.join(dirname, 'model_version.txt')
PATH_TO_CKPT = os.path.join(dirname, 'inference_graph', get_model_name())


class BaseModel():
	def __init__(self):
		detection_graph = tf.Graph()

		with detection_graph.as_default():
			od_graph_def = tf.GraphDef()
			
			with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
				serialized_graph = fid.read()
				od_graph_def.ParseFromString(serialized_graph)
				tf.import_graph_def(od_graph_def, name='')
			
			self.sess = tf.Session(graph=detection_graph)
		
		self.image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
		self.detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
		self.detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
		self.detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
		self.num_detections = detection_graph.get_tensor_by_name('num_detections:0')
		
		self.__predict_raw(np.ndarray(shape=(1,224,224,3), dtype=float, order='F'))
	
	def __prepare_input(self, img):
		return np.expand_dims(img, axis=0)
	
	def __predict_raw(self, img):
		return self.sess.run(
			[self.detection_boxes, self.detection_scores, self.detection_classes, self.num_detections],
			feed_dict={self.image_tensor: img}
		)
	
	def predict(self, img):
		expanded_img = self.__prepare_input(img)
		boxes, scores, classes, num = self.__predict_raw(expanded_img)
		
		return {
			'boxes': boxes,
			'scores': scores,
			'classes': classes,
			'num': num
		}


def draw_boxes(img, output, threshold):
	vis_util.visualize_boxes_and_labels_on_image_array(
		img,
		np.squeeze(output['boxes']),
		np.squeeze(output['classes']).astype(np.int32),
		np.squeeze(output['scores']),
		category_index,
		use_normalized_coordinates=True,
		line_thickness=8,
		min_score_thresh=threshold
	)
	
	return img