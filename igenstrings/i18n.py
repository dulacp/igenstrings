# -*- coding: utf-8 -*-

import io
import copy

from .parser import AppleStringsParser, LocalizedString


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
            formatted_strings = '\n'.join(AppleStringsParser.format_string(s) for s in self.stringset)
            f.write(formatted_strings)

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
                old_string = copy.copy(stringsdict[new_string.key])
                old_string.comment = new_string.comment
                new_string = old_string
            merged.stringset.append(new_string)
        return merged
