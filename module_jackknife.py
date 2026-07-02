import numpy as np
import sys
sys.path.append(r'C:\Users\david\OneDrive\Desktop\scolastiche\magistrale\moduli')

from module_divisors import find_divisors  # type: ignore

#Takes a 1D array of data and shortens it to a length with at least MIN_NUM_DIVISORS useful divisors
#Calculates and returns the Jackknife sigma array


# Minimum number of useful divisors for block sizes
MIN_NUM_DIVISORS = 6

def jackknife(array):

    if len(array) < 1:
        raise ValueError("Input array must have at least two elements.")

    m = np.copy(array)
    new_length, block_sizes = find_divisors(len(m), MIN_NUM_DIVISORS)
    cutoff = len(m) - new_length
    m = m[cutoff:]  # adjust length
    N = len(m)

    total_sum = np.sum(m)
    var_jack = []        #array totale delle varianze per diversi k

    for k in block_sizes:  # loop over block sizes
        n_blocks = N // k
        block_means = []

        for i in range(n_blocks):       #scorrimento sui blocchi
            start = i * k            #primo elemento blocco i-esimo
            stop = (i + 1) * k       #ultimo elemento blocco i-esimo
            sum_block = np.sum(m[start:stop])   #somma del blocco i

            # leave-one-block-out mean
            mean_i = (total_sum - sum_block) / (N - k)
            block_means.append(mean_i)

        mean_jack = np.mean(block_means)

        # jackknife variance of the mean
        var_k = ((n_blocks - 1) / n_blocks) * np.sum((block_means - mean_jack)**2)       # prefattore uguale a (N-K)/N
        var_jack.append(var_k)    # create array of jackknife variances

    sigma_jack = np.sqrt(var_jack)        # Array of jackknife standard deviations for different block sizes.

    return mean_jack, sigma_jack