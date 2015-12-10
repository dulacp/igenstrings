#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_igenstrings
----------------------------------

Tests for `igenstrings` module.
"""

import unittest
from codecs import open

from igenstrings.merger import Merger


class TestMergerIntegration(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_keep_existing_translated_strings(self):
        merger = Merger('tests/objc', None)
        merger.merge_localized_strings()
        content = None
        with open('tests/objc/fr.lproj/Localizable.strings', encoding='utf16', mode='r') as fr_locale_file:
            content = fr_locale_file.read()
        self.assertIn('Bonjour', content)
