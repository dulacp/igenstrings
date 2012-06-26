pygenstrings
============

Enhance the genstrings command by adding merging capabilities

Usage
---

    $ python genstring.py -p ../Relative/Path/To/Your/Project/Root

* It takes care of runing the genstrings command on all files *.m 
* Merge the results with previous version of the Localizable.string file
* Inform you if it works correctly

Known Issues
---
* You need to respect the format used by the genstrings command unless it breaks
So to avoid issues use strictly this format for each translated text.
Also do not remove the line break between two fields or it will breaks too.

So this format (used by the genstrings command), and everything should be fine

    /* Comment for localizable string */
    "Your string" = "Translated string";

    /* Comment for localizable string */
    "Your string #2" = "Translated string #2";

