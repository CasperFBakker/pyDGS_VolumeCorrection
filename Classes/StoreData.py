import os
import tkinter as tk

import cv2
import numpy as np
import pandas as pd
from exif import Image

from Classes.CoinPlot import CoinPlots as Cplt
from Classes.GetInput import GetInput


class Store_Img_data():
    def __init__(self):
        self.Meta_data()
        
    def Scale_Img(self, img_path, r_final, coin_type):
        coin_vault = {"2_Euro": 25.75, "1_Euro": 23.25, "50_Cent": 24.25,
                    "20_Cent": 22.25, "10_Cent": 19.75, "5_Cent": 21.25, "US_Quarter":24.257}

        dia_coin_pix = r_final * 2 
        coin_dia_mm = coin_vault[coin_type]
        size_pixel = coin_dia_mm / dia_coin_pix # pixel size in mm  

        image = cv2.imread(img_path, cv2.IMREAD_COLOR) # Read the image 
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 
        [height, width, _] = np.shape(image)
        height *= size_pixel
        width *= size_pixel

        return height, width, size_pixel

    def Calc_HeightAboveBed(self, model, focal_length, height, width, size_pixel):
        if model == 'SM-A515F':
            img_heigth = min(height, width)
            heightabovebed = (focal_length * img_heigth / 3.4) * size_pixel
        elif model == 'Canon EOS 1100D':
            img_heigth = min(height, width)
            heightabovebed = (focal_length * img_heigth / 22.2) * size_pixel
        else: 
            heightabovebed = np.nan
        return heightabovebed

    def Convert_GPS(self, gps_latitude, gps_latitude_ref, gps_longitude, gps_longitude_ref):
        lat = gps_latitude
        lon = gps_longitude

        Latitude = (str(int(lat[0]))+"°"+str(int(lat[1]))+"'"+str(lat[2])+'" '+gps_latitude_ref) 
        Longitude = (str(int(lon[0]))+"°"+str(int(lon[1]))+"'"+str(lon[2])+'" '+gps_longitude_ref) 
        return Latitude, Longitude
    
    
    def Storing_data(self, *args):
        path = GetInput.Import_Image.img_path
        coin_type = GetInput.GetCoinType.coin_type

        if hasattr(Cplt.update, 'r_final'):
            Store_Img_data.Meta_data(self, path, Cplt.update.r_final, coin_type)
        else:
            Store_Img_data.Meta_data(self, path, Cplt.update.r_coin, coin_type)

    def Meta_data(self, img_path, r_coin, coin_type):
        with open(img_path, 'rb') as img_file:
            img = Image(img_file)

        filename = os.path.basename(img_path)
        
        height, width, size_pixel = Store_Img_data.Scale_Img(self, img_path, r_coin, coin_type)
 
        if img.get("model") == 'Canon EOS 1100D' or  img.get("model") == 'iPhone SE (2nd generation)':
            img_height = img.get("pixel_y_dimension") * size_pixel
            img_width = img.get("pixel_x_dimension")* size_pixel

            heightabovebed = Store_Img_data.Calc_HeightAboveBed(self, img.get("model"), img.get("focal_length"), img.get("pixel_y_dimension"), img.get("pixel_x_dimension"), size_pixel)
            data = filename, size_pixel, img.get("datetime"), img.get("model"), 'None', 'None', img_height, img_width, heightabovebed
            columns = ['Image name', 'Pixel size (mm/pixel)', 'Date/time', 'Device', 'Latitude', 'Longitude', 'Image height (mm)', 'Image width (mm)', 'Heigth above bed (mm)']
        else:
            img_height = img.get("image_height") * size_pixel
            img_width = img.get("image_width") * size_pixel
            heightabovebed = Store_Img_data.Calc_HeightAboveBed(self, img.get("model"), img.get("focal_length"), img.get("image_height"), img.get("image_width"), size_pixel)
            Latitude, Longitude = Store_Img_data.Convert_GPS(self, img.get("gps_latitude"), img.get("gps_latitude_ref"), img.get("gps_longitude"), img.get("gps_longitude_ref"))
            
            data = filename, size_pixel, img.get("datetime_original"), img.get("model"), str(Latitude), str(Longitude), img_height, img_width, heightabovebed
            columns = ['Image name', 'Pixel size (mm/pixel)', 'Date/time', 'Device', 'Latitude', 'Longitude', 'Image height (mm)', 'Image width (mm)', 'Heigth above bed (mm)']
            

        dir_path = os.path.dirname(img_path)
        dir_name = os.path.basename(dir_path)


        temp = pd.DataFrame([data], columns=columns)
        temp.to_csv('Output data/Image_data/temp.csv', index=False)

        try: 
            DF = pd.read_csv("Output data/Image_data/data_" + dir_name +".csv")

            if filename in DF.values:
                result = tk.messagebox.askquestion(title=':(::(:(:(:(', message='The data from this image is already stored. Do you want to replace the data?')
                if result == 'yes':
                    temp = pd.DataFrame([data], columns=columns)
                    merged = pd.concat([temp, DF])

                    merged = merged.drop_duplicates(subset=['Image name'])
                    merged.to_csv("Output data/Image_data/data_" + dir_name +".csv", index=False)

                else:
                    pass
            else:
                temp = pd.DataFrame([data], columns=columns)
                merged = pd.concat([temp, DF])
                merged.to_csv("Output data/Image_data/data_" + dir_name +".csv", index=False)

        except FileNotFoundError:
            temp = pd.DataFrame([data], columns=[columns])
            temp.to_csv("Output data/Image_data/data_" + dir_name +".csv", index=False)


