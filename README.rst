===============================
igenstrings
===============================

.. image:: https://img.shields.io/pypi/v/igenstrings.svg
        :target: https://pypi.python.org/pypi/igenstrings

.. image:: https://img.shields.io/travis/dulaccc/igenstrings.svg
        :target: https://travis-ci.org/dulaccc/igenstrings

.. image:: https://readthedocs.org/projects/igenstrings/badge/?version=latest
        :target: https://readthedocs.org/projects/igenstrings/?badge=latest
        :alt: Documentation Status


Enhance the genstrings command by adding merging capabilities

* Free software: ISC license
* Documentation: https://igenstrings.readthedocs.org.

Features
--------

* Takes care of runing the genstrings command on all files *.m
* Merge the results with previous version of the Localizable.string files you may have
* Inform you if it works correctly

Known Issues
--------

* genstrings doesn't like path containing spaces, so avoid subfolders containing spaces.
Otherwise the Localizable.string will not be complete
* You need to respect the format used by the genstrings command unless it will breaks.
So, to avoid issues use strictly the format below for each translated text.
Also do not remove the line break between two fields or it will breaks too.

    ```ruby
    /* Comment for localizable string */
    "Your string" = "Translated string";

    /* Comment for localizable string */
    "Your string #2" = "Translated string #2";
    ```

Credits
---------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-pypackage`_

Contact
--------

`Pierre Dulac`_
`@dulaccc`_


.. _`Pierre Dulac`: http://github.com/dulaccc
.. _`@dulaccc`: https://twitter.com/dulaccc
