import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import statistics as st
from datetime import datetime
from math import ceil, pi

def LowPassFilter(array, sample_rate, frequency):
 dt = 1 / sample_rate
 RC = 1 / (2 * 3.14 * frequency)
 alpha = dt / (RC + dt)
 size = len(array)
 new_array = np.empty(size)
 for i in range(size):
  new_array[i] = alpha * array[i] + (1 - alpha) * new_array[i - 1]
 return new_array

def NormalizeArray(array):
 norm = np.linalg.norm(array)
 normal_array = array/norm
 return normal_array

def ValuesStd(error_max, array_x, array_y, approach):
    error = ceil(error_max)
    x = array_x
    y = array_y
    size = len(x)
    result = np.zeros(error)
    for i in range(error):
        abs_values = abs(x - y)
        result[i] = st.stdev(abs_values)
        if approach == False:
            y = np.delete(y, len(y) - 1)
            x = np.delete(x, 0)
        else:
            x = np.delete(x, len(x) - 1)
            y = np.delete(y, 0)
    return result

def FirstLocalMinimum(array, error_max):
 for i in range(1, ceil(error_max) - 1):
  if array[i] < array[i - 1] and array[i] < array[i + 1]:
   return i
 return error_max + 1

def Sincro(x, y): 
 error_max = int(len(x) * 0.05) + 1
 x = LowPassFilter(x, 1, pi)
 y = LowPassFilter(y, 1, pi)
 x = NormalizeArray(x)
 y = NormalizeArray(y)
 approach_neg = ValuesStd(error_max, x, y, False)
 approach_pos = ValuesStd(error_max, x, y, True)
 approach_neg_minimum = FirstLocalMinimum(approach_neg, error_max)
 approach_pos_minimum = FirstLocalMinimum(approach_pos, error_max)
 return -approach_neg_minimum if approach_neg_minimum <= approach_pos_minimum else approach_pos_minimum

# Test
if __name__ == '__main__':
    n = range(50)
    theta = (np.pi / 2) * np.array(n)
    npx = np.cos(theta)
    npy = np.sin(theta)
    sincro_value = Sincro(npx,npy)
    print("Sicro: ", sincro_value)
    plt.figure(figsize=(20, 10), dpi=80)
    plt.plot(range(len(n)), npx, npy)
    plt.show()