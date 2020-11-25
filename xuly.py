import cv2
import numpy as np

class xulys():
	def __init__(self, image):
		self.image = image
	
	def preprocess_input(self, net_h = 416, net_w = 416):

	    new_h, new_w, _ = self.image.shape

	    # determine the new size of the image
	    if (float(net_w)/new_w) < (float(net_h)/new_h):
	        new_h = (new_h * net_w)/new_w
	        new_w = net_w
	    else:
	        new_w = (new_w * net_h)/new_h
	        new_h = net_h

	    # resize the image to the new size
	    resized = cv2.resize(self.image[:,:,::-1]/255., (int(new_w), int(new_h)))

	    # embed the image into the standard letter box
	    new_image = np.ones((net_h, net_w, 3)) * 0.5
	    new_image[int((net_h-new_h)//2):int((net_h+new_h)//2), int((net_w-new_w)//2):int((net_w+new_w)//2), :] = resized
	    new_image = np.expand_dims(new_image, 0)

	    return new_image