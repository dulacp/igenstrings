#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_igenstrings
----------------------------------

Tests for `igenstrings` module.
"""

import unittest
from codecs import open

from igenstrings import parser


class TestIgenstrings(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_keep_existing_translated_strings(self):
        parser.merge_localized_strings('tests/objc', None)
        content = None
        with open('tests/objc/fr.lproj/Localizable.strings', encoding='utf16', mode='r') as fr_locale_file:
            content = fr_locale_file.read()
        self.assertIn('Bonjour', content)
