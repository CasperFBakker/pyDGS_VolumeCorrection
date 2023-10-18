import os
import shutil

import cv2
import numpy as np
import pandas as pd
from imageio import imread
from scipy.ndimage import rotate as rotate_image

from Classes.InputQuestions import Setup_Questions
from Classes.NovelCorrection import AreaVolumeConversion
from Classes.pyDGS import *

if __name__ == '__main__':
    path_of_the_directory, dir_path, dir_name, ImageData_Dir, OutputData_Dir = Setup_Questions.Input_Directory()
    print(ImageData_Dir)
    save_NVCM = Setup_Questions.Input_NVCM()
    save_Percentages = Setup_Questions.Input_StoreUncorrected()
    if save_NVCM == 'y' or save_NVCM == 'yes' or save_Percentages == 'y' or save_Percentages == 'yes':
        Description_Data = Setup_Questions.Input_StoreDescription(dir_name)
    else: 
        Description_Data = []

    ext = ('.jpg', '.JPG', '.jpeg', '.heif', '.png')
    Angles = np.array([30, 45]) #30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330, 360


    for index, Angle in enumerate(Angles):
        Description_Data = 'Rotated_' + str(Angle)
        print(Description_Data)
        Setup_Questions.Input_Reminder(path_of_the_directory, save_NVCM, save_Percentages, Description_Data)
        if index != 0:
            pass

        for files in os.listdir(path_of_the_directory):
            if files.endswith(ext):
                image = path_of_the_directory + files  
                print(image)

                resolution = pyDGS_Functions.GetImageRes(image, ImageData_Dir) 
                print(files, resolution)
                # **************************** Pre-Processing ****************************
                original, nx, ny, width = run_pyDGS.Preprocessing(image, Angle)
                # ***************************** Small Scales *****************************
                percentage_small = run_pyDGS.get_GSD(original, nx, ny, width, resolution, scale='Small')
                # ***************************** Large Scales *****************************
                percentage_large = run_pyDGS.get_GSD(original, nx, ny, width, resolution, scale='Large')
                Uncorrected_Percentage = pyDGS_Functions.PercentageFromSum((percentage_small[0:10] + percentage_large[10:]))
                
                pyDGS_Functions.Store_Percentage(OutputData_Dir + '/Rotations', files, Uncorrected_Percentage, Description_Data)

    pyDGS_Functions.combine_csv_files(OutputData_Dir, dir_name)
    pyDGS_Functions.Statistics_csv(OutputData_Dir, dir_name)

    os.system('clear')
    if save_NVCM == 'y' or save_NVCM == 'yes':
        print('Start Volume Correction') 

        dgs_data, Resolution, STdev = AreaVolumeConversion.Read_Input(dir_name)
        data_dict, GrainSz, Density_Sand = AreaVolumeConversion.import_data()

        for i in range(len(Resolution)):
            Area_Fraction = AreaVolumeConversion.Area_Fraction(Resolution[i], dgs_data[i, 1:])
            Nb_Grains = AreaVolumeConversion.Top_ViewArea(Area_Fraction, STdev[i, :], GrainSz)

            GrainVolume = []

            for index, value in enumerate(STdev[i, 1:]):
                if value < 0.5:
                    CorCoef = (AreaVolumeConversion.get_CorCoef(data_dict, GrainSz[index], 0))
                    GrainVolume.append(AreaVolumeConversion.Comp_GrainVolume(GrainSz[index], CorCoef))
                elif value >= 0.5 and value < 1:
                    CorCoef = AreaVolumeConversion.get_CorCoef(data_dict, GrainSz[index], 1)
                    CorCoef = AreaVolumeConversion.update_CorCoef(CorCoef, GrainSz[index], value, 'mid')
                    GrainVolume.append(AreaVolumeConversion.Comp_GrainVolume(GrainSz[index], CorCoef))
                else:
                    CorCoef = AreaVolumeConversion.get_CorCoef(data_dict, GrainSz[index], 2)
                    CorCoef = AreaVolumeConversion.update_CorCoef(CorCoef, GrainSz[index], value, 'max')
                    GrainVolume.append(AreaVolumeConversion.Comp_GrainVolume(GrainSz[index], CorCoef))
                
            Grain_Mass = AreaVolumeConversion.Comp_GrainMass(GrainVolume) 


            Mass_Fraction = Nb_Grains * Grain_Mass
            Mass_Fraction = (Mass_Fraction / np.nansum(Mass_Fraction)) * 100

            AreaVolumeConversion.Store_Percentage(OutputData_Dir + '/Corrected', dir_name, dgs_data[i, 0], Mass_Fraction)


    
    if save_Percentages == 'n' or save_Percentages == 'no':
        shutil.rmtree(OutputData_Dir + 'Correction_Statistics/')
        shutil.rmtree(OutputData_Dir + 'Rotations/')
