import os
import sys

sys.path.append('..')

from model.base_model import BaseModel, draw_boxes
import cv2

print('Please wait while we are loading the model...')

model = BaseModel()

print('We are ready! Please enter the filename (Ctrl + C for exit):')

while True:
	try:
		PATH_TO_IMAGE = input()
	except KeyboardInterrupt:
		break
	
	image = cv2.imread(PATH_TO_IMAGE)
	
	output = model.predict(image)
	image = draw_boxes(image, output, 0.3)
	image = cv2.resize(image, (900, 900))
	
	cv2.imshow('Object detector', image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()