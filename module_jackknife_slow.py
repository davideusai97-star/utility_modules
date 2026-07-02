import numpy as np
import sys
sys.path.append(r'C:\Users\david\OneDrive\Desktop\scolastiche\magistrale\moduli')

from module_divisors import find_divisors # type: ignore

#Takes a 1D array of data and shortens it to a length with at least MIN_NUM_DIVISORS useful divisors
#Calculates and returns the Jackknife sigma array of a generic function
MIN_NUM_DIVISORS=6

def jackknife_gen_unsure(array, stat_func, **stat_kwargs):
    """
    Generic jackknife over contiguous blocks.
    - array: 1-D sequence of raw data values
    - stat_func: callable(sample: 1D-array, **stat_kwargs) -> scalar or 1D-array statistic
    - stat_kwargs: extra kwargs forwarded to stat_func

    Returns: sigma (np.array). If return_block_sizes True, returns (sigma, block_sizes).
    """
    m = np.asarray(array).ravel()
    if m.size < 1:          #flag for empty array
        raise ValueError("array must contain at least one element.")

    new_length, block_sizes = find_divisors(len(m), MIN_NUM_DIVISORS)   #find at least MIN_NUM_DIVISORS divisors of numbers close to N
    cutoff = len(m) - new_length
    m = m[cutoff:]                      #adapt array to new length to maximise useful divisors
    N = len(m)

    sigmas = []
    for k in block_sizes:
        n_blocks = N // k
        stats = []
        for i in range(n_blocks):
            start = i * k
            stop = (i + 1) * k
            # leave-one-block-out sample
            sample = np.concatenate((m[:start], m[stop:])) if start > 0 else m[stop:]
            stat_val = np.asarray(stat_func(sample, **stat_kwargs))
            stats.append(stat_val)
        stats = np.stack(stats, axis=0)      # shape (n_blocks, ...)

        mean_stat = np.mean(stats, axis=0)
        # jackknife variance scaling ((N - k)/N) * sum((theta_i - mean)^2)
        var = ((N - k) / N) * np.sum((stats - mean_stat) ** 2, axis=0)
        sigmas.append(np.sqrt(var))

    sigmas = np.stack(sigmas, axis=0)  # shape (n_block_sizes, ...)

    return sigmas