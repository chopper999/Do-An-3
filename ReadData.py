import cv2
from PIL import Image
import os
import imutils

class load_video():

	def	__init__(self, path):
		self.path = path
		self.cam = cv2.VideoCapture(self.path)
		__, self.frame = self.cam.read()
		self.cam.release()

	def	show(self):
		cam = cv2.VideoCapture(self.path)
		i = 0
		try:
			while cam.isOpened():
				__, self.frame = cam.read()
				cv2.imshow('frame',self.frame)
				img_item = "frame" + str(i) + ".png"
				cv2.imwrite( "imageFrame/"+ img_item, self.frame)
				if cv2.waitKey(1) &0xFF == ord('q'):
					break
				i = i + 1
		except:
			print("End video!")
		cam.release()
		cv2.destroyAllWindows()

input = load_video('input/MVI_8484.MOV').show()