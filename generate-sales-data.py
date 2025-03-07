import pandas as pd
from datetime import date, datetime, timedelta
from random import randint
import configparser
import os

dirname = os.path.dirname(__file__)

config = configparser.ConfigParser()
config.read(os.path.join(dirname, 'config.ini'))

COMPANIES = eval(config['Companies']['COMPANIES'])

# Если запуск в воскресенье или понедельник, то программа ничего не делает (7, 1)
today = datetime.today()
yesterday = today - timedelta(days=1)

if 2 <= today.isoweekday() <= 6:
    d = {
        'dt': [yesterday.strftime('%Y-%m-%d')] * len(COMPANIES) * 2,
        'company': COMPANIES * 2,
        'transaction_type': ['buy'] * len(COMPANIES) + ['sale'] * len(COMPANIES),
        'amount': [randint(0, 1000) for _ in range(len(COMPANIES) * 2)]
    }

    df = pd.DataFrame(d)
    df.to_csv(os.path.join(dirname, 'sales-data.csv'), index=False)
    print('Данные загружены в csv')