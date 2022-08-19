import pandas as pd
from netCDF4 import Dataset
from datetime import timedelta
import datetime
import csv
import os


def createCsv(lat, long):
    try:
        pd.read_csv("./data/"+str(lat)+"-"+str(long)+".csv")
    except FileNotFoundError:
        inp = Dataset('./data/latest.nc')
        sst = inp.variables['sst']

        sst_time = sst[:, lat, long]
        print(sst_time)
        sst_time -= 282
        str_title = './data/' + lat + '-' + long + '.csv'

        date = datetime.datetime(1999, 1, 1)

        with open('ref.csv', 'w') as f:

            writer = csv.writer(f)
            for i in sst_time:
                # print(i)
                row = [date.strftime('%m/%d/%Y'), i]
                writer.writerow(row)
                date += timedelta(days=1)
        df = pd.read_csv('ref.csv')
        df.to_csv(str_title, index=False)

        os.remove('ref.csv')
