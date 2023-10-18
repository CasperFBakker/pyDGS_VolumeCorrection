import os
from time import sleep

import cv2
import numpy as np
import pandas as pd
import pywt
import scipy.stats as stats
from imageio import imread
from scipy.ndimage import rotate as rotate_image
from tqdm import tqdm


class pyDGS_Functions:
    
    def rescale(dat,mn,mx):
        """
        rescales an input dat between mn and mx
        """
        m = min(dat.flatten())
        M = max(dat.flatten())
        return (mx-mn)*(dat-m)/(M-m)+mn

    def standardize(img):
        img = np.array(img)
        #standardization using adjusted standard deviation
        N = np.shape(img)[0] * np.shape(img)[1]  # Calculate the total number of pixels
        s = np.maximum(np.std(img), 1.0/np.sqrt(N)) # Compute the adjusted standard deviation
        m = np.mean(img) 
        img = (img - m) / s 
        img = pyDGS_Functions.rescale(img, 0, 1)
        del m, s, N

        return img

    def PercentageFromPDF(r_v, scales, resolution):
        # Calculating Percentages
        a = (scales*resolution)
        minSz = np.array([0, 0.063, 0.125, 0.180, 0.250, 0.300, 0.355, 0.425, 0.500, 0.710, 1, 2, 4, 8])
        maxSz = np.array([0.063, 0.125, 0.180, 0.250, 0.300, 0.355, 0.425, 0.500, 0.710, 1, 2, 4, 8, 20])
        percentage = []
        
        for i in range(len(minSz)):
            _, length = np.shape(np.where((a>minSz[i])&(a<maxSz[i])))   
            percentage.append(((np.trapz(np.interp([np.linspace(minSz[i], maxSz[i], 1000)], (scales*resolution), r_v)[0])*length/1000))*100)

        return percentage

    def GetImageRes(img_path, ImageData_Dir):
        filename = os.path.basename(img_path)
        dir_path = os.path.dirname(img_path)
        dir_name = os.path.basename(dir_path)

        try:
            DataFrame = pd.read_csv(ImageData_Dir + "data_" + dir_name +".csv")
            row = DataFrame[DataFrame["Image name"] == filename].index[0]
            resolution = DataFrame.at[row, 'Pixel size (mm/pixel)']
        except FileNotFoundError:
            DataFrame = pd.read_csv("/home/casper/Documents/Python/pyDGS-GUI/Output data/Image_data/data_" + dir_name +".csv")
            row = DataFrame[DataFrame["Image name"] == filename].index[0]
            resolution = DataFrame.at[row, 'Pixel size (mm/pixel)']
        return resolution
    
    def PercentageFromSum(Percentage_Arr):
        Sum = np.sum(Percentage_Arr)
        Corrected_Percentages = []
        for index, value in enumerate(Percentage_Arr):
            Corrected_Percentages.append((value / Sum)*100)

        return Corrected_Percentages

    def Store_Percentage(path_of_the_directory, image_name, percentage, description):
        columns = ['Image name', '0 mm', '0.063 mm', '0.125 mm', '0.180 mm', '0.250 mm', '0.300 mm', '0.355 mm', '0.425 mm', '0.500 mm', '0.710 mm', '1 mm', '2 mm', '4 mm', '8 mm']

        data = [image_name] + percentage
        temp = pd.DataFrame([data], columns=columns)

        dir_path = os.path.dirname(path_of_the_directory)
        output_file_name = os.path.basename(dir_path)

        output_file_name += "_UncPct"
        if description:
            output_file_name += f"_{description}"

        try:
            existing_df = pd.read_csv(os.path.join(path_of_the_directory, output_file_name + ".csv"))
            if image_name not in existing_df['Image name'].values:
                merged = pd.concat([temp, existing_df])
                merged.to_csv(os.path.join(path_of_the_directory, output_file_name + ".csv"), index=False)
        except FileNotFoundError:
            temp.to_csv(os.path.join(path_of_the_directory, output_file_name + ".csv"), index=False)

    def combine_csv_files(path_of_the_directory, dir_name):
        combined_df = pd.DataFrame()

        # Loop through files in the directory
        for filename in sorted(os.listdir(path_of_the_directory + '/Rotations/')):
            if filename.endswith(".csv"):
                file_path = os.path.join(path_of_the_directory + '/Rotations/', filename)
                df = pd.read_csv(file_path)
                combined_df = combined_df.append(df, ignore_index=True)

        combined_df.sort_values(by=combined_df.columns[0], inplace=True)
        combined_df.to_csv(path_of_the_directory + '/Correction_Statistics/' + dir_name + '_UncPct_CombinedRotations.csv', index=False)

    def Statistics_csv(path_of_the_directory, dir_name):

        for filename in os.listdir(path_of_the_directory + '/Correction_Statistics/'):
            if filename.endswith("_CombinedRotations.csv"):
                df = pd.read_csv(path_of_the_directory + '/Correction_Statistics/' + filename)

        Average = df.groupby(['Image name']).mean()
        Average.to_csv(path_of_the_directory + '/Correction_Statistics/' + dir_name + '_MeanRotate.csv')

        StDev = df.groupby(['Image name']).std()
        StDev.to_csv(path_of_the_directory + '/Correction_Statistics/' + dir_name + '_StDevRotate.csv')

class run_pyDGS: 
    def Preprocessing(image, Angle):
        img = cv2.imread(image)
        nxx, nyy, _ = img.shape
        width = min(nxx, nyy)

        im = imread(image)   # read the image straight with imread
        im = np.squeeze(im)  # squeeze singleton dimensions
        if len(np.shape(im))>3:
            im = im[:, :, :3]            # only keep the first 3 bands

        if len(np.shape(im))==3: # if rgb, convert to grey
            im = (0.299 * im[:,:,0] + 0.5870*im[:,:,1] + 0.114*im[:,:,2]).astype('uint8')

        nx,ny = np.shape(im)

        im = rotate_image(im, Angle)
        im = pyDGS_Functions.standardize(im)
        region = im.copy()
        original = pyDGS_Functions.rescale(region,0,255)
        nx, ny = original.shape
        return original, nx, ny, width 

    def get_GSD(original, nx, ny, width, resolution, scale):
        P = []; M = []

        # Define scale parameters based on the input 'scale'
        if scale == 'Small':
            horizontal_lines = 100
            min_scale = 3 
            max_scale = np.maximum(nx, ny) / (width * resolution / 1)
        elif scale == 'Large':
            horizontal_lines = 10
            min_scale = np.maximum(nx, ny) / (width * resolution / 1)
            max_scale = np.maximum(nx, ny) / (width * resolution / 8)
        else:
            raise ValueError("Invalid 'scale' value. Use 'Small' or 'Large'.")

        for k in tqdm(np.linspace(1, nx-1, horizontal_lines)):
            [cfs, frequencies] = pywt.cwt(original[int(k), :], np.arange(min_scale, max_scale, 1), 'morl', 0.5)
            period = 1. / frequencies
            power = (abs(cfs)) ** 2
            power = np.mean(np.abs(power), axis=1) / (period**2)
            P.append(power)
            M.append(period[np.argmax(power)])
            sleep(np.random.uniform(0.005, 0.01))

        p = np.mean(np.vstack(P), axis=0)
        p = np.array(p / np.sum(p))

        scales = np.array(period)
        srt = np.sqrt(np.sum(p * ((scales - np.mean(M))**2)))

        p = p + stats.norm.pdf(scales, np.mean(M), srt / 2)
        p = np.hstack([p])
        scales = np.hstack([scales])
        p = p / np.sum(p)

        percentage = pyDGS_Functions.PercentageFromPDF(p, scales, resolution)

        return percentage

    def Cor_NVCM(pwr1, pwr2):
        pass