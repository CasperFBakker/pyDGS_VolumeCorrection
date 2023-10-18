import os
import tkinter as tk
from tkinter import *
from tkinter import (ALL, BOTH, BOTTOM, END, FLAT, GROOVE, LEFT, NE, NW, RIGHT,
                     SE, SUNKEN, SW, TOP, VERTICAL, YES, Button, Canvas,
                     Checkbutton, E, Entry, Frame, IntVar, Label, Listbox,
                     Menu, N, PhotoImage, S, Scrollbar, StringVar, Text, Tk,
                     Toplevel, W, X, Y, filedialog, ttk)
from tkinter.filedialog import askopenfilename

from natsort import natsorted
from screeninfo import get_monitors

from CoinFinderGUI import GUI


class GetInput(GUI):
    def __init__(self, master, WindFrame, ImpFrame):
        super(GUI,self).__init__()
        self.ImportFrame = ImpFrame
        self.WindowFrame = WindFrame
    
    def get_screen_resolution():
        monitors = get_monitors()
        primary = monitors[0]
        w, h = primary.width, primary.height
        return w, h
    
    def PrintPath(self):
        printPath = Text(self.ImportFrame, height = 2, width = 14, bg = "light gray")
        printPath.insert(END, os.path.basename(self.img_path))
        printPath.configure(state=DISABLED)
        printPath.grid(column=3, row=1)



    def Import_Image(self):#, *args):
        filetypes = [('Images', '*.png *.jpg *.JPG *.jpeg *.heif *.HEIC'),
                     ('Any File', '*.*')]
        self.img_path = askopenfilename(title='Open Image file', filetypes=filetypes, initialdir='Input data/')
        setattr(GetInput.Import_Image, 'img_path', self.img_path)
        self.PrintPath()
        
        self.dir_path = os.path.split(self.img_path)[0] 

        ext = ('.png', '.jpg', '.JPG','.jpeg', '.heif', '.HEIC')
        self.images_list = []
        for files in natsorted(os.listdir(self.dir_path)):
            if files.endswith(ext):
                self.images_list.append(files)  
            else:
                continue
        self.IndexImage = self.images_list.index(os.path.split(self.img_path)[1]) 
        setattr(GetInput.Import_Image, 'IndexImage', self.IndexImage)



    def Next_Image(self, img_nb):
        if img_nb == -2:
            index = self.images_list.index(os.path.split(self.img_path)[1])
            img_nb = index + 1

        self.img_path = self.images_list[img_nb]

        self.PrintPath()

        setattr(GetInput.Import_Image, 'img_path', (self.dir_path + '/' + self.img_path))
        if (img_nb+1) == len(self.images_list):
            img_nb = -1

        self.nextImg = ttk.Button(self.ImportFrame, text="Next") 
        self.nextImg.grid(row=4, column=4)
        self.nextImg.bind("<ButtonRelease-1>", lambda Var: self.Next_Image(img_nb + 1))



    def Previous_Image(self, img_nb):
        if img_nb == -2:
            index = self.images_list.index(os.path.split(self.img_path)[1])
            img_nb = index - 1

        self.img_path = self.images_list[img_nb]

        self.PrintPath()

        setattr(GetInput.Import_Image, 'img_path', (self.dir_path + '/' + self.img_path))
        if (img_nb-1) == -1:
            img_nb = len(self.images_list)

        self.previousImg = ttk.Button(self.ImportFrame, text="Previous") 
        self.previousImg.grid(row=4, column=2)
        self.previousImg.bind("<ButtonRelease-1>", lambda Var: self.Previous_Image(img_nb - 1))
        

    def GetCoinType(self, coin_bank, CoinVar):
        self.coin_type = coin_bank[CoinVar.get()]
        setattr(GetInput.GetCoinType, 'coin_type', self.coin_type)

    def GetBlur(self, val):
        self.ks_blur = int(val)
        setattr(GetInput.GetBlur, 'ks_blur', self.ks_blur)
        return self.ks_blur

    def refreshWindowScale(self):
        self.minR = tk.Scale(self.WindowFrame, from_= 0, to= 500, length=330, width=10, orient='horizontal', command = lambda val: self.SelectMinR(val))
        self.maxR = tk.Scale(self.WindowFrame, from_= 0, to= 500, length=330, width=10, orient='horizontal', command = lambda val: self.SelectMaxR(val))
        self.minR.grid(row=5, column=0, sticky="nsew");     self.maxR.grid(row=6, column=0, sticky="nsew")


    def GetWindowSz(self, WindowVar):
        self.refreshWindowScale()
        self.maxR.configure(state=NORMAL); self.minR.configure(state=NORMAL)
        
        self.WindowSz = WindowVar.get()
        
        self.minR.configure(to=(500 - int(self.WindowSz)))
        self.maxR.configure(from_=(0 + int(self.WindowSz)))

    def SelectMinR(self, val):
        self.minRad = int(val)
        self.maxR.configure(state=NORMAL)
        self.maxR.set(self.minRad + self.WindowSz)
        self.maxR.configure(state=DISABLED)
        setattr(GetInput.SelectMinR, 'MinR', self.minRad)

    def SelectMaxR(self, val):
        self.maxRad = int(val)
        setattr(GetInput.SelectMaxR, 'MaxR', self.maxRad)

    def GetRadiusSp(self, RadiusVar):
        self.RadiusWindow = RadiusVar.get()
        setattr(GetInput.GetRadiusSp, 'RadiusWindow', self.RadiusWindow)

    def GetScale(self, val):
        self.Scale = int(val)
        setattr(GetInput.GetScale, 'Scale', self.Scale)
