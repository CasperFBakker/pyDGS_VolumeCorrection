import tkinter as tk
from tkinter import *
from tkinter import (ALL, BOTH, BOTTOM, END, FLAT, GROOVE, LEFT, NE, NW, RIGHT,
                     SE, SUNKEN, SW, TOP, VERTICAL, YES, Button, Canvas,
                     Checkbutton, E, Entry, Frame, IntVar, Label, Listbox,
                     Menu, N, PhotoImage, S, Scrollbar, StringVar, Text, Tk,
                     Toplevel, W, X, Y, filedialog, ttk)

import cv2
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from matplotlib.figure import Figure
from matplotlib.patches import Circle

from CoinFinderGUI import GUI

class CoinPlots(GUI):
    def __init__(self, master, CoinFrame, TotalFrame):
        super(GUI,self).__init__()
        self.CoinFrame = CoinFrame
        self.TotalFrame = TotalFrame
        setattr(CoinPlots, 'TotalFrame', self.TotalFrame)
        setattr(CoinPlots, 'CoinFrame', self.CoinFrame)

    def draw_coin(self, image, y_coin, x_coin, r_coin):
                 
        cv2.circle(image, (y_coin, x_coin), r_coin, (0, 255, 0), 2) # draw edge of coin
        cv2.circle(image, (y_coin, x_coin), 2, (255, 255, 255), 3) # draw center of coin

        return image
        

    def CoinPlot(self, img_og, y_coin, x_coin, r_coin):
        image_coin = CoinPlots.draw_coin(self, img_og, y_coin, x_coin, r_coin)

        fig = plt.figure(figsize=(5,5))
        fig.add_subplot(111).imshow(image_coin)

        f0 = ttk.Frame(CoinPlots.TotalFrame)
        canvas = FigureCanvasTkAgg(fig, f0)
        toolbar = NavigationToolbar2Tk(canvas, f0)
        toolbar.update()

        canvas._tkcanvas.pack(side=LEFT, fill=BOTH, expand=True)
        f0.place(x=90, y=40)
        return image_coin

    def CropCoinPlot(self, image, y_coin, x_coin, r_coin):
        crop_image = image[(x_coin - 50 - r_coin): (x_coin + 50 + r_coin),
                           (y_coin - 50 - r_coin):(y_coin + 50 + r_coin)]
        nx, ny, _ = np.shape(crop_image)
        XCenter = int(nx/2); YCenter = int(ny/2)
        
        fig = Figure(figsize=(6,6))
        fig.subplots_adjust(0,0,1,1,0,0)

        ax = fig.add_subplot(111)
        ax.imshow(crop_image)

        f0 = ttk.Frame(CoinPlots.CoinFrame)
        canvas = FigureCanvasTkAgg(fig, f0)
        canvas._tkcanvas.grid(row=0, column=0)


        fig.canvas.draw()

        self.r_slider = tk.Scale(f0,variable=tk.IntVar(), from_=-100, 
                    to=100, label='Fine-tune Radius', 
                    orient=tk.HORIZONTAL,length=int(fig.bbox.width), 
                    width=int(fig.bbox.height * 0.05), command = 
                    lambda i : CoinPlots.update(self, crop_image, XCenter, YCenter, r_coin, ax, fig, canvas))
        self.r_slider.set(0)
        self.r_slider.grid(row=1, column=0)

        self.x_slider = tk.Scale(f0,variable=tk.IntVar(), from_=-100, 
                    to=100, label='Fine-tune x-position', 
                    orient=tk.HORIZONTAL,length=int(fig.bbox.width), 
                    width=int(fig.bbox.height * 0.05), command = 
                    lambda i : CoinPlots.update(self, crop_image, XCenter, YCenter, r_coin, ax, fig, canvas))
        self.x_slider.set(0)
        self.x_slider.grid(row=2, column=0)

        self.y_slider = tk.Scale(f0,variable=tk.IntVar(), from_=-100, 
                    to=100, label='Fine-tune y-position', 
                    orient=tk.HORIZONTAL,length=int(fig.bbox.width), 
                    width=int(fig.bbox.height * 0.05), command = 
                    lambda i : CoinPlots.update(self, crop_image, XCenter, YCenter, r_coin, ax, fig, canvas))
        self.y_slider.set(0)
        self.y_slider.grid(row=3, column=0)

        f0.place(x=8, y=10)
        setattr(CoinPlots.update, 'r_coin', (r_coin))



    def update(self, image, XCenter, YCenter, r_coin, ax, fig, canvas):
        
        r = self.r_slider.get()
        x = self.x_slider.get()
        y = self.y_slider.get()

        ax.clear()
        ax.imshow(image)

        ax.add_patch(Circle(((x + XCenter),(y + YCenter)), (r + r_coin), fill=False, color="red"))
        ax.add_patch(Circle(((x + XCenter),(y + YCenter)), 2, fill=True, color="black"))
        ax.plot([(XCenter+x-r_coin-r), (x+XCenter+r_coin+r)], [(y+YCenter), (y+YCenter)], color="red", linestyle="--")
        ax.plot([(XCenter+x), (x+XCenter)], [(y+YCenter-r_coin-r), (y+YCenter+r_coin+r)], color="red", linestyle="--")
        fig.canvas.draw()
        setattr(CoinPlots.update, 'r_final', (r+r_coin))