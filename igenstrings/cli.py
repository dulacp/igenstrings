from os import getcwd
from os.path import realpath
from argparse import ArgumentParser

from clint import arguments

from parser import merge_localized_strings


if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument("-d", "--debug",
            action="store_true", default=False, dest="debug",
            help="Set to DEBUG the logging level (default to INFO)")

    parser.add_argument("-p", "--path",
            action="store", type=str, default=None, dest="path",
            help="Path (relative or absolute) to use for searching for *.lproj directories")

    parser.add_argument("-e", "--exclude",
            action="store", type=str, default=None, dest="excluded_paths",
            help="Regex for paths to exclude eg. ``./Folder1/*``")

    opts = parser.parse_args()

    if opts.debug:
        logger.level = logging.DEBUG
    if opts.path:
        opts.path = realpath(opts.path)
    if opts.excluded_paths:
        opts.excluded_paths = realpath(opts.excluded_paths)

    logger.info("Running the script on path %s" % opts.path)
    merge_localized_strings(opts.path, opts.excluded_paths)
