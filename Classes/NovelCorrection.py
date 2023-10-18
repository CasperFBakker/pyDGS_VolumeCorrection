import os

import numpy as np
import pandas as pd


class AreaVolumeConversion():
    
    def Read_Input(dir_name):
        dgs_data = np.array(pd.read_csv(f"Output data/{dir_name}/Correction_Statistics/{dir_name}_MeanRotate.csv"))
        Resolution = np.array(pd.read_csv(f"Output data/Image_data/{dir_name}/data_{dir_name}.csv"))[:,1]
        STdev = np.array(pd.read_csv(f"Output data/{dir_name}/Correction_Statistics/{dir_name}_StDevRotate.csv"))
        return dgs_data, Resolution, STdev

    def Area_Fraction(Resolution, dgs_data):
        Nb_Grains = []
        Image_Area = (4000*Resolution) * (2250 * Resolution)

        DGS_Fractions = dgs_data /100

        Area_Fraction = (DGS_Fractions * Image_Area)
        return Area_Fraction

    def Top_ViewArea(Area_Fraction, STdev, GrainSz):
        Nb_Grains = []

        for index, value in enumerate(Area_Fraction):
            if value == 0:
                Nb_Grains.append(0)
            else:
                if STdev[index+1] < 0.5:
                    Nb_Grains.append((value) / (np.pi*(GrainSz[index]/2)**2))
                elif STdev[index+1] >= 0.5 and STdev[index+1] < 1:
                    if GrainSz[index] < 1:
                        Nb_Grains.append((value) / (np.pi*(0.75 *(GrainSz[index]/2) * (GrainSz[index]/2))))
                    else:
                        Nb_Grains.append((value) / ((1/STdev[index+1]* (GrainSz[index]/2))* 0.1 * np.pi*(GrainSz[index]/2)))
                else:
                    Nb_Grains.append((value) / ((STdev[index+1]* (GrainSz[index]/2) * 0.001) * np.pi*(GrainSz[index]/2)))
    
        return Nb_Grains

    def update_CorCoef(CorCoef, GrainSz, Stdev, way):
        if way == 'mid':
            if GrainSz == 0.710 or GrainSz == 2 or GrainSz == 8:
                return CorCoef
            else:   
                return CorCoef * Stdev
        elif way == 'max': 
            if GrainSz == 2:
                return CorCoef
            else: 
                return CorCoef * (1/Stdev)

    def get_CorCoef(dictionary, key, item):
        if key in dictionary and dictionary[key]:
            return dictionary[key][item]
        else:
            return None 

    def Comp_GrainVolume(GrainSz, CorCoef):
        return (np.pi/6) * (GrainSz)**3 * CorCoef

    def Comp_GrainMass(Grain_Volume, Density_Sand=0.00165):
        return np.array(Grain_Volume) * Density_Sand 
        

    def Store_Percentage(path_of_the_directory, dir_name, image_name, percentage):
        columns = ['Image name', '0 mm', '0.063 mm', '0.125 mm', '0.180 mm', '0.250 mm', '0.300 mm', '0.355 mm', '0.425 mm', '0.500 mm', '0.710 mm', '1 mm', '2 mm', '4 mm', '8 mm']
        percentage = [0 if np.isnan(x) else x for x in percentage]
        data = [image_name] + percentage
        temp = pd.DataFrame([data], columns=columns)
        output_file_name = f"{dir_name}_CorPct"

        try:
            existing_df = pd.read_csv(os.path.join(path_of_the_directory, output_file_name + ".csv"))
            if image_name not in existing_df['Image name'].values:
                merged = pd.concat([temp, existing_df])
                merged.to_csv(os.path.join(path_of_the_directory, output_file_name + ".csv"), index=False)
        except FileNotFoundError:
            temp.to_csv(os.path.join(path_of_the_directory, output_file_name + ".csv"), index=False)
    

    def import_data():
        data_dict = {
            0.000: [0.1, 0.01, 1],
            0.063: [0.1, 0.01, 1],
            0.125: [0.1, 0.01, 1],
            0.180: [0.1, 0.01, 1],
            0.250: [0.1, 0.01, 1],
            0.300: [0.1, 0.01, 1],
            0.355: [0.1, 0.01, 1],
            0.425: [0.1, 0.01, 1],
            0.500: [0.05, 0.1, 0.000001],
            0.710: [0.001, 0.075, 1],
            1.000: [0.1, 0.01, 0.00025],
            2.000: [0.1, 0.0005, 0.000001],
            4.000: [0.1, 0.01, 0.000001],
            8.000: [0.1, 0.00075, 0.000001],
        }
        GrainSz = np.array(list(data_dict.keys()))
        Density_Sand = 0.00165  # (g/mm**3)

        return data_dict, GrainSz, Density_Sand

   