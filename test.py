from Canny_Edge_Detect import Auto_Canny
from Canny_Edge_Detect import Canny_Detect
import cv2
import numpy as np
import math

path = '4.jpg'
# Canny_Detect().show(path)
Canny_Detect()
# edges = Auto_Canny.auto_canny(path)
img = cv2.imread('4.jpg')
# convert to gray scale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # color -> gray
edges = Canny_Detect().get_egde(path)
lines = cv2.HoughLines(edges, rho=1, theta=np.pi/180, threshold=190)
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

img = cv2.resize(img, dsize=(600, 600))
cv2.imshow("Result Image", img)

if cv2.waitKey(0) & 0xff == 27:  
    cv2.destroyAllWindows()




# for i in range(100,211):
#     lines = cv2.HoughLines(edges, rho=1, theta=np.pi/180, threshold=i)
#     for line in lines:
#         rho, theta = line[0]
#         a = np.cos(theta)
#         b = np.sin(theta)
#         x0 = a*rho
#         y0 = b*rho
#         x1 = int(x0 + 1000*(-b))
#         y1 = int(y0 + 1000*(a))
#         x2 = int(x0 - 1000*(-b))
#         y2 = int(y0 - 1000*(a))
#         returnImage = cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2) 
#     img_item = "image" + str(i) + ".png"
#     returnImage = cv2.resize(returnImage, dsize=(600, 600))
#     cv2.imwrite( "imageTest/"+ img_item, returnImage)   
    


    # cv2.imwrite('geo_hough.jpg',img)




# import numpy as np
# import cv2
# from matplotlib import pyplot as plt
# from matplotlib import image as image

# img = cv2.imread('4.jpg', cv2.IMREAD_COLOR)
# # Convert the image to gray-scale
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# # Find the edges in the image using canny detector
# edges = cv2.Canny(gray, 50, 200)
# # Detect points that form a line
# lines = cv2.HoughLinesP(edges, 3, np.pi/180, 400, minLineLength=5, maxLineGap=500)
# # Draw lines on the image
# maxLenLine = 0
# maxLine = lines[0]
# # for i in range(0,len(lines)):
# #     x1, y1, x2, y2 = lines[i]
# #     if abs(x2-x1) >= maxLenLine:
# #         maxLenLine = abs(x2-x1)
# #         maxLine = lines[i]

# # x1, y1, x2, y2,s,a = maxLine
# # cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 1)
# # Canny_Detect().show('4.jpg')
# for line in lines:
#     x1, y1, x2, y2 = line[0]
#     cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 1)


