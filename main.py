#from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog

import imageio
import cv2

import numpy as np
import os

from DrawLine import Window



root = tk.Tk()
app = Window(root)
root.geometry("%dx%d"%(1280, 720))
root.title("Nhan dien xe vi pham")
root.mainloop()
