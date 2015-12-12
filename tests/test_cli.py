#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from click.testing import CliRunner
from py import path

from igenstrings import cli


@pytest.fixture(autouse=True)
def initdir(tmpdir):
    fixture_basename = 'tests/objc'
    fixture_path = path.local(fixture_basename)
    fixture_path.copy(tmpdir / fixture_basename)
    tmpdir.chdir()  # change to pytest-provided temporary directory


@pytest.fixture
def runner():
    return CliRunner()


def test_cli(runner):
    result = runner.invoke(cli.main, ['tests/objc/existing'])
    assert result.exit_code == 0
    assert not result.exception
    assert result.output.strip().startswith('Running the script')


def test_cli_with_debug(runner):
    result = runner.invoke(cli.main, ['--debug', 'tests/objc/existing'])
    assert not result.exception
    assert result.exit_code == 0
    assert 'Debug mode is on' in result.output


# def test_cli_with_excluded_paths(runner):
#     result = runner.invoke(cli.main, ['--excluded-path tests/objc/existing', 'tests/objc/existing'])
#     assert result.exit_code == 0
#     assert not result.exception
#     assert result.output.strip() == 'Hello, {{ cookiecutter.full_name.split()[0] }}.'
