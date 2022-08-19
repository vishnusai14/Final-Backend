from netCDF4 import Dataset


inp = Dataset('data/latest.nc')
sst = inp.variables['sst']
sst_time = sst[:, 73.25, 10.25]

print(sst_time)