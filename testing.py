from Houghlines_Detect import hough_detect
from Canny_Edge_Detect import Canny_Detect

Can = Canny_Detect()
Can.show('images/5.jpg')
hou = hough_detect('images/5.jpg')
#hou.run()
