from pickle import FALSE
import pandas as pd
from netCDF4 import Dataset
from datetime import timedelta
import datetime
import csv
import os
import numpy


def createCsv(lat, long):
    try:
        pd.read_csv("./data/"+str(lat)+"-"+str(long)+".csv")
        return True
    except FileNotFoundError:
        inp = Dataset('./data/latest.nc')
        sst = inp.variables['sst']

        sst_time = sst[:, long, lat]
        print(type(sst_time[0]))
        if (type(sst_time[0]) != numpy.float64):
            return False
        print("This is the SST")
        print(sst_time)
        sst_time -= 282
        str_title = './data/' + str(lat) + '-' + str(long) + '.csv'

        date = datetime.datetime(1999, 1, 1)

        with open('ref.csv', 'w') as f:

            writer = csv.writer(f)
            row = ["DATE", "DelT"]
            writer.writerow(row)
            for i in sst_time:
                # print(i)
                row = [date.strftime('%m/%d/%Y'), i]
                writer.writerow(row)
                date += timedelta(days=1)
        df = pd.read_csv('ref.csv')
        df.to_csv(str_title, index=False)

        os.remove('ref.csv')
        return True
