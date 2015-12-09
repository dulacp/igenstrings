# -*- coding: utf-8 -*-

from sys import argv
from copy import copy
import os
import io
import re
import shutil
import optparse
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

STRINGS_FILE = 'Localizable.strings'


class LocalizedString(object):

    def __init__(self, key, value, comment="no comment"):
        self.key = key
        self.value = value
        self.comment = comment

    def __unicode__(self):
        return u'/*{}*/\n"{}" = "{}";\n'.format(self.comment, self.key, self.value)


class LocalizedFile(object):

    def __init__(self, strings=None):
        """
        :param: strings a list of `LocalizedString` instances
        """
        self.stringset = strings or []

    def read(self, input_filename):
        with io.open(input_filename, encoding='utf16', mode='r') as f:
            parser = AppleStringsParser()
            content = f.read()
            strings = parser.parse(content)
            self.stringset = strings

    def save(self, output_filename):
        if not self.stringset:
            raise ValueError("Can't saved a file with no strings defined")

        with io.open(output_filename, encoding='utf16', mode='w') as f:
            # sort by key
            self.stringset.sort(key=lambda item: item.key)
            for string in self.stringset:
                f.write(string.__unicode__())

    def _get_stringsdict(self):
        """Turns the stringset into a `dict`"""
        s_dict = {}
        for s in self.stringset:
            s_dict[s.key] = s
        return s_dict

    def merge(self, other):
        """
        Merge the current file strings with the given other file strings
        by taking any other string as the newer version

        :param: other another instance of `LocalizedFile`
        :return: the merged `LocalizedFile` instance
        """
        merged = LocalizedFile()
        stringsdict = self._get_stringsdict()
        for new_string in other.stringset:
            if new_string.key in stringsdict:
                old_string = copy(stringsdict[new_string.key])
                old_string.comment = new_string.comment
                new_string = old_string
            merged.stringset.append(new_string)
        return merged


class AppleStringsParser(object):
    """
    Parser for Apple STRINGS translation files.

    inspired by the transifex implementation
    https://github.com/transifex/transifex/blob/master/transifex/resources/formats/strings.py

    NB: Apple strings files *must* be encoded in UTF-16 encoding.
    """

    def _escape(self, s):
        return s.replace('"', '\\"').replace('\n', r'\n').replace('\r', r'\r')

    def _unescape_key(self, s):
        return s.replace('\\\n', '')

    def _unescape(self, s):
        s = s.replace('\\\n', '')
        return s.replace('\\"', '"').replace(r'\n', '\n').replace(r'\r', '\r')

    def parse(self, content):
        """
        Parse an apple .strings file and create a stringset with all entries in the file.

        See Apple spec for details.
        https://developer.apple.com/library/ios/documentation/MacOSX/Conceptual/BPInternational/MaintaingYourOwnStringsFiles/MaintaingYourOwnStringsFiles.html
        """
        stringset = []

        f = content
        prefix = ""
        if f.startswith(u'\ufeff'):
            prefix = u'\ufeff'
            f = f.lstrip(u'\ufeff')

        #regex for finding all comments in a file
        cp = r'(?:/\*(?P<comment>(?:[^*]|(?:\*+[^*/]))*\**)\*/)'
        p = re.compile(r'(?:%s[ \t]*[\n]|[\r\n]|[\r]){0,1}(?P<line>(("(?P<key>[^"\\]*(?:\\.[^"\\]*)*)")|(?P<property>\w+))\s*=\s*"(?P<value>[^"\\]*(?:\\.[^"\\]*)*)"\s*;)'%cp, re.DOTALL|re.U)
        #c = re.compile(r'\s*/\*(.|\s)*?\*/\s*', re.U)
        c = re.compile(r'//[^\n]*\n|/\*(?:.|[\r\n])*?\*/', re.U)
        ws = re.compile(r'\s+', re.U)

        end = 0
        start = 0
        for i in p.finditer(f):
            start = i.start('line')
            end_ = i.end()
            line = i.group('line')
            key = i.group('key')
            comment = i.group('comment') or ''
            if not key:
                key = i.group('property')
            value = i.group('value')
            while end < start:
                m = c.match(f, end, start) or ws.match(f, end, start)
                if not m or m.start() != end:
                    raise StringsParseError("Invalid syntax: %s" %\
                            f[end:start])
                end = m.end()
            end = end_
            key = self._unescape_key(key)
            stringset.append(LocalizedString(key, self._unescape(value), comment=comment))

        return stringset


def merge(merged_fname, old_fname, new_fname):
    try:
        old = LocalizedFile()
        old.read(old_fname)
        new = LocalizedFile()
        new.read(new_fname)
        merged = old.merge(new)
        merged.save(merged_fname)
    except Exception as inst:
        logger.error('Error: input files have invalid format : {}'.format(inst))
        raise


def merge_localized_strings(path, excluded_paths, logging_level=logging.INFO):
    logger.level = logging_level

    languages = []
    for root, dirs, files in os.walk(path):
        logger.debug(dirs)
        for name in dirs:
            if name.endswith('.lproj'):
                languages.append(os.path.join(root, name))

    logger.info("languages found : {}".format(languages))

    for language in languages:
        original = merged = os.path.join(language, STRINGS_FILE)
        old = original + '.old'
        new = original + '.new'

        def rungenstrings():
            os.system('find %s -name \*.m -or -name \*.mm -not -path "%s" | xargs genstrings -q -o "%s"' % (path, excluded_paths, language))

        if os.path.exists(original):
            os.rename(original, old)
            rungenstrings()
            shutil.copy(original, new)

            # merge
            merge(merged, old, new)
            logger.info("Job done for language: %s" % language)
        else:
            rungenstrings()

        if os.path.exists(old):
            os.remove(old)
        if os.path.exists(new):
            os.remove(new)
