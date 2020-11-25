import cv2
import numpy as np
import imutils

from Canny_Edge_Detect import Canny_Detect

can = Canny_Detect()

img = can.get_image('images/3.jpg')
# Convert the image to gray-scale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Find the edges in the image using canny detector
#edges = cv2.Canny(gray, 50, 200)
edges = can.get_egde('images/3.jpg')
# Detect points that form a line
lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=100, maxLineGap=50)
# Draw lines on the image
for line in lines:
    x1, y1, x2, y2 = line[0]
    cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 1)

# Show result
#img = imutils.resize(img, width=600)
cv2.imshow("Result Image", edges)

if cv2.waitKey(0) & 0xff == 27:  
    cv2.destroyAllWindows()