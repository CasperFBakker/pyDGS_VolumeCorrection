import os 

class Setup_Questions:

    def Setup_Dir(date, name):
        base_dir = os.path.dirname(os.path.abspath(name))
        Photo_Dir = f'{base_dir}/Input data/{date}/'
        ImageData_Dir = f'{base_dir}/Output data/Image_data/'
        OutputData_Dir = f'{base_dir}/Output data/{date}'

        return Photo_Dir, ImageData_Dir, OutputData_Dir

    def Input_Directory():
        input_dir = False

        while input_dir == False:
            input_directory = input('Type the name of the directory: ')
            Photo_Dir, ImageData_Dir, OutputData_Dir = Setup_Questions.Setup_Dir(input_directory, name='__main__')
            if os.path.exists(Photo_Dir):
                input_dir = True
            else:
                print(f"The working directory '{Photo_Dir}' does not exist.")
                input_dir = False


        path_of_the_directory = os.path.join(Photo_Dir)
        dir_path = os.path.dirname(path_of_the_directory)
        dir_name = os.path.basename(dir_path)

        print('The working directory is set as: ', path_of_the_directory)
        print('____________________________________________________________________________________________________________________')
        return path_of_the_directory, dir_path, dir_name, ImageData_Dir, OutputData_Dir
    def Input_StoreUncorrected():
        answer = False 

        while answer == False:
            save_Percentages = input('Do you want to save the uncorrected percentages? (y/n) ')

            if save_Percentages == "y" or save_Percentages == "yes":
                print("Uncorrected percentages will be stored")
                answer = True     
            elif save_Percentages == "n" or save_Percentages == "no":
                print("Uncorrected percentages will not be stored")
                answer = True
            else: 
                print("please answer with y or n")
        print('____________________________________________________________________________________________________________________')
        return save_Percentages

    def Input_NVCM():
        Correction = False 

        while Correction == False:
            save_NVCM = input('Do you want to apply and store the Novel Volume Correction Method? (y/n) ')

            if save_NVCM == "y" or save_NVCM == "yes":
                print("Correction will be preformed")
                Correction = True     
            elif save_NVCM == "n" or save_NVCM == "no":
                print("No correction is done")
                Correction = True
            else: 
                print("please answer with y or n")

        print('____________________________________________________________________________________________________________________')
        return save_NVCM

    def Input_GCM():
        Correction = False 

        while Correction == False:
            save_GCM = input('Do you want to apply and store the general conversion correction? (y/n) ')

            if save_GCM == "y" or save_GCM == "yes":
                print("Correction will be preformed")
                pwr1 = float(input('What is the power of the small scales (< 0.5 mm)?'))
                pwr2 = float(input('What is the power of the large scales (=> 0.5 mm)?'))
                Correction = True     
            elif save_GCM == "n" or save_GCM == "no":
                print("No correction is done")
                Correction = True
                pwr1 = pwr2 = 0
            else: 
                print("please answer with y or n")

        print('____________________________________________________________________________________________________________________')
        return save_GCM, pwr1, pwr2

    def Input_StoreDescription(dir_name):
        Description_Data = input('Give a description for stored data: ')
        if len(Description_Data) == 0:
            print("The data will be stored as: /..._" + dir_name + ".csv")
        else:
            print("The data will be stored as: /..._" + dir_name + "_" + Description_Data + ".csv")
        print('____________________________________________________________________________________________________________________')
        return Description_Data

    def Input_Reminder(path_of_the_directory, save_NVCM, save_Percentages, Description_Data):
        print('The working directory is set as: ', path_of_the_directory)
        print('____________________________________________________________________________________________________________________')

        if save_NVCM == "y" or save_NVCM == "yes":
            print("Correction will be preformed")   
        elif save_NVCM == "n" or save_NVCM == "no":
            print("No correction is done")

        if save_Percentages == "y" or save_Percentages == "yes":
            print("Uncorrected percentages will be stored")
        elif save_Percentages == "n" or save_Percentages == "no":
            print("Uncorrected percentages will not be stored")

        if len(Description_Data) == 0:
            print("The data will be stored as: /..._" + os.path.basename(os.path.dirname(path_of_the_directory)) + ".csv")
        else:
            print("The data will be stored as: /..._" + os.path.basename(os.path.dirname(path_of_the_directory)) + "_" + Description_Data + ".csv")
        print('____________________________________________________________________________________________________________________')