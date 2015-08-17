import argparse, sys, os

from more_itertools import ilen

from . import lcw

argparser = argparse.ArgumentParser('Estimate how many lines are in a file.')
argparser.add_argument('file', type = argparse.FileType('rb'))
argparser.add_argument('--sample-size', '-n', type = int, default = 100, dest = 'n',
                       help = 'Number of lines to sample for the estimate')
argparser.add_argument('--confidence', '-c', type = int, default = .99,
                       help = 'Confidence level')


def main():
    args = argparser.parse_args()
    if args.n < 1:
        sys.stderr.write('Sample size must be at least one.\n')
        return 1
    elif not (0 < args.confidence < 1):
        sys.stderr.write('Confidence level must be between 0 and 1, exclusive.\n')
        return 1

    filesize = os.stat(args.file.name).st_size
    cdf = lcw.estimated_cdf(args.n, args.file)
    average = lcw.inverse_cdf(cdf, 0.5)
    print(int(filesize / average))

if __name__ == '__main__':
    main()
