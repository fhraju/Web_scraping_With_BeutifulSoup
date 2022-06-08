from turtle import title
import pandas as pd
import urllib.request as urlre
from bs4 import BeautifulSoup
import warnings

# Start of Yahoo income statement (ticker)

def yahoo_income_statement(ticker='AAPL'):
    #yahoo income statement url
    income_url = f'https://finance.yahoo.com/quote/{ticker}/financials?p={ticker}'
    read_url = urlre.urlopen(income_url).read()

    # BeautifulSoup the xml
    income_soup = BeautifulSoup(read_url, 'lxml')

    #Find relevant data structure for financial
    div_list = []

    #Find all HTML data structure that are divs
    for div in income_soup.find_all('div'):
        # Get the content and title
        div_list.append(div.string)

        #Prevent duplicate titles
        if not div.string == div.get('title'):
            div_list.append(div.get('title'))
    
    # Filter out irrelevant data
    # Exclude 'Operating expenses' and Non recurring events
    div_list = [incl for incl in div_list if incl not in ('Operating expenses', 'Non-recuring-events', 'Expand All')]

    # Filter out empty elements
    div_list = list(filter(None, div_list))

    # Filter out functions
    div_list = [incl for incl in div_list if not incl.startswith('(function')]

    # Sublist the relevant financial information
    income_list = div_list[13: -5] # Why [13: -5]

    # Insert "Breakdown" to the begening of the list to give it a proper structure
    income_list.insert(0, 'Breakdown')

    # Create a dataFrame of the financial data
    # Store the financial data as a list of tuples
    income_data = list(zip(*[iter(income_list)]* 6)) # Why 6

    # Create a DataFrame
    income_df = pd.DataFrame(income_data)

    # Make the top row the headers
    headers = income_df.iloc[0]
    income_df = income_df[1:]
    income_df.columns = headers
    income_df.set_index('Breakdown', inplace=True, drop=True)

    warnings.warn('Amounts are in thousands.')

    return income_df

# End of Yahoo income statement ticker

# Start of Yahoo Balance Sheet ticker
def yahoo_balance_sheet(ticker='AAPL'):
    # Read the yahoo balance sheet url
    balancesheet_url = f'https://finance.yahoo.com/quote/{ticker}/balance-sheet?p={ticker}'