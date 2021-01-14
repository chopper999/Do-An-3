from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog

import imageio
import cv2
from Moto_Detect import detect_moto
import numpy as np
import os


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.pos = []
        self.line = []
        self.rect = []
        self.master.title("GUI")

        self.pack(fill=BOTH, expand=1) 

        self.counter = 0
        self.sec = 0
        self.stopp = True

        #tạo menu
        menu = Menu(self.master)
        self.master.config(menu=menu)
        
        # # add menu item
        file = Menu(menu)
        file.add_command(label="Open", command=self.open_file)
        file.add_command(label="Exit", command=self.client_exit)
        menu.add_cascade(label = "Menu",menu = file)

        #tạo button
        btn1 = Button(self.master, text='ĐÈN ĐỎ', fg="red", command = self.client_clickred)
        btn2 = Button(self.master, text='ĐÈN XANH', fg="green", command = self.client_clickgreen)
        btn3 = Button(self.master, text='BẮT ĐẦU', fg="green", command = self.main_process)

        inputtxt = Text(self.master, height = 1, 
                width = 10, 
                bg = "light yellow")

        inputtxt.pack(side=RIGHT)
        btn2.pack(side=RIGHT)
        btn1.pack(side=RIGHT, padx=5, pady=5)
        btn3.pack(side=RIGHT, padx=5, pady=5)


        # # add hình nền
        self.filename = "images/3.jpg"
        self.imgSize = Image.open(self.filename)
        self.tkimage =  ImageTk.PhotoImage(self.imgSize) #Tham số truyền vào cho ImageTk là image
        self.w, self.h = (1920, 1080)
        
        self.canvas = Canvas(master = root, width = self.w, height = self.h)
        self.canvas.create_image(20, 20, image=self.tkimage, anchor='nw') 
        self.canvas.pack()


    def open_file(self):
        self.filename = filedialog.askopenfilename()
        cap = cv2.VideoCapture(self.filename)
        reader = imageio.get_reader(self.filename)
        fps = reader.get_meta_data()['fps']
        
        ret, image = cap.read()
        
        
        # show frame[0] của video đầu vào để vẽ đường thẳng
        cv2.imwrite('images\image0.jpg', image)
        self.show_image('images\image0.jpg')

        root.config(cursor="target")

        self.canvas.bind("<Button-1>", self.imgClick)


    def client_exit(self):
        exit()

    def client_clickred(self):
        self.stopp = True

    def client_clickgreen(self):
        self.stopp = False


    def imgClick(self, event):

        if self.counter < 2:
            x = int(self.canvas.canvasx(event.x))
            y = int(self.canvas.canvasy(event.y))
            self.line.append((x, y))
            self.pos.append(self.canvas.create_line(x - 5, y, x + 5, y, fill="red", tags="crosshair"))
            self.pos.append(self.canvas.create_line(x, y - 5, x, y + 5, fill="red", tags="crosshair"))
            self.counter += 1

        if self.counter == 2:
            self.canvas.unbind("<Button-1>") # Nếu đã vẽ đủ 2 điểm thì ngưng gọi event mouse-click
            root.config(cursor="arrow")
            self.counter = 0

            img = cv2.imread('images\image0.jpg')
            cv2.line(img, self.line[0], self.line[1], (0, 255, 0), 3)
            cv2.imwrite('images\_afterdraw.jpg', img)
            self.show_image('images\_afterdraw.jpg')


            #image processing
            #self.main_process() 
            
            #clearing things
            #self.line.clear()
            #self.rect.clear()
            for i in self.pos:
                self.canvas.delete(i)

    def show_image(self, frame):
        self.imgSize = Image.open(frame)
        self.tkimage =  ImageTk.PhotoImage(self.imgSize)
        self.w, self.h = (1920, 1080)

        self.canvas.destroy()

        self.canvas = Canvas(master = root, width = self.w, height = self.h)
        self.canvas.create_image(0, 0, image=self.tkimage, anchor='nw')
        self.canvas.pack()


    def show_frame(self, frame):

        #Graphics window
        imageFrame = Frame(master = root, width=600, height=500)
        imageFrame.grid(row=0, column=0, padx=10, pady=2)


        display1 = Label(imageFrame)
        display1.grid(row=1, column=0, padx=10, pady=2)  #Display 1

        self.frame = frame
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        display1.imgtk = imgtk #Shows frame for display 1
        display1.configure(image=imgtk)
        window.after(10, show_frame)


    def main_process(self):

        video_src = self.filename
        secs = 0
        X = 0
        weightsPath = os.path.sep.join(["yolo-coco", "yolov3.weights"])
        configPath = os.path.sep.join(["yolo-coco", "yolov3.cfg"])

        print("[INFO] loading DATA YOLO ...")
        net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)


        cap = cv2.VideoCapture(video_src)

        frame_width = int(cap.get(3)) 
        frame_height = int(cap.get(4)) 
        size = (frame_width, frame_height) 

        reader = imageio.get_reader(video_src)
        fps = reader.get_meta_data()['fps']    
        result = cv2.VideoWriter('output/outputvideo.avi',  
                         cv2.VideoWriter_fourcc(*'MJPG'), 
                         fps, size)

            
        det = detect_moto()
        while True:
            ret, image1 = cap.read()
            if (type(image1) == type(None)):
                break
            index = X

            image1, secs = det.run(self.line,image1, net, fps)
            X = round(secs + index, 2)
            det.setsecs(X)
            a = det.getsecs()
            
            print(a)
            result.write(image1)

            cv2.imshow('Nhan dien xe vi pham vuot vach den do', image1)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break


        cv2.destroyAllWindows()

root = Tk()
app = Window(root)
root.geometry("%dx%d"%(1080, 720))
root.title("Nhan dien xe vi pham")

root.mainloop()