from os import getcwd
from os.path import realpath
import logging

import click

from .merger import Merger


@click.command()
@click.argument('path',
    type=click.Path(exists=True))
@click.option('--debug',
    default=False,
    is_flag=True,
    help='Configure the output for debugging purposes')
@click.option('--excluded-path',
    default=None,
    help='Regex for paths to exclude eg. ``./Folder1/*``')
def main(path, debug, excluded_path):
    if debug:
        logging_level = logging.DEBUG
    else:
        logging_level = logging.INFO
    if path:
        path = realpath(path)
    if excluded_path:
        excluded_path = realpath(excluded_path)

    click.echo(click.style('Running the script on path {}'.format(path), fg='green'))
    click.echo(click.style('Excluded path regex: {}'.format(excluded_path), fg='red'))
    if logging_level == logging.DEBUG:
        click.echo(click.style('Debug mode is on', fg='red'))

    merger = Merger(path, excluded_path, logging_level=logging_level)
    merger.merge_localized_strings()
    click.echo(click.style('Done', fg='green'))
