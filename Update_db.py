"""
Admin have to run this program one a day to update the forex database.

On line 76 Admin have to change the value of pairs(1 to 8), when they run the program each time. 

Admin also need to check if database have been successfully updated or not 
"""

import requests
import sqlalchemy as db
import pandas as pd
from config import API_KEY


 # Function to fetch data from the Alpha Vantage API   
def get_api_data(url):
    response = requests.get(url)
    return response.json()

# Function to process and create a DataFrame from API data
def create_database(api_data,time_series):
    data = api_data[time_series]
    processed_data = []

    for date, values in data.items():
        processed_data.append({
            'date': date,
            'open': float(values['1. open']),
            'high': float(values['2. high']),
            'low': float(values['3. low']),
            'close': float(values['4. close'])
        })
    
    return pd.DataFrame(processed_data)

# Currency pairs and timeline options
Currencypair = {
                '1' : ["EUR", "USD"],
                '2' : ["USD", "JPY"],
                '3' : ["GBP", "USD"],
                '4' : ["USD", "CHF"],
                '5' : ["USD", "CAD"],
                '6' : ["AUD", "USD"],
                '7' : ["NZD", "USD"],
                '8' : ["EUR", "JPY"]
            }

timeline = {
            '1' : ["FX_DAILY", 'Time Series FX (Daily)',"Daily"] ,
            '2' : ["FX_WEEKLY", 'Time Series FX (Weekly)', "Weekly"],
            '3' : ["FX_MONTHLY", 'Time Series FX (Monthly)', "Monthly"]
            }

# Create lists to store URLs, currency pairs, titles, and DataFrame titles
set_of_url = []
set_of_url = []
from_currency = []
to_currencey = []
full_title = []
df_title = []


# Loop through currency pairs and timelines to generate URLs and lists
for currency in Currencypair.values():
    for Time in timeline.values():
        url = f'https://www.alphavantage.co/query?function={Time[0]}&from_symbol={currency[0]}&to_symbol={currency[1]}&apikey={API_KEY}'
        set_of_url.append(url)

        from_currency.append(currency[0])
        to_currencey.append(currency[1])
        full_title.append(Time[1])
        df_title.append(Time[2])


# Specify a currency pair for demonstration purposes
pairs = "8"
first = Currencypair[pairs][0]
second =  Currencypair[pairs][1]

# Loop through URLs to fetch API data and create DataFrames
for i in range(24):
    if from_currency[i] ==first and to_currencey[i] == second: 
        api_data = get_api_data(set_of_url[i])
        df = create_database(api_data, full_title[i])[:100]
        database_name = 'forex_data2.db'
        engine = db.create_engine(f"sqlite:///{database_name}")
        df.to_sql(f'{from_currency[i]}{to_currencey[i]}{df_title[i]}', engine, if_exists='replace', index=False)
        print(f'{from_currency[i]}{to_currencey[i]}{df_title[i]}')


print("Data_updated")



