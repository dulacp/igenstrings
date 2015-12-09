# -*- coding: utf-8 -*-

from sys import argv
from re import compile
from copy import copy
import os
import io
import shutil
import optparse
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

re_translation = compile(r'^"((?:[^"]|\\")+)" = "((?:[^"]|\\")+)";(?:\n)?$')
re_comment_single = compile(r'^/\*.*\*/$')
re_comment_start = compile(r'^/\*.*$')
re_comment_end = compile(r'^.*\*/$')

STRINGS_FILE = 'Localizable.strings'


class LocalizedString(object):

    def __init__(self, comments, translation):
        self.comments, self.translation = comments, translation
        self.key, self.value = re_translation.match(self.translation).groups()

    def __unicode__(self):
        return u"{}{}\n".format("".join(self.comments), self.translation)


class LocalizedFile(object):

    def __init__(self, filename=None):
        self.strings = []
        self.strings_d = {}

        if filename:
            self.filename = filename
            self.read()

    def read(self):
        with io.open(self.filename, encoding='utf16', mode='r') as f:
            line = f.readline()
            logger.debug(line)

            i = 1
            while line:
                comments = [line]

                if not re_comment_single.match(line):
                    while line and not re_comment_end.match(line):
                        line = f.readline()
                        comments.append(line)

                line = f.readline()
                i += 1

                # handle multi lines
                while len(line) > 1 and line[-2] != u';':
                    nextline = f.readline()
                    if not nextline:
                        nextline = '\n'
                    line += nextline
                    i += 1

                logger.debug("%d %s" % (i, line.rstrip('\n')))
                if line and re_translation.match(line):
                    translation = line
                else:
                    logger.error("Line {} of file '{}' raising the exception: {}".format(i, self.filename, line))
                    raise ValueError('invalid file')

                line = f.readline()
                i += 1
                while line and line == u'\n':
                    line = f.readline()
                    i += 1

                string = LocalizedString(comments, translation)
                self.strings.append(string)
                self.strings_d[string.key] = string

    def save(self, output_filename):
        with io.open(output_filename, encoding='utf16', mode='w') as f:
            # sort by key
            self.strings.sort(key=lambda item: item.key)
            for string in self.strings:
                f.write(string.__unicode__())

    def merge_with(self, new):
        merged = LocalizedFile()

        for string in new.strings:
            if string.key in self.strings_d:
                new_string = copy(self.strings_d[string.key])
                new_string.comments = string.comments
                string = new_string

            merged.strings.append(string)
            merged.strings_d[string.key] = string

        return merged

    def update_with(self, new):
        for string in new.strings:
            if not self.strings_d.has_key(string.key):
                self.strings.append(string)
                self.strings_d[string.key] = string


def merge(merged_fname, old_fname, new_fname):
    try:
        old = LocalizedFile(old_fname)
        new = LocalizedFile(new_fname)
        merged = old.merge_with(new)
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
