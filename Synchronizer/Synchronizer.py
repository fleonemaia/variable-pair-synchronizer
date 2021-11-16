import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statistics as stat
from scipy.signal import butter, lfilter, find_peaks
import os
import array as arr
from datetime import datetime
from scipy import signal

def syncro(data_path):
    data_set = begin_data_set(data_path)
    # if(len(data_set)>300):
    #     data_set = data_set[30:330]
    print("Data Size: ", len(data_set))
    range_error_max = int(len(data_set) * 0.05) + 1
    leftSD = array_off_SD(range_error_max, data_set, True)
    rightSD = array_off_SD(range_error_max, data_set, False)
    leftMinimum = firstLocalMinimum(leftSD, range_error_max)
    rightMinimum = firstLocalMinimum(rightSD, range_error_max)
    lagging = lagTime(leftMinimum, rightMinimum, data_set, range_error_max)
    return lagging
def begin_data_set(data_path):
    data_set = pd.read_csv(data_path, sep=" ", header=None)
    data_set.columns = ['time', 'X', 'Y']
    # data_set['X'] = butter_lowpass_filter(data_set['X'], 0.5, 10, 3)
    # data_set['Y'] = butter_lowpass_filter(data_set['Y'], 0.5, 10, 3)
    # data_set = data_set.iloc[20:]
    data_set['X'] = lowpassfilter(data_set['X'],1,3.14)
    data_set['Y'] = lowpassfilter(data_set['Y'], 1, 3.14)
    data_set['X'] = data_set['X'] / data_set['X'].max()
    data_set['Y'] = data_set['Y'] / data_set['Y'].max()
    do_plot1(data_set['X'], data_set['Y'])
    return data_set
def lowpassfilter(array_x, sample_rate, frequency):
    dt = 1 / sample_rate
    RC = 1 / (2 * np.pi * frequency)
    alpha = dt / (RC + dt)
    array_y = np.zeros(len(array_x))
    array_y[0] = alpha * array_x[0]
    for i in range(1,len(array_x)):
        array_y[i] = alpha * array_x[i] + (1 - alpha) * array_y[i - 1]
    return array_y
def array_off_SD(range_error_max, data_set, turn):
    X = data_set['X'].values.transpose()
    Y = data_set['Y'].values.transpose()
    sideSD = np.zeros(range_error_max)
    for k in range(range_error_max):
        abs_value_of_subtraction = abs(X - Y)
        sideSD[k] = standardDeviation(abs_value_of_subtraction)
        if turn == True:
            X, Y = cut_off_1(X, Y)
        else:
            X, Y = cut_off_2(X, Y)
    return sideSD
def standardDeviation(array_x):
    average = stat.mean(array_x)
    sum_of_derivation = 0
    for value in array_x:
        sum_of_derivation += (value) * (value)
    sum_of_derivation_average = sum_of_derivation / len(array_x)
    return np.sqrt(sum_of_derivation_average - (average * average))
def cut_off_1(X, Y):
    X = np.delete(X, len(X) - 1)
    Y = np.delete(Y, 0)
    return X, Y
def cut_off_2(X, Y):
    Y = np.delete(Y, len(Y) - 1)
    X = np.delete(X, 0)
    return X, Y
def firstLocalMinimum(sideSD, range_of_error):
    for i in range(1,range_of_error-1):
        if(sideSD[i]<sideSD[i - 1] and sideSD[i] < sideSD[i + 1]):
            return i
    return range_of_error + 1
def lagTime(leftMinimum, rightMinimum, data_set, range_error_max):
    X = data_set['X'].values.transpose()
    Y = data_set['Y'].values.transpose()
    print("Left: ", leftMinimum, " Right: ", rightMinimum)
    # if leftMinimum < rightMinimum:
    #     print("ESQUERDA")
    #     for i in range(leftMinimum):
    #         X, Y = cut_off_1(X, Y)
    #     do_plot2(X, Y)
    #     return toTime(data_set['time'][leftMinimum]) - toTime(data_set['time'][0])
    # elif rightMinimum < leftMinimum:
    #     print("DIREITA")
    #     for i in range(rightMinimum):
    #         X, Y = cut_off_2(X, Y)
    #     do_plot2(X, Y)
    #     return toTime(data_set['time'][rightMinimum]) - toTime(data_set['time'][0])
    if leftMinimum == (range_error_max + 1):
        print("NÂO MODIFICADO")
        do_plot2(X, Y)
        # return toTime("00:00:00.000")
        return datetime.now()-datetime.now()
    else:
        print("IGUAL")
        for i in range(leftMinimum):
            X, Y = cut_off_1(X, Y)
        do_plot2(X, Y)
        return toTime(data_set['time'][leftMinimum]) - toTime(data_set['time'][0])
def toTime(elementTime):
    return datetime.strptime(elementTime, '%H:%M:%S.%f')
def do_plot1(X, Y):
    plt.subplot(2,2,1)
    plt.plot(X, color='blue')
    plt.plot(Y, color='red')
def do_plot2(X, Y):
    plt.subplot(2,2,2)
    plt.plot(X, color='midnightblue')
    plt.plot(Y, color='crimson')

def do_plot0(data_path):
    fig, ax = plt.figure()
    fig.set_size_inches(12, 8)
    plt.title('VAZBAL (blue, green) and PRESSDEF (red, orange) X POINTS')
    lagging = syncro(data_path)
    txt = 'Na esquerda: o gráfico da tabela original. Na direita: o gráfico do ajuste executado nos dados.\nEm azul os valores de vazão da balança e em vermelho os valores da pressão defasada, ambos normalizados para visualização. Lagging total seconds: ' + lagging.total_seconds()
    fig.text(.5, .05, txt, ha='center')
    plt.draw()
    plt.savefig(r'Figure\figure_' + side[i] + '_' + str(j) + '_5' + '.png')
    plt.close()