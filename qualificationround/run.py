import argparse
import glob
import shutil
from itertools import chain
from multiprocessing import Pool
import os

import solution


def main(files, sequential):
    files = list(chain(*[glob.glob(entry) for entry in files]))

    if sequential:
        for f in files:
            solution.process(f)
    else:
        with Pool(os.cpu_count()-1) as pool:
            pool.map(solution.process, files)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='+', help="files to process, allows *s")
    parser.add_argument('-s', '--sequential', action='store_true')
    args = parser.parse_args()

    main(args.files, args.sequential)