#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from click.testing import CliRunner

from igenstrings import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_cli(runner):
    result = runner.invoke(cli.main, ['tests/objc'])
    assert result.exit_code == 0
    assert not result.exception
    assert result.output.strip().startswith('Running the script')


def test_cli_with_debug(runner):
    result = runner.invoke(cli.main, ['--debug', 'tests/objc'])
    assert not result.exception
    assert result.exit_code == 0
    assert 'Debug mode is on' in result.output


# def test_cli_with_excluded_paths(runner):
#     result = runner.invoke(cli.main, ['--excluded-path tests/objc', 'tests/objc'])
#     assert result.exit_code == 0
#     assert not result.exception
#     assert result.output.strip() == 'Hello, {{ cookiecutter.full_name.split()[0] }}.'
