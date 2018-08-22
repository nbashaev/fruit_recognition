import os
import io
import sys
import csv   
import pandas as pd
import tensorflow as tf

from PIL import Image
from collections import namedtuple
from object_detection.utils import dataset_util

sys.path.append('..')
from model.labels import label_map_dict

CSV_PATH = '../data/out.csv'
TF_RECORD_PATH = '../data/out.record'


def add_csv_record(data, csv_path):
	exist_flag = os.path.exists(csv_path)
	
	with open(csv_path, 'a+') as f:
		writer = csv.writer(f, lineterminator='\n')
		
		if not exist_flag:
			writer.writerow(['path', 'class', 'xmin', 'ymin', 'xmax', 'ymax'])
		
		for label in data['labels']:
			writer.writerow([data['path'], label['name'], label['xMin'], label['yMin'], label['xMax'], label['yMax']])

def split(df, group):
	data = namedtuple('data', ['path', 'object'])
	gb = df.groupby(group)
	return [data(path, gb.get_group(x)) for path, x in zip(gb.groups.keys(), gb.groups)]


def create_tf_example(group):
	with tf.gfile.GFile(group.path, 'rb') as fid:
		encoded_jpg = fid.read()
	
	encoded_jpg_io = io.BytesIO(encoded_jpg)
	image = Image.open(encoded_jpg_io)
	width, height = image.size

	filename = (group.path.split('\\')[-1]).encode('utf8')
	image_format = b'jpg'
	xmins = []
	xmaxs = []
	ymins = []
	ymaxs = []
	classes_text = []
	classes = []

	for index, row in group.object.iterrows():
		xmins.append(row['xmin'] / width)
		xmaxs.append(row['xmax'] / width)
		ymins.append(row['ymin'] / height)
		ymaxs.append(row['ymax'] / height)
		classes_text.append(row['class'].encode('utf8'))
		classes.append(label_map_dict[row['class']])

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
		'image/object/class/label': dataset_util.int64_list_feature(classes),
	}))
	
	return tf_example


def csv_to_tf_record(input_path, output_path):
	writer = tf.python_io.TFRecordWriter(output_path)
	
	writer = tf.python_io.TFRecordWriter(output_path)
	groups = split(pd.read_csv(input_path), ['path'])
	
	for group in groups:
		tf_example = create_tf_example(group)
		writer.write(tf_example.SerializeToString())
	
	writer.close()

def store_info(data):
	add_csv_record(data, CSV_PATH)

def create_tf_record():
	csv_to_tf_record(CSV_PATH, TF_RECORD_PATH)