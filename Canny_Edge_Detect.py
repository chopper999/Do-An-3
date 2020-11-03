# import the necessary packages
import numpy as np
import argparse
import glob
import cv2
import imutils

class Auto_Canny():

	def auto_canny( self, image, sigma=0.33):
		v = np.median(image)
		lower = int(max(0, (1.0 - sigma) * v))
		upper = int(min(255, (1.0 + sigma) * v))
		self.edged = cv2.Canny(image, lower, upper)
		return self.edged


class Canny_Detect():

	def show(self, path):
		au = Auto_Canny()
		for imagePath in glob.glob(path):
			image = cv2.imread(imagePath)
			image = imutils.resize(image, width=600)
			gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			blurred = cv2.GaussianBlur(gray, (3, 3), 0)

			wide = cv2.Canny(blurred, 10, 200)
			tight = cv2.Canny(blurred, 225, 250)
			auto = au.auto_canny(blurred)
			# show
			cv2.imshow("Original", image)
			cv2.imshow("Edges", np.hstack([wide]))
			
			cv2.waitKey(0)


	def get_egde(self,path):
		au = Auto_Canny()
		for imagePath in glob.glob(path):
			image = cv2.imread(imagePath)
			# image = imutils.resize(image, width=600)
			gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			blurred = cv2.GaussianBlur(gray, (3, 3), 0)

			self.wide = cv2.Canny(blurred, 10, 200)
			self.tight = cv2.Canny(blurred, 225, 250)
			self.auto = au.auto_canny(blurred)

			return np.hstack([self.wide])
			

