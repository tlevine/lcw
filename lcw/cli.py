import argparse, sys, os

from more_itertools import ilen

from . import lcw

argparser = argparse.ArgumentParser('Estimate how many lines are in a file.')
argparser.add_argument('file', type = argparse.FileType('rb'))
argparser.add_argument('--sample-size', '-n', type = int, default = 100, dest = 'n',
                       help = 'Number of lines to sample for the estimate')
argparser.add_argument('--just-ml', '-j', action = 'store_true',
                       help = 'Only print the maximum likelihood estimate')


def main():
    args = argparser.parse_args()
    if args.n < 1:
        sys.stderr.write('Sample size must be at least one.\n')
        return 1

    # 99% gaussian confidence interval
    z = 2.575829

    filesize = os.stat(args.file.name).st_size
   #cdf = lcw.estimated_cdf(args.n, args.file)
    cdf = lcw.exact_cdf(args.file)
    pdf = list(lcw.pdf(cdf))
    estimated_mean = lcw.weighted_mean(pdf)
    standard_error_of_the_mean = (lcw.weighted_variance(estimated_mean, pdf)/args.n)**0.5
    radius = standard_error_of_the_mean * z

    maximum_likelihood = filesize / estimated_mean
    if args.just_ml:
        sys.stdout.write('%d\n' % maximum_likelihood)
    else:
        low = filesize / (estimated_mean + radius)
        high = filesize / (estimated_mean - radius)
        sys.stdout.write('Between %d and %d lines (99%% confidence)\n' % (low, high))

if __name__ == '__main__':
    main()
