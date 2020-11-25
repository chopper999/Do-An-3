#from Houghlines_Detect import hough_detect
#from Canny_Edge_Detect import Canny_Detect


from Moto_Detect import detect_moto
import cv2

Can = Canny_Detect()
#Can.show('images/5.jpg')
hou = hough_detect('images/5.jpg')
#hou.run()
det = detect_moto('images/5.jpg')
img = det.run()
cv2.imshow("Image", img)
cv2.waitKey(0)
