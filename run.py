import os
import pandas as pd
import configparser
import yfinance as yf
from datetime import date, datetime, timedelta
from pgdb import PGDatabase

config = configparser.ConfigParser()
config.read('config.ini')


SALES_PATH = config['Files']['SALES_PATH']
COMPANIES = eval(config['Companies']['COMPANIES'])
DATABASE_CREDS = config['Database']

sales_df = pd.DataFrame()
if os.path.exists(SALES_PATH):
    sales_df = pd.read_csv(SALES_PATH)
    os.remove(SALES_PATH)  

historical_d = {}
for company in COMPANIES:
    stock = yf.Ticker(company)
    data = stock.history(start=(date.today() - timedelta(days=1)).isoformat(),
                         end=date.today().isoformat()).reset_index()
    
    historical_d[company] = data
    
database = PGDatabase(
    host = DATABASE_CREDS['HOST'],
    database = DATABASE_CREDS['DATABASE'],
    user = DATABASE_CREDS['USER'],
    password = DATABASE_CREDS['PASSWORD'],
)
    
for i, row in sales_df.iterrows():
    query = f"insert into sales values('{row['dt']}', '{row['company']}', '{row['transaction_type']}', {row['amount']})"
    database.post(query)

for company, data in historical_d.items():
    for i, row in data.iterrows():
        query = f"insert into stock values('{row['Date'].strftime('%Y-%m-%d')}', '{company}', {row['Open']}, {row['Close']})"
        database.post(query)