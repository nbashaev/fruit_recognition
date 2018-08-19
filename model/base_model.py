import os
import sys
import numpy as np

import tensorflow as tf

from utils import label_map_util
from utils import visualization_utils as vis_util


dirname = os.path.dirname(os.path.realpath(__file__))

PATH_TO_CKPT = os.path.join(dirname, 'inference_graph', 'frozen_inference_graph.pb')
PATH_TO_LABELS = os.path.join(dirname, 'label_map.pbtxt')

NUM_CLASSES = 6


label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

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
	
	def prepare_input(self, img):
		return np.expand_dims(img, axis=0)
	
	def predict_raw(self, img):
		return self.sess.run(
			[self.detection_boxes, self.detection_scores, self.detection_classes, self.num_detections],
			feed_dict={self.image_tensor: img}
		)
	
	def predict(self, img):
		expanded_img = self.prepare_input(img)
		boxes, scores, classes, num = self.predict_raw(expanded_img)
		
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