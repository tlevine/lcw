import argparse, sys, os

from more_itertools import ilen

from . import lcw

argparser = argparse.ArgumentParser('Estimate how many lines are in a file.')
argparser.add_argument('file', type = argparse.FileType('rb'))
argparser.add_argument('--sample-size', '-n', type = int, default = 100, dest = 'n',
                       help = 'Number of lines to sample for the estimate')


def main():
    args = argparser.parse_args()
    if args.n < 1:
        sys.stderr.write('Sample size must be at least one.\n')
        return 1

    filesize = os.stat(args.file.name).st_size
    cdf = lcw.estimated_cdf(args.n, args.file)
    average = lcw.inverse_cdf(cdf, 0.5)
    print(int(filesize / average))
    print(average)
    print(lcw.weighted_mean(lcw.pdf(cdf)))

if __name__ == '__main__':
    main()
