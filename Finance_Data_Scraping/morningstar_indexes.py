"""
This will collect and store all three market indexes The S&P500, NASDAQ, DJIA
"""
import requests
import datetime
import pandas as pd
import os
from bs4 import BeautifulSoup
from xlsxwriter import Workbook

current_dt = datetime.datetime.now()
print("Start: " + current_dt.strftime("%I:%M:%S: %p"  ))

#Read Morning Star
print("Reading Market Indexes")
print("")

html = requests.get('https://www.morningstar.com/markets').content
df_morningstar = pd.read_html(html)
df_market_indexes = df_morningstar[0]

#Excel will treat % as string
# Convert by removing % and convert to float
# Replaced the standard minus sign with a U+2212 minus sign
df_market_indexes['Change %'] = df_market_indexes['Change %'].str.replace(u"\u2212", '-')
df_market_indexes['Change %'] = df_market_indexes['Change %'].str.rstrip('%').astype('double') / 100.0

# Change only comes in as positive. Negate change if change % is negative
df_market_indexes.loc[df_market_indexes['Change %'] < 0, ['Change']] = df_market_indexes['Change'] * -1

del df_market_indexes['Value']
df_market_indexes.rename(columns={'Graph':'Value'}, inplace=True)

# Add data time source
# Data source is from website
page = requests.get('https://www.morningstar.com/markets')
soup = BeautifulSoup(page.content, 'html.parser')

section = soup.find_all('div', class_='mdc-market-indexes-table__last-updated')
for elem in section:
    wrappers = elem.find('time')

timestamp_string = wrappers.get('datetime')
timestamp_string = timestamp_string[:-6] # strip away UTC
date_time_obj = datetime.datetime.strptime(timestamp_string, '%Y-%m-%dT%H:%M:%S')
df_market_indexes['TimeStamp']=date_time_obj.strftime("%b-%d-%Y %I:%M:%S %p")

print(df_market_indexes)

# File name has a time stamp
xlsx_filename = current_dt.strftime("%Y_%m%d_%I%M%S_%p" )+ "_MarketIndexes" + ".xlsx"
xlsx_fullname = os.path.dirname(os.path.abspath(__file__)) + "\\" + xlsx_filename

# Read NASDAQ
print("")
print("Writing to Excel")

# Create a pandas excel writer using XlsxWriter as the engine.
# Set default date format
writer = pd.ExcelWriter(xlsx_fullname, engine='xlsxwriter', datetime_format='mmm-d-yyyy hh:mm AM/PM')

# Convert the dataframe to an xlxsWriter Excel object.
df_market_indexes.to_excel(writer, sheet_name='Indexes', index=False)

# Get the xlsx workbook and worksheet objects.
workbook = writer.book
worksheet = writer.sheets['Indexes']

# Add cell formating to workbook
format_comma = workbook.add_format({'num_format': '#,##0.00;[Red]-#,##0.00'})
format_percent = workbook.add_format({'num_format': '0.00%;[Red]-0.00%'})
format_decimal = workbook.add_format({'num_format': '#,##0'})
format_date = workbook.add_format({'num_format': 'mmm-dd-yyyy hh:mm:ss AM/PM'})

# Set the column width and format
worksheet.set_column('A:A', 13)
worksheet.set_column('B:C', 9, format_comma)
worksheet.set_column('D:D', 9, format_percent)
worksheet.set_column('E:E', 23, format_date)

worksheet.freeze_panes(1, 0) # Freeze header row

# Add hyperlink source
worksheet.write(8, 0, 'Source')
worksheet.write_url('0', '89', 'https://www.morningstar.com/markets')

# Close the pandas excel writer and output the excel file.
writer.save()

# Launch workbook
os.system('start "excel" '+ xlsx_fullname)

print("")
current_dt = datetime.datetime.now()

print("Finish saving indexes into an Excel workbook on " + current_dt.strftime("%I:%M:%S %p"))
print("The file '" + xlsx_filename + "'is saved in the following location")
print(os.path.dirname(os.path.abspath(__file__)))

xlsx_fullname = os.path.dirname(os.path.abspath(__file__)) + xlsx_filename

print("")
print("End: " + current_dt.strftime("%I:%M%:%S %p"))