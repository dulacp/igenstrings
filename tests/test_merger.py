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
    fixture_basename = 'tests/src'
    fixture_path = path.local(fixture_basename)
    fixture_path.copy(tmpdir / fixture_basename)
    tmpdir.chdir()  # change to pytest-provided temporary directory


##
# Obj-C support

def test_create_localizable_strings_for_objc():
    merger = Merger('tests/src/objc/new', None)
    merger.merge_localized_strings()
    assert os.path.exists('tests/src/objc/new/en.lproj/Localizable.strings')
    assert os.path.exists('tests/src/objc/new/fr.lproj/Localizable.strings')
    content = None
    with open('tests/src/objc/new/en.lproj/Localizable.strings', encoding='utf8', mode='r') as en_locale_file:
        content = en_locale_file.read()
    assert 'Hi' in content


def test_keep_existing_translated_strings():
    merger = Merger('tests/src/objc/existing', None)
    merger.merge_localized_strings()
    content = None
    with open('tests/src/objc/existing/fr.lproj/Localizable.strings', encoding='utf8', mode='r') as fr_locale_file:
        content = fr_locale_file.read()
    assert 'Bonjour' in content


def test_merge_new_translated_strings():
    merger = Merger('tests/src/objc/existing', None)
    merger.merge_localized_strings()
    content = None
    with open('tests/src/objc/existing/fr.lproj/Localizable.strings', encoding='utf8', mode='r') as fr_locale_file:
        content = fr_locale_file.read()
    assert 'How are you doing' in content


def test_linespace_between_strings():
    merger = Merger('tests/src/objc/existing', None)
    merger.merge_localized_strings()
    content = None
    with open('tests/src/objc/existing/en.lproj/Localizable.strings', encoding='utf8', mode='r') as en_locale_file:
        content = en_locale_file.read()
    assert content == """/* title for the simple object */
"Hi %@ !" = "Hi %@ !";

/* subtitle for the simple object */
"How are you doing today" = "How are you doing today";
"""


def test_escape_double_quotes():
    merger = Merger('tests/src/objc/doublequotes', None)
    merger.merge_localized_strings()
    content = None
    with open('tests/src/objc/doublequotes/en.lproj/Localizable.strings', encoding='utf8', mode='r') as en_locale_file:
        content = en_locale_file.read()
    assert content == """/* title for the simple object */
"Hi \\"%@\\" !" = "Hi \\"%@\\" !";
"""


def test_escape_linebreaks():
    merger = Merger('tests/src/objc/linebreaks', None)
    merger.merge_localized_strings()
    content = None
    with open('tests/src/objc/linebreaks/en.lproj/Localizable.strings', encoding='utf8', mode='r') as en_locale_file:
        content = en_locale_file.read()
    assert content == """/* title for the simple object */
"Hello \\nworld!" = "Hello \\nworld!";
"""


def test_cannot_parse_malformatted_strings():
    merger = Merger('tests/src/objc/malformatted', None)
    with pytest.raises(Exception) as excinfo:
        merger.merge_localized_strings()
    assert isinstance(excinfo.value, ValueError)


def test_excluded_path():
    merger = Merger('tests/src/objc/exclusion', ['tests/src/objc/exclusion/ExcludedDirectory/*.m'])
    merger.merge_localized_strings()
    with open('tests/src/objc/exclusion/en.lproj/Localizable.strings', encoding='utf8', mode='r') as en_locale_file:
        content = en_locale_file.read()
    assert 'Should be excluded from localization' not in content


def test_works_with_utf8_encoding():
    merger = Merger('tests/src/objc/utf8', None)
    merger.merge_localized_strings()
    content = None
    with open('tests/src/objc/utf8/fr.lproj/Localizable.strings', encoding='utf8', mode='r') as fr_locale_file:
        content = fr_locale_file.read()
    assert 'Bonjour' in content


def test_works_with_ascii_encoding():
    merger = Merger('tests/src/objc/ascii', None)
    merger.merge_localized_strings()
    content = None
    with open('tests/src/objc/ascii/fr.lproj/Localizable.strings', encoding='utf8', mode='r') as fr_locale_file:
        content = fr_locale_file.read()
    assert 'Bonjour' in content


def test_raise_error_with_utf16_encoding():
    merger = Merger('tests/src/objc/utf16', None)
    with pytest.raises(Exception) as excinfo:
        merger.merge_localized_strings()
    assert isinstance(excinfo.value, ValueError)


##
# Obj-C++ support

def test_create_localizable_strings_for_objcpp():
    merger = Merger('tests/src/objcpp/new', None)
    merger.merge_localized_strings()
    assert os.path.exists('tests/src/objcpp/new/en.lproj/Localizable.strings')
    assert os.path.exists('tests/src/objcpp/new/fr.lproj/Localizable.strings')
    content = None
    with open('tests/src/objcpp/new/en.lproj/Localizable.strings', encoding='utf8', mode='r') as en_locale_file:
        content = en_locale_file.read()
    assert 'Hi' in content


##
# Swift support

def test_create_localizable_strings_for_swift():
    merger = Merger('tests/src/swift/new', None)
    merger.merge_localized_strings()
    assert os.path.exists('tests/src/swift/new/en.lproj/Localizable.strings')
    assert os.path.exists('tests/src/swift/new/fr.lproj/Localizable.strings')
    content = None
    with open('tests/src/swift/new/en.lproj/Localizable.strings', encoding='utf8', mode='r') as en_locale_file:
        content = en_locale_file.read()
    assert 'Hi' in content
