import requests
import json
from json import JSONDecodeError
import datetime
import time
import pandas as pd

def parse(addr):
    while True:
        r = requests.get(addr)
        try:
            j = json.loads(r.text)

            depfares = j['journeyDateMarkets'][0]['lowFares']['lowestFares']
            dep_df = pd.DataFrame(depfares, columns=['date', 'price'])
            dep_df.index = pd.to_datetime(dep_df['date'])
            dep_df = dep_df.drop('date', 1)
            dep_df.columns = ['dep_price']

            arrfares = j['journeyDateMarkets'][1]['lowFares']['lowestFares']
            arr_df = pd.DataFrame(arrfares, columns=['date', 'price'])
            arr_df.index = pd.to_datetime(arr_df['date'])
            arr_df = arr_df.drop('date', 1)
            arr_df.columns = ['arr_price']

            df = pd.concat([dep_df, arr_df], axis=1)
            return df

        except OSError as e:
            print(e)
        except JSONDecodeError as e:
            continue
        break


def interval(start, dest):
    startfmt = start.strftime("%Y-%m-%d")
    end = start# + datetime.timedelta(days=10)
    endfmt = end.strftime("%Y-%m-%d")

    addr = 'https://tiger-wkgk.matchbyte.net/wkapi/v1.0/flightsearch?adults=1&children=0&infants=0&originStation=TPE&originStation='\
        +dest+'&destinationStation='+dest+'&destinationStation=TPE&departureDate='\
        +startfmt+'&departureDate='+endfmt+'&includeoverbooking=false&daysBeforeAndAfter=4&locale=zh-TW'
    return parse(addr)


def flight(dest):
    df = pd.DataFrame()
    for i in range(0, 10):
        start = datetime.datetime(2018, 1, 1, 0, 0, 0, 0) + datetime.timedelta(i*9)
        t_df = interval(start, dest)
        df = df.append(t_df)

    # print(df)
    df.to_csv(dest+'.csv')

if __name__ == '__main__':
    dest = ['KIX', 'FUK', 'HKD', 'NGO', 'OKA', 'OKJ', 'CJU', 'PUS', 'TAE']

    for _ in dest:
        flight(_)
    
