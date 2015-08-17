import logging
from collections import Counter
from random import sample
import itertools

logger = logging.getLogger(__name__)

def count(fp, n = 100, character = b'\n', page_size = 2**16):
    '''
    Estimate how many times a particular character appears in a file.

    If data are appended to the file during the function call,
    the appended data are ignored for the sampling.
    Sampling is without replacement

    :param int n: Number of samples
    :type fp: File-like object
    :param fp: The file to estimate line lengths of
    :rtype: collections.Counter
    :returns: Exact cumulative distribution function of line length
    '''
    if n < 0:
        raise ValueError('Sample size must be greater than zero.')

    file_start = fp.tell()
    fp.seek(0, 2)
    file_end = fp.tell()

    # Population size
    N = int((file_end - file_start) / page_size)

    if file_end <= file_start:
        raise ValueError('The file is empty, or you have seeked to a strange part of it.')
    elif file_end < file_start + page_size:
        raise ValueError('File is too small; just use "wc -l".')
    elif file_end - file_start < n:
        raise ValueError('Your sample size is larger than the population of bytes in the file.')

    def f(i):
        fp.seek(i * page_size)
        return fp.read(page_size).count(character)

    ts = list(map(f, sorted(sample(range(0, N), n))))
    E_t_sample = sum(ts) / n
    Var_t_sample = sum((t - E_t_sample) ** 2 for t in ts) / (n - 1)

    # 99% gaussian confidence interval
    z = 2.575829

    # Levy & Lemeshow, page 51
    fpc = (N - n) / N
    E_t_population = N * E_t_sample
    Var_t_population = (N ** 2) * fpc * Var_t_sample / n
    SE_t_population = Var_t_population ** 0.5

    return {
        'ml': E_t_population,
        'radius': z * SE_t_population,
    }
