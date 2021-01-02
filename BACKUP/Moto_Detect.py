
import numpy as np
import argparse
import time
import cv2
import os

class detect_moto():
	def __init__(self, img):
		self.img = img


	def intersection(self,p, q, r, t):
		#print(p,q,r,t)
		(x1, y1) = p
		(x2, y2) = q

		(x3, y3) = r
		(x4, y4) = t

		a1 = y1-y2
		b1 = x2-x1
		c1 = x1*y2-x2*y1

		a2 = y3-y4
		b2 = x4-x3
		c2 = x3*y4-x4*y3

		if(a1*b2-a2*b1 == 0):
			return False
		#print((a1, b1, c1), (a2, b2, c2))
		x = (b1*c2 - b2*c1) / (a1*b2 - a2*b1)
		y = (a2*c1 - a1*c2) / (a1*b2 - a2*b1)
		#print((x, y))

		if x1 > x2:
			tmp = x1
			x1 = x2
			x2 = tmp
		if y1 > y2:
			tmp = y1
			y1 = y2
			y2 = tmp
		if x3 > x4:
			tmp = x3
			x3 = x4
			x4 = tmp
		if y3 > y4:
			tmp = y3
			y3 = y4
			y4 = tmp

		if x >= x1 and x <= x2 and y >= y1 and y <= y2 and x >= x3 and x <= x4 and y >= y3 and y <= y4:
			return True
		else:
			return False


	def run(self, line, net, stopp):
		self.net = net
		self.stopp = stopp

		labelsPath = os.path.sep.join(["yolo-coco", "coco.names"])
		LABELS = open(labelsPath).read().strip().split("\n")


		np.random.seed(42)
		COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
			dtype="uint8")

		try:
			image = self.img
		except:
			print("Can not read image")
		# image = cv2.imread(img)


		(H, W) = image.shape[:2]

		ln = net.getLayerNames()
		ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

		blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
			swapRB=True, crop=False)
		net.setInput(blob)
		start = time.time()
		layerOutputs = net.forward(ln)
		end = time.time()


		print("[INFO] Time load Frame: {:.6f} seconds".format(end - start))


		boxes = []
		confidences = []
		classIDs = []

		for output in layerOutputs:

			for detection in output:

				scores = detection[5:]
				classID = np.argmax(scores)
				confidence = scores[classID]

				if confidence > 0.5: 	#0,5: minimum probability to filter weak detections

					box = detection[0:4] * np.array([W, H, W, H])
					(centerX, centerY, width, height) = box.astype("int")

					x = int(centerX - (width / 2))
					y = int(centerY - (height / 2))


					boxes.append([x, y, int(width), int(height)])
					confidences.append(float(confidence))
					classIDs.append(classID)

		idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.3)	#0.3: threshold when applyong non-maxima suppression


		if len(idxs) > 0:

			for i in idxs.flatten():
				try:
					if LABELS[classIDs[i]] == "motorbike":
					# extract the bounding box 
						(x, y) = (boxes[i][0], boxes[i][1])
						(w, h) = (boxes[i][2], boxes[i][3])
						# draw a bounding box
						tf = False
						if stopp == True:
							# highlight box with intersection = true
							(rxmin, rymin) = (x, y)
							(rxmax, rymax) = (x+w, y+h)

							tf |= self.intersection(line[0], line[1], (rxmin, rymin), (rxmin, rymax))
							tf |= self.intersection(line[0], line[1], (rxmax, rymin), (rxmax, rymax))
							tf |= self.intersection(line[0], line[1], (rxmin, rymin), (rxmax, rymin))
							tf |= self.intersection(line[0], line[1], (rxmin, rymax), (rxmax, rymax))

						if tf:
							color = (255,0,0)
						else: 
							color = [int(c) for c in COLORS[classIDs[i]]]
						cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)

						text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
						cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
							0.5, color, 2)
				except: 
					pass
				
		return image

	