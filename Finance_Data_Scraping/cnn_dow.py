from colorama import Cursor
import requests
import pandas as pd
import datetime
from time import sleep
import random

current_dt = datetime.datetime.now()
print("Python start time: " + current_dt.strftime("%I:%M:%S %p" ))

df_dow30 =pd.read_html('https://money.cnn.com/data/markets/dow?utm_source=optzlynewmarketribbon') #('https://money.cnn.com/quote/quote.html?symb=indu')

print("")
print("Dow 30")
print(df_dow30[0].to_string(header=False,index=False))
print("")
sleep(random.randrange(1,3))
print(df_dow30[1].to_string(header=False,index=False))
print("")
sleep(random.randrange(1,3))
print(df_dow30[2].to_string(header=False,index=False))

print("")
current_dt = datetime.datetime.now()
print("Python End Time: " + current_dt.strftime("%I:%M:%S %p" ))