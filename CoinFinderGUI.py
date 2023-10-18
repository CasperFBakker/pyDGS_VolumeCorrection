from Imports.Import_Modules import * 

class GUI(object):
    def __init__(self, master):
        super().__init__()
        self.initComplete = 0

        self.frame = ttk.Frame(master)
        self.frame.pack(fill=BOTH, expand=tk.YES)
        self.master = master
        
        # set the window location
        self.master.title("pyDGS GUI")
        self.master.geometry(f"{GetInput.get_screen_resolution()[0]}x{GetInput.get_screen_resolution()[1]}")

        self.image_imported = False

        # ======================  Make a Widget Frame =============
        self.notebook = ttk.Notebook(self.frame)

        tab_1 = ttk.Frame(self.notebook)
        tab_1.grid_columnconfigure(0, weight=1)
        tab_1.grid_rowconfigure(0, weight=1)
        tab_1.grid_columnconfigure(1, weight=50)
        tab_1.grid_columnconfigure(2, weight=50)
        tab_1.grid_rowconfigure(1, weight=1)
        tab_1.grid_rowconfigure(2, weight=1)
        tab_1.grid(row=0, column=0,sticky='NSEW')

        tab_2 = ttk.Frame(self.notebook)
        tab_2.grid_columnconfigure(0, weight=25)
        tab_2.grid_columnconfigure(1, weight=50)
        tab_2.grid_columnconfigure(2, weight=25)
        tab_2.grid_rowconfigure(1, weight=50)
        tab_2.grid_rowconfigure(0, weight=1)
        tab_2.grid(row=0, column=0,sticky='NSEW')

        self.notebook.add(tab_1, text="Image Resolution")
        self.notebook.add(tab_2, text="pyDGS: Spectrogram")
        self.notebook.pack(fill=BOTH, expand=tk.YES)


        tab_1_left_frame = ttk.LabelFrame(tab_1, text="Import Image")
        tab_1_left_frame_2 = ttk.LabelFrame(tab_1, text="Detection Settings")
        tab_1_mid_frame = ttk.LabelFrame(tab_1, text="Coin Image")
        tab_1_right_frame = ttk.LabelFrame(tab_1, text="Full Image")
        tab_1_right_frame_2 = ttk.LabelFrame(tab_1, text="Output")

        tab_1_left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        tab_1_left_frame_2.grid(row=1, column=0, rowspan=2, padx=10, pady=10, sticky="nsew")
        tab_1_mid_frame.grid(row=0, column=1, rowspan=3, padx=10, pady=10, sticky="nsew")
        tab_1_right_frame.grid(row=0, column=2, rowspan=2, padx=10, pady=10, sticky=tk.NSEW)
        tab_1_right_frame_2.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")

        self.WindFrame = tab_1_left_frame_2
        self.ImportFrame = tab_1_left_frame
        self.Input = GetInput(self.master, self.WindFrame, tab_1_left_frame)
        self.PlotFrame = CoinPlots(self.master, tab_1_mid_frame, tab_1_right_frame)

        # ------------ tab_1 -----------------
        # ============ Import Image Frame ===============
        # ------------ Import image file ----------------
        tab_1_left_frame.grid_rowconfigure(0, weight=1)
        tab_1_left_frame.grid_rowconfigure(5, weight=1)
        tab_1_left_frame.grid_columnconfigure(0, weight=1)
        tab_1_left_frame.grid_columnconfigure(5, weight=1)

        self.import_file = ttk.Button(tab_1_left_frame, text="From Files", width="14")
        self.import_file.grid_columnconfigure(0, weight=1)
        self.import_file.grid(row=3, column=3, sticky="nsew")
        self.import_file.bind("<ButtonRelease-1>",  lambda Var: self.Input.Import_Image())
        
        self.nextImg = ttk.Button(tab_1_left_frame, text="Next") 
        self.nextImg.grid(row=4, column=4)
        self.nextImg.bind("<ButtonRelease-1>", lambda Var: self.Input.Next_Image(-2))

        self.previousImg = ttk.Button(tab_1_left_frame, text="Previous") 
        self.previousImg.grid(row=4, column=2)
        self.previousImg.bind("<ButtonRelease-1>", lambda Var: self.Input.Previous_Image(-2))

        # ============ Coin Detection Frame ============
        # ------------ Select Coin Type ------------  
        self.CoinTypeLabel = ttk.Label(tab_1_left_frame_2, text='Coin type:')
        self.CoinTypeLabel.grid(row=0, column=0, sticky="nsew")
        self.coin_bank = {"Select Coin Type": 0,"2 Euro": '2_Euro', "1 Euro": '1_Euro', "50 Cent": '50_Cent',
                          "20 Cent": '20_Cent', "10 Cent": '10_Cent', "5 Cent": '5_Cent', "US Quarter": 'US_Quarter'}
        self.CoinVar = StringVar()
        self.CoinType = ttk.OptionMenu(tab_1_left_frame_2, self.CoinVar,  *self.coin_bank, command = lambda x: self.Input.GetCoinType(self.coin_bank, self.CoinVar))
        self.CoinType.grid(row=1, column=0, pady=20, sticky="nsew")
        # ------------ Select Blur ------------  
        self.BlurLabel = ttk.Label(tab_1_left_frame_2, text='Kernel size for blur:')
        self.BlurLabel.grid(row=2, column=0, sticky="nsew")
        self.BlurSlide = tk.Scale(tab_1_left_frame_2, from_=1,to_=31, resolution = 2,
                                  length = 400, takefocus = 1, tickinterval=2,orient = tk.HORIZONTAL, command = lambda val: self.Input.GetBlur(val))
        self.BlurSlide.set(5)
        setattr(GetInput.GetBlur, 'ks_blur', 5)
        self.BlurSlide.grid(row=3, pady=10, column=0)
        # ------------ Min/Max Radius ------------  
        self.minR = tk.Scale(tab_1_left_frame_2, from_= 0, to= 500, orient='horizontal', command = lambda val: self.Input.SelectMinR(val))
        self.maxR = tk.Scale(tab_1_left_frame_2, from_= 0, to= 500, orient='horizontal', command = lambda val: self.Input.SelectMaxR(val))
        self.minR.set(0); self.maxR.set(5) 
        setattr(GetInput.SelectMinR, 'MinR', 0)
        setattr(GetInput.SelectMaxR, 'MaxR', 5) 
        self.minR.configure(state=DISABLED); self.maxR.configure(state=DISABLED)
        self.minR.grid(row=5, column=0, sticky="nsew"); self.maxR.grid(row=6, column=0, sticky="nsew")
        # ------------ Select Radius Window size ------------  
        Window_Sizes = ['Select difference min/max radius', 1, 2, 3, 4, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
        self.Window_SizesLabel = ttk.Label(tab_1_left_frame_2, text='Difference between minimum and maximum radius')
        self.Window_SizesLabel.grid(row=4, column=0, sticky="nsew")
        self.WindowVar = IntVar()
        self.WindowSize = ttk.OptionMenu(tab_1_left_frame_2, self.WindowVar, *Window_Sizes, command = lambda Var: self.Input.GetWindowSz(self.WindowVar))
        self.WindowSize.grid(row=4, column=0, sticky="nsew")
        # ------------ Select Radius Window steps ------------  
        Radius_Steps = ['Select steps radius window', 1, 2, 3, 4, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
        self.RadiusVar = IntVar()
        self.RadiusStep = ttk.OptionMenu(tab_1_left_frame_2, self.RadiusVar, *Radius_Steps, command = lambda Var: self.Input.GetRadiusSp(self.RadiusVar))
        self.RadiusStep.grid(row=7, column=0, pady=20, sticky="nsew")
        setattr(GetInput.GetRadiusSp, 'RadiusWindow', 10)
        # ------------ Run Coin Detection ------------  
        self.Coin_Detect = ttk.Button(tab_1_left_frame_2, text="Run") 
        self.Coin_Detect.grid(row=8, column=0, pady=100)
        self.Coin_Detect.bind("<ButtonRelease-1>", CoinDetector.Search_Coin)
        # =========== Output Text Box =============
        tab_1_right_frame_2.grid_rowconfigure(0, weight=1)
        tab_1_right_frame_2.grid_rowconfigure(3, weight=1)
        tab_1_right_frame_2.grid_columnconfigure(0, weight=1)
        tab_1_right_frame_2.grid_columnconfigure(3, weight=1)

        self.Save_Data = ttk.Button(tab_1_right_frame_2, text="Save") 
        self.Save_Data.grid(row=1, column=1)
        self.Save_Data.bind("<ButtonRelease-1>", Store.Storing_data)


def main(): 
    root = ThemedTk(theme="breeze")
    app = GUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()