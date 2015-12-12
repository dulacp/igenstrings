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


class TestMerger(unittest.TestCase):
    pass


class TestMergerIntegration(unittest.TestCase):

    def setUp(self):
        super(TestMergerIntegration, self).setUp()

    @pytest.fixture(autouse=True)
    def initdir(self, tmpdir):
        fixture_basename = 'tests/objc'
        fixture_path = path.local(fixture_basename)
        fixture_path.copy(tmpdir / fixture_basename)
        tmpdir.chdir() # change to pytest-provided temporary directory

    def test_create_localizable_strings(self):
        merger = Merger('tests/objc/new', None)
        self.assertTrue(not os.path.exists('tests/objc/new/en.lproj/Localizable.strings'))
        self.assertTrue(not os.path.exists('tests/objc/new/fr.lproj/Localizable.strings'))
        merger.merge_localized_strings()
        self.assertTrue(os.path.exists('tests/objc/new/en.lproj/Localizable.strings'))
        self.assertTrue(os.path.exists('tests/objc/new/fr.lproj/Localizable.strings'))
        content = None
        with open('tests/objc/new/en.lproj/Localizable.strings', encoding='utf16', mode='r') as en_locale_file:
            content = en_locale_file.read()
        self.assertIn('Hi', content)

    def test_keep_existing_translated_strings(self):
        merger = Merger('tests/objc/existing', None)
        merger.merge_localized_strings()
        content = None
        with open('tests/objc/existing/fr.lproj/Localizable.strings', encoding='utf16', mode='r') as fr_locale_file:
            content = fr_locale_file.read()
        self.assertIn('Bonjour', content)

    def test_merge_new_translated_strings(self):
        merger = Merger('tests/objc/existing', None)
        merger.merge_localized_strings()
        content = None
        with open('tests/objc/existing/fr.lproj/Localizable.strings', encoding='utf16', mode='r') as fr_locale_file:
            content = fr_locale_file.read()
        self.assertIn('How are you doing', content)
