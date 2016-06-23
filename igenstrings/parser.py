# -*- coding: utf-8 -*-

import re


class LocalizedString(object):

    def __init__(self, key, value, comment="no comment"):
        self.key = key
        self.value = value
        self.comment = comment


class AppleStringsParser(object):
    """
    Parser for Apple STRINGS translation files.

    inspired by the transifex implementation
    https://github.com/transifex/transifex/blob/master/transifex/resources/formats/strings.py

    NB: Apple strings files *must* be encoded in UTF-16 encoding.
    """

    @classmethod
    def format_string(cls, s):
        """
        Format a `LocalizedString` instance
        """
        return u'/*{}*/\n"{}" = "{}";\n'.format(s.comment, s.key, s.value)

    def _unescape_key(self, s):
        return s.replace('\\\n', '')

    def _unescape(self, s):
        s = s.replace('\\\n', '')
        return s.replace(r'\n', '\n').replace(r'\r', '\r')

    def parse(self, content):
        """
        Parse an apple .strings file and create a stringset with all entries in the file.

        See Apple spec for details.
        https://developer.apple.com/library/ios/documentation/MacOSX/Conceptual/BPInternational/MaintaingYourOwnStringsFiles/MaintaingYourOwnStringsFiles.html
        """
        stringset = []

        f = content
        f = f.lstrip(u'\ufeff')  # in case the file contains this Big/Little edian char

        #regex for finding all comments in a file
        cp = r'(?:/\*(?P<comment>(?:[^*]|(?:\*+[^*/]))*\**)\*/)'
        p = re.compile(r'(?:%s[ \t]*[\n]|[\r\n]|[\r]){0,1}(?P<line>("(?P<key>[^"\\]*(?:\\.[^"\\]*)*)")\s*=\s*"(?P<value>[^"\\]*(?:\\.[^"\\]*)*)"\s*;)'%cp, re.DOTALL|re.U)
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
            value = i.group('value')
            while end < start:
                m = c.match(f, end, start) or ws.match(f, end, start)
                if not m or m.start() != end:
                    raise ValueError("Invalid syntax: %s" % f[end:start])
                end = m.end()
            end = end_
            key = self._unescape_key(key)
            stringset.append(LocalizedString(key, self._unescape(value), comment=comment))

        return stringset
