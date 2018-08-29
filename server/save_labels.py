import os
import io
import sys

from PIL import Image
import tensorflow as tf
from object_detection.utils import dataset_util

sys.path.append('..')

from model.labels import label_map_dict
from db import get_db_wrapper


DATA_FOLDER = '../data'
BATCH_SIZE = 100


def create_tf_example(img_path, group):
	with tf.gfile.GFile(img_path, 'rb') as fid:
		encoded_jpg = fid.read()
	
	encoded_jpg_io = io.BytesIO(encoded_jpg)
	img = Image.open(encoded_jpg_io)
	width, height = img.size

	filename = (img_path.split('\\')[-1]).encode('utf8')
	image_format = b'jpg'
	xmins = []
	xmaxs = []
	ymins = []
	ymaxs = []
	classes_text = []
	classes = []

	for row in group:
		classes_text.append(row['class'].encode('utf8'))
		classes.append(label_map_dict[row['class']])
		xmins.append(row['xmin'] / width)
		xmaxs.append(row['xmax'] / width)
		ymins.append(row['ymin'] / height)
		ymaxs.append(row['ymax'] / height)
	
	tf_example = tf.train.Example(features=tf.train.Features(feature={
		'image/height': dataset_util.int64_feature(height),
		'image/width': dataset_util.int64_feature(width),
		'image/filename': dataset_util.bytes_feature(filename),
		'image/source_id': dataset_util.bytes_feature(filename),
		'image/encoded': dataset_util.bytes_feature(encoded_jpg),
		'image/format': dataset_util.bytes_feature(image_format),
		'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
		'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
		'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
		'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
		'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
		'image/object/class/label': dataset_util.int64_list_feature(classes)
	}))
	
	return tf_example


def create_tf_record(db_wrapper, path_list, output_path):
	writer = tf.python_io.TFRecordWriter(output_path)
	
	for img_path in path_list:
		group = db_wrapper.get_group_by_path(img_path)
		tf_example = create_tf_example(img_path, group)
		writer.write(tf_example.SerializeToString())
	
	writer.close()


def store_info(data):
	db_wrapper = get_db_wrapper()
	db_wrapper.add_record(data['path'], data['labels'])
	
	path_list = db_wrapper.get_all_paths()
	n = len(path_list)
	
	if n % BATCH_SIZE == 0:
		output_path = os.path.join(DATA_FOLDER, 'data_{0}.record'.format(n // BATCH_SIZE))
		create_tf_record(db_wrapper, path_list[-BATCH_SIZE:], output_path)