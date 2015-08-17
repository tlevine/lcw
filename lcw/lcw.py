import logging
from collections import Counter
from random import randint, random
import itertools

from sliding_window import window
from more_itertools import ilen

logger = logging.getLogger(__name__)

def count(fp, n = 10000, N = None, replace = False, character = b'\n',
          page_size = 2**16):
    '''
    Estimate how many times a particular character appears in a file.

    If data are appended to the file during the function call,
    the appended data are ignored for the sampling.

    :param int n: Number of samples
    :type fp: File-like object
    :param fp: The file to estimate line lengths of
    :param bool replace: Whether to sample with replacement
    :rtype: collections.Counter
    :returns: Exact cumulative distribution function of line length
    '''
    if n < 0:
        raise ValueError('Sample size must be greater than zero.')

    file_start = fp.tell()
    fp.seek(0, 2)
    file_end = fp.tell()

    if file_end <= file_start:
        raise ValueError('The file is empty, or you have seeked to a strange part of it.')
    elif file_end < file_start + page_size
        raise ValueError('File is too small; just use "wc -l".')

    if replace and file_end - file_start < n:
        raise ValueError('Your sample size is larger than the population of bytes in the file.')

    if replace:
        selections = list()
        save = selections.append
    else:
        raise NotImplementedError
        selections = set()
        save = selections.add

    count = 0
    while len(selections) < n:
        i = randint(file_start, file_end - 1)
        if replace or i not in selections:
            fp.seek(i)
            save(i)
            count += (fp.read(1) == character)

    x = count
    fp.seek(file_end - 1)
    x += (fp.read(1) == b'\n')
    
    p = x / n
    var_p = p * (1 - p)
    se_p = (var_p/n) ** .5

    # 99% gaussian confidence interval
    z = 2.575829

    # Population size
    if not N:
        N = os.stat(fp.name).st_size

    return {
        'low': (p - z * se_p) * N,
        'ml': p * N,
        'high': (p + z * se_p) * N,
    }
