import argparse, sys, os

from more_itertools import ilen

from . import lcw

argparser = argparse.ArgumentParser('Estimate how many lines are in a file.')
argparser.add_argument('file', type = argparse.FileType('rb'))
argparser.add_argument('--sample-size', '-n', type = int, default = 1000, dest = 'n',
                       help = 'Number of lines to sample for the estimate')
argparser.add_argument('--just-ml', '-j', action = 'store_true',
                       help = 'Only print the maximum likelihood estimate')


def main():
    args = argparser.parse_args()
    if args.n < 1:
        sys.stderr.write('Sample size must be at least one.\n')
        return 1

    stats = lcw.count(args.file, n = args.n)
    if args.just_ml:
        sys.stdout.write('%d\n' % stats['ml'])
    else:
        sys.stdout.write('%(ml)d ± %(radius)d lines (99%% confidence)\n' % stats)

if __name__ == '__main__':
    main()
