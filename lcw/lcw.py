import logging
from collections import Counter
from random import randint, random
import itertools

from sliding_window import window
from more_itertools import ilen

logger = logging.getLogger(__name__)

def estimated_cdf(n, fp, give_up_at = 100):
    '''
    Estimate the cumulative distribution function of line lengths.

    If data are appended to the file during the function call,
    the appended data are ignored for the sampling.
    Samples are with replacement.

    :param int n: Number of samples
    :type fp: File-like object
    :param fp: The file to estimate line lengths of
    :rtype: collections.Counter
    :returns: Exact cumulative distribution function of line length
    '''
    if n < 0:
        raise ValueError('Sample size must be greater than zero.')

    file_start = 0
    fp.seek(0, 2)
    file_end = fp.tell()

    negative_absolute_cdf = Counter()
    for i in itertools.count():

        # Select a random byte.
        fp.seek(randint(file_start, file_end))

        line = fp.readline()
        if line.endswith(b'\n'):
            negative_absolute_cdf[len(line)] += 1
            if sum(negative_absolute_cdf.values()) == n:
                break

        elif i > give_up_at and len(negative_absolute_cdf) < (i / give_up_at):
            raise EnvironmentError('This file probably doesn\'t have enough lines.')

    cdf = Counter()
    total = 0
    for i in sorted(negative_absolute_cdf):
        total += negative_absolute_cdf[i]
        cdf[i] = 1 - total / n
    return cdf

def exact_cdf(fp):
    '''
    Cumulative distribution function of line lengths.

    :type fp: File-like object
    :param fp: The file to estimate line lengths of
    :rtype: collections.Counter
    :returns: Exact cumulative distribution function of line length
    '''
    negative_absolute_cdf = Counter()
    n = 0

    for line in fp:
        for i in range(len(line)):
            negative_absolute_cdf[i] += 1
            n += 1

    cdf = Counter()
    total = 0
    for i in sorted(negative_absolute_cdf):
        total += negative_absolute_cdf[i]
        cdf[i] = total / n
    return cdf


def resample(cdf, total_length):
    '''
    Generate a distribution of line lengths with a particular total length.
    '''
    length = 0
    while length < total_length:
        r = random()
        for line_length in sorted(cdf):
            if cdf[line_length] > r:
                yield line_length
                length += line_length
                break
