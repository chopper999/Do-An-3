
from DetectColorPY.shapedetector import ShapeDetector
from DetectColorPY.colorlabeler import ColorLabeler
import argparse
import imutils
import cv2

class detect_color():
	def det_color(self, image,xx,yy):
		self.image = image

		w = 70
		x = xx-w
		y = 0
		h = 80

		#image = cv2.imread(image)
		image = image[y:y+h, x:x+w]
		resized = imutils.resize(image, width=300)

		blurred = cv2.GaussianBlur(resized, (5, 5), 0)
		gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
		lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)
		thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]
		#cv2.imshow("thresh", thresh)

		# find 
		cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)

		#sd = ShapeDetector()
		cl = ColorLabeler()

		# loop over the contours
		for c in cnts:

			color = cl.label(lab, c)
			if color =="red" or color =="green"or color == "yellow":
				text = "{}".format(color)
				cv2.drawContours(resized, [c], -1, (0, 255, 0), 2)

				cv2.imshow("Image", resized)
				#cv2.waitKey(0)
				return text