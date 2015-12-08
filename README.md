# igenstrings

[![build-status-image]][travis]
[![pypi-version-image]][pypi]
[![docs-image]][docs]

> Eventually, all things merge into one, and a river runs through it.

Enhance the genstrings command by adding merging capabilities  
Documentation is available at [https://igenstrings.readthedocs.org][docs].

## Features

* Takes care of runing the genstrings command on all files \*.m
* Merge the results with previous version of the Localizable.string files you may have
* Inform you if it works correctly

## Known Issues

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

## Credits

Tools used in rendering this package:

*  [`Cookiecutter`][Cookiecutter]
*  [`cookiecutter-pypackage`][cookiecutter]

## Contact

[Pierre Dulac][github-dulaccc]  
[@dulaccc][twitter-dulaccc]

## License

`igenstrings` is available under the MIT license. See the [LICENSE](LICENSE) file for more info.


[build-status-image]: https://img.shields.io/travis/dulaccc/igenstrings.svg
[travis]: https://travis-ci.org/dulaccc/igenstrings
[pypi-version-image]: https://img.shields.io/pypi/v/igenstrings.svg
[pypi]: https://pypi.python.org/pypi/igenstrings
[docs-image]: https://readthedocs.org/projects/igenstrings/badge/?version=latest
[docs]: https://readthedocs.org/projects/igenstrings/?version=latest

[Cookiecutter]: https://github.com/audreyr/cookiecutter
[cookiecutter-pypackage]: https://github.com/audreyr/cookiecutter-pypackage
[github-dulaccc]: https://github.com/dulaccc
[twitter-dulaccc]: https://twitter.com/dulaccc
