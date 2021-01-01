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
        self.stopp = True

        menu = Menu(self.master)
        btn1 = Button(self.master, text='ACTION', fg="green", command = self.client_clickaction)
        btn2 = Button(self.master, text='CANCEL', fg="red", command = self.client_clickcancel)
        self.master.config(menu=menu) # Tạo giao diện menu của tk
        

        # # add menu item
        file = Menu(menu)
        file.add_command(label="Open", command=self.open_file)
        file.add_command(label="Exit", command=self.client_exit)
        menu.add_cascade(label = "Menu",menu = file)

        btn2.pack(side=RIGHT)
        btn1.pack(side=RIGHT, padx=5, pady=5)\

        self.panel = None
        

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

    def client_clickaction(self):
        self.stopp = True

    def client_clickcancel(self):
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
            self.line.clear()
            self.rect.clear()
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

    def main_process(self):

        video_src = self.filename

        labelsPath = os.path.sep.join(["yolo-coco", "coco1.names"])
        LABELS = open(labelsPath).read().strip().split("\n")


        np.random.seed(42)
        COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
            dtype="uint8")


        weightsPath = os.path.sep.join(["yolo-coco", "yolov3.weights"])
        configPath = os.path.sep.join(["yolo-coco", "yolov3.cfg"])


        print("[INFO] loading DATA YOLO ...")
        net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
        cap = cv2.VideoCapture(video_src)
        # convert to a Movie
        reader = imageio.get_reader(video_src)
        fps = reader.get_meta_data()['fps']    
        writer = imageio.get_writer('output\output1.mp4', fps = fps)
            
        j = 1
        while True:
            if j%10 == 0:
                ret, image1 = cap.read()
                if (type(image1) == type(None)):
                    writer.close()
                    break
                det = detect_moto(image1)
                image1 = det.run(self.line, net, self.stopp)

                writer.append_data(image1)
                cv2.imshow('Nhan dien xe vi pham vuot vach den do', image1)

                if cv2.waitKey(10) & 0xFF == ord('q'):
                    writer.close()
                    break

            j = j+1

        cv2.destroyAllWindows()


root = Tk()
app = Window(root)
root.geometry("%dx%d"%(1280, 720))
root.title("Nhan dien xe vi pham")
root.mainloop()
