import numpy as np
import cv2 
import tkinter as tk
import time
import matplotlib.pyplot as plt

from Classes.GetInput import GetInput as Input
from Classes.CoinPlot import CoinPlots as Cplt

class CoinDetector():

    def moving_r_window(image, RadiusWindow, minRadius, maxRadius):
        coin = 1
        timeout = time.time() + 10
        while np.size(coin) != 3:
            coin = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 1, 120, param1=50, param2=30, 
                                            minRadius=minRadius, maxRadius=maxRadius)
            [minRadius, maxRadius] = [minRadius + RadiusWindow, maxRadius + RadiusWindow]
            if time.time() > timeout: # Set timer of 10s, to prevent endless loop
                tk.messagebox.showwarning(title='Error, Coin Not Found', 
                                        message='Cannot distinguish the coin from image. Recommended: change kernel size of median blur.')
                raise Exception("Cannot distinguish the coin from image."  
                                "Recommended: change kernel size of median blur.") from None
                break

        return coin


    def Coin_Dector(self, img_path, ks_blur, RadiusWindow, minRadius, maxRadius):

        img = cv2.imread(img_path, cv2.IMREAD_COLOR) # Read the image 

        img_og = img.copy()                              # Make copy of image
        img_og = cv2.cvtColor(img_og, cv2.COLOR_BGR2RGB) # Converting the image to RGB pattern (default = BGR)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Grayscale image
        img = cv2.medianBlur(img, ks_blur) # Blur image 

        find_coin = CoinDetector.moving_r_window(img, RadiusWindow, minRadius, maxRadius)   # find the coin in image
        find_coin = np.reshape(find_coin, (1,3))            # remove unused dimension
        pos_coin_rounded = np.uint16(np.around(find_coin))  # rounded position
        [y_coin, x_coin, r_coin]= pos_coin_rounded[0,:] # position of coin and radius of coin (in pixels)
        
        return y_coin, x_coin, r_coin, img_og


    def Search_Coin(self, *args):
        global img_og, y_coin, x_coin, r_coin

        path = Input.Import_Image.img_path
        print(path)
        ks_blur = Input.GetBlur.ks_blur
        RadiusWindow = Input.GetRadiusSp.RadiusWindow
        minRadius = Input.SelectMinR.MinR
        maxRadius = Input.SelectMaxR.MaxR

        [y_coin, x_coin, r_coin, img_og] = CoinDetector.Coin_Dector(self, path, ks_blur, RadiusWindow, minRadius, maxRadius)
        plt.close('all')

        image_coin = Cplt.CoinPlot(self, img_og, y_coin, x_coin, r_coin)
        Cplt.CropCoinPlot(self, image_coin, y_coin, x_coin, r_coin)

