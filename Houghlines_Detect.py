
from Canny_Edge_Detect import Canny_Detect
import cv2
import numpy as np
import math

class hough_detect():
    def __init__(self,path):
        self.path = path

    def run(self):

        ca = Canny_Detect()

        img = cv2.imread(self.path)

        edges = ca.get_egde(self.path)
        lines = cv2.HoughLines(edges, rho=1, theta=np.pi/180, threshold=210)
        for line in lines:
            rho, theta = line[0]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))
            cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2) 


        # Show result
        #img = cv2.resize(img, dsize=(640,480))
        cv2.imshow("Result Image", img)

        if cv2.waitKey(0) & 0xff == 27:  
            cv2.destroyAllWindows()


  