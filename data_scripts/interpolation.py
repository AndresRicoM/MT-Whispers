import numpy as np
import math
from progressbar import printProgressBar

def interpolate(first, last, spaces): #Takes as argument first number, last number and the number of spaces in between.
    result = np.zeros((spaces, 1))
    delta = abs(last - first) / (spaces + 1)
    if first < last or first == last:
        for rows in range(0,result.shape[0]):
            if rows == 0:
                result[rows, 0] = first
            elif rows == result.shape[0] - 1:
                result[rows, 0] = last
            else:
                result[rows,0] = first + ((rows + 1) * delta)
        return result
    if first > last:
        for rows in range(0,result.shape[0]):
            result[rows,0] = first - ((rows + 1) * delta)
        return result

#print(interpolate(4336.4531,4336.4536,8))
