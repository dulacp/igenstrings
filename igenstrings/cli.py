from os import getcwd
from os.path import realpath
import logging

import click

from .parser import merge_localized_strings


@click.command()
@click.option('--debug',
    default=False,
    help='Set to DEBUG the logging level (default to INFO)')
@click.option('--path',
    prompt='Indicate the project classes directory path',
    help='Path (relative or absolute) to use for searching for *.lproj directories')
@click.option('--excluded-path',
    default=None,
    help='Regex for paths to exclude eg. ``./Folder1/*``')
def main(debug, path, excluded_path):
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
    merge_localized_strings(path, excluded_path, logging_level=logging_level)
