from tkinter import *
import cv2.cv as cv

root = Tk()

w = Canvas(root, width=500, height=300, bd = 10, bg = 'white')
w.grid(row = 0, column = 0, columnspan = 2)

b = Button(width = 10, height = 2, text = 'Button1')
b.grid(row = 1, column = 0)
b2 = Button(width = 10, height = 2, text = 'Button2')
b2.grid(row = 1,column = 1)

cv.NamedWindow("camera",1)
capture = cv.CaptureFromCAM(0)

while True:
    img = cv.QueryFrame(capture)
    canvas.create_image(0,0, image=img)
    if cv.WaitKey(10) == 27:
        break

root.mainloop()