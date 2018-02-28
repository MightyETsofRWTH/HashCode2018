import argparse
import glob
from itertools import chain
from multiprocessing import Pool
import os

import solution


def main(files):
    files = list(chain(*[glob.glob(entry) for entry in files]))

    with Pool(os.cpu_count()-1) as pool:
        pool.map(solution.process, files)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='+', help="files to process, allows *s")
    args = parser.parse_args()

    main(args.files)
