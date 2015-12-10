# -*- coding: utf-8 -*-

import os
import shutil
import logging

from .i18n import LocalizedFile


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

STRINGS_FILE = 'Localizable.strings'


class Merger(object):

    def __init__(self, path, excluded_paths, logging_level=logging.INFO):
        super(Merger, self).__init__()
        self.path = path
        self.excluded_paths = excluded_paths
        logger.level = logging_level

    def _merge(self, merged_fname, old_fname, new_fname):
        old = LocalizedFile()
        old.read(old_fname)
        new = LocalizedFile()
        new.read(new_fname)
        merged = old.merge(new)
        merged.save(merged_fname)

    def _get_languages(self):
        languages = []
        for root, dirs, files in os.walk(self.path):
            logger.debug(dirs)
            for name in dirs:
                if name.endswith('.lproj'):
                    languages.append(os.path.join(root, name))
        return languages

    def _run_genstrings(self, lang):
        os.system('find {} -name \*.m -or -name \*.mm -not -path "{}" | xargs genstrings -q -o "{}"'.format(
            self.path,
            self.excluded_paths,
            lang))

    def _merge_locale(self, lang):
        final_filename = os.path.join(lang, STRINGS_FILE)
        old_filename = '{}.old'.format(final_filename)
        new_filename = '{}.new'.format(final_filename)

        if not os.path.exists(final_filename):
            # create the initial localized strings
            self._run_genstrings(lang)
            return

        os.rename(final_filename, old_filename)
        self._run_genstrings(lang)
        shutil.copy(final_filename, new_filename)

        # merge
        self._merge(final_filename, old_filename, new_filename)
        logger.info("Job done for lang: %s" % lang)
        os.remove(old_filename)
        os.remove(new_filename)

    def merge_localized_strings(self):
        languages = self._get_languages()
        logger.info("languages found : {}".format(languages))
        for lang in languages:
            self._merge_locale(lang)
