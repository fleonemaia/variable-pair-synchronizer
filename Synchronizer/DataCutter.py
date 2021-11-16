from numpy import isnan as isnan
import numpy as np
import pandas as pd

# Right Side

side = 'right'
data_name = 'Data\DataOriginals\data_'+side+'_sample.txt'
data_set = pd.read_csv(data_name, sep=' ', header=None)
data_set.columns = ['time', 'X', 'Y']
time = data_set['time'].values.transpose()
X = data_set['X'].values.transpose()
Y = data_set['Y'].values.transpose()
X = np.around(X,3)
Y = np.around(Y,4)
last = 0
j = 1
for i in range(len(data_set)):
    if isnan(X[i]):
        temp = pd.DataFrame({'time': time[last:i], 'X': X[last: i], 'Y': Y[last: i]})
        data_name = 'Data\data_'+side+'_'+str(j)
        temp.to_csv(data_name+'.txt', sep=' ', header=None, index=False)
        last = i+1
        j=j+1

# Left Side

side = 'left'
data_name = 'Data\DataOriginals\data_'+side+'_sample.txt'
data_set = pd.read_csv(data_name, sep=' ', header=None)
data_set.columns = ['time', 'X', 'Y']
time = data_set['time'].values.transpose()
X = data_set['X'].values.transpose()
Y = data_set['Y'].values.transpose()
X = np.around(X,3)
Y = np.around(Y,4)
last = 0
j = 1
for i in range(len(data_set)):
    if isnan(X[i]):
        temp = pd.DataFrame({'time': time[last:i], 'X': X[last: i], 'Y': Y[last: i]})
        data_name = 'Data\data_'+side+'_'+str(j)
        temp.to_csv(data_name+'.txt', sep=' ', header=None, index=False)
        last = i+1
        j=j+1