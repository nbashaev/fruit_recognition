import os
from utils import label_map_util

dirname = os.path.dirname(os.path.realpath(__file__))

PATH_TO_LABELS = os.path.join(dirname, 'label_map.pbtxt')
NUM_CLASSES = 6

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
label_map_dict = label_map_util.get_label_map_dict(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)