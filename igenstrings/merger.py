# -*- coding: utf-8 -*-

import os
import shutil
import logging

from .i18n import LocalizedFile


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

STRINGS_FILE = 'Localizable.strings'


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
