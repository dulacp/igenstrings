#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_igenstrings
----------------------------------

Tests for `igenstrings` module.
"""

import os
import unittest
from codecs import open

from py import path
import pytest

from igenstrings.merger import Merger


@pytest.fixture(autouse=True)
def initdir(tmpdir):
    fixture_basename = 'tests/objc'
    fixture_path = path.local(fixture_basename)
    fixture_path.copy(tmpdir / fixture_basename)
    tmpdir.chdir()  # change to pytest-provided temporary directory


def test_create_localizable_strings():
    merger = Merger('tests/objc/new', None)
    assert not os.path.exists('tests/objc/new/en.lproj/Localizable.strings')
    assert not os.path.exists('tests/objc/new/fr.lproj/Localizable.strings')
    merger.merge_localized_strings()
    assert os.path.exists('tests/objc/new/en.lproj/Localizable.strings')
    assert os.path.exists('tests/objc/new/fr.lproj/Localizable.strings')
    content = None
    with open('tests/objc/new/en.lproj/Localizable.strings', encoding='utf16', mode='r') as en_locale_file:
        content = en_locale_file.read()
    assert 'Hi' in content


def test_keep_existing_translated_strings():
    merger = Merger('tests/objc/existing', None)
    merger.merge_localized_strings()
    content = None
    with open('tests/objc/existing/fr.lproj/Localizable.strings', encoding='utf16', mode='r') as fr_locale_file:
        content = fr_locale_file.read()
    assert 'Bonjour' in content


def test_merge_new_translated_strings():
    merger = Merger('tests/objc/existing', None)
    merger.merge_localized_strings()
    content = None
    with open('tests/objc/existing/fr.lproj/Localizable.strings', encoding='utf16', mode='r') as fr_locale_file:
        content = fr_locale_file.read()
    assert 'How are you doing' in content


def test_linebreak_between_strings():
    merger = Merger('tests/objc/existing', None)
    merger.merge_localized_strings()
    content = None
    with open('tests/objc/existing/en.lproj/Localizable.strings', encoding='utf16', mode='r') as en_locale_file:
        content = en_locale_file.read()
    assert content == """/* title for the simple object */
"Hi %@ !" = "Hi %@ !";

/* subtitle for the simple object */
"How are you doing today" = "How are you doing today";
"""
