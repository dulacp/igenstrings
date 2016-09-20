# -*- coding: utf-8 -*-

import os
import codecs
import shutil
import logging

from chardet.universaldetector import UniversalDetector

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

    def _find_encoding(self, filename):
        detector = UniversalDetector()
        for line in open(filename, 'rb'):
            detector.feed(line)
            if detector.done: break
        detector.close()
        best_guess_encoding = detector.result.get('encoding')
        return best_guess_encoding

    def _merge(self, merged_fname, old_fname, new_fname, encoding='utf8'):
        old = LocalizedFile()
        old.read(old_fname, encoding=encoding)
        new = LocalizedFile()
        new.read(new_fname, encoding=encoding)
        merged = old.merge(new)
        merged.save(merged_fname, encoding=encoding)

    def _get_languages(self):
        languages = []
        for root, dirs, files in os.walk(self.path):
            logger.debug(dirs)
            for name in dirs:
                if name.endswith('.lproj'):
                    languages.append(os.path.join(root, name))
        return languages

    def _convert_encoding(self, source_filename, souce_encoding, target_filename, target_encoding):
        block_size = 1024
        with codecs.open(source_filename, "rb", souce_encoding) as sourceFile:
            with codecs.open(target_filename, "wb", target_encoding) as targetFile:
                while True:
                    contents = sourceFile.read(block_size)
                    if not contents:
                        break
                    targetFile.write(contents)

    def _run_genstrings(self, lang):
        if self.excluded_paths:
            exclusion_options = ' '.join('-not -path "{}"'.format(excl_path) for excl_path in self.excluded_paths)
        else:
            exclusion_options = ''
        cmd = 'find {} {} -name \*.m -or -name \*.mm -or -name \*.swift | xargs genstrings -q -o "{}"'.format(
            self.path,
            exclusion_options,
            lang)
        os.system(cmd)

        # convert the generated utf-16 to utf-8
        # cause now Apple is recommending UTF-8
        final_filename = os.path.join(lang, STRINGS_FILE)
        utf8_final_filename = "{}.encoded"
        self._convert_encoding(final_filename, 'utf-16', utf8_final_filename, 'utf-8')
        os.remove(final_filename)
        os.rename(utf8_final_filename, final_filename)

    def _merge_locale(self, lang):
        final_filename = os.path.join(lang, STRINGS_FILE)
        old_filename = '{}.old'.format(final_filename)
        new_filename = '{}.new'.format(final_filename)

        if not os.path.exists(final_filename):
            # create the initial localized strings
            self._run_genstrings(lang)
            return

        encoding = self._find_encoding(final_filename)
        if encoding is None:
            logger.warn("No encoding found for your file '{}'. You should use UTF-8 encoding as recommended by Apple.")
            encoding = 'utf-8'  # fallback
        if encoding.lower().startswith('utf-16'):
            raise ValueError("igenstrings now only supports UTF-8 encoded files how recommended by Apple. "
                             "We found your file to be encoded with `{}`. "
                             "Please convert your file to proceed, with iconv for instance".format(encoding))
        if not encoding.lower().startswith('utf-8'):
            logger.warn("It's recommended to encode your file '{}' with the UTF-8 encoding, "
                        "instead we found '{}', behavior is unexpected".format(final_filename, encoding))

        os.rename(final_filename, old_filename)
        self._run_genstrings(lang)
        shutil.copy(final_filename, new_filename)

        # merge
        self._merge(final_filename, old_filename, new_filename, encoding=encoding)
        logger.info("Job done for lang: %s" % lang)
        os.remove(old_filename)
        os.remove(new_filename)

    def merge_localized_strings(self):
        languages = self._get_languages()
        logger.info("languages found : {}".format(languages))
        for lang in languages:
            self._merge_locale(lang)
