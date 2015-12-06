##This uses 'tia' package bloomberg api wrapper and utils from https://github.com/bpsmith/tia
##Installed at C:\Python27\Lib\site-packages

##Imports for simple daily data query
from tia.bbg import LocalTerminal
import pandas as pd

#Other imports for all tia utils
#import datetime
#import matplotlib.pyplot as plt

#Simple bloomberg data download to responce object
resp = LocalTerminal.get_historical('INTC US EQUITY', ['PX_OPEN', 'PX_LAST'], start='1/1/2014', end='3/1/2014')
#View data in terminal
#resp.as_map()

#Data as data frame
resp_frame = resp.as_frame()

#To csv
resp_frame.to_csv('C:\Program Files\StrataStack\Bberg_Python_out\histTest.csv')#, sep='\t')
