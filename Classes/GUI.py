import os
import sys
import time
import tkinter as tk
from functools import partial
from tkinter import *
from tkinter import (ALL, BOTH, BOTTOM, END, FLAT, GROOVE, LEFT, NE, NW, RIGHT,
                     SE, SUNKEN, SW, TOP, VERTICAL, YES, Button, Canvas,
                     Checkbutton, E, Entry, Frame, IntVar, Label, Listbox,
                     Menu, N, PhotoImage, S, Scrollbar, StringVar, Text, Tk,
                     Toplevel, W, X, Y, filedialog, ttk)
from tkinter.filedialog import askopenfilename

import cv2
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pywt
from imageio import imread
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Circle
from natsort import natsorted
from screeninfo import get_monitors
from skimage.restoration import denoise_wavelet, estimate_sigma
from tqdm import tqdm
from ttkthemes import ThemedTk

_denoise_wavelet = partial(denoise_wavelet, rescale_sigma=True)
import matplotlib.pyplot as plt
import scipy.stats as stats
from exif import Image

from Classes.CoinDector import *
from Classes.CoinPlot import CoinPlots as Cplt
from Classes.CoinPlot import *
from Classes.GetInput import GetInput
from Classes.StoreData import Store_Img_data as Store


