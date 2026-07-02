#module to mask an array based on a threshold value
import numpy as np

def mask(array, threshold):
    if (array[0] >= threshold):
        try:
            start_index = np.where(array <= threshold)[0][0]
            return array[start_index:]
        except IndexError:
            return np.array([])
    else:
        try:
            start_index = np.where(array >= threshold)[0][0]
            return array[start_index:]
        except IndexError:
            return np.array([])