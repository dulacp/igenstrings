# igenstrings

[![build-status-image]][travis]
[![build-coverage-image]][codecov]
[![pypi-version-image]][pypi]
[![docs-image]][docs]

> Eventually, all things merge into one, and a river runs through it.

Enhance the genstrings command by adding merging capabilities  
Documentation is available at [https://igenstrings.readthedocs.org][docs].

## Features

* Takes care of runing the genstrings command on all files \*.m
* Merge the results with previous version of the Localizable.string files you may have
* Inform you if it works correctly

## Installation

```sh
$ pip install igenstrings
```

## Usage

```sh
$ igenstrings ./MyXcodeProjectDir
```

*output*

```sh
Running the script on path ./MyXcodeProjectDir
Excluded path regex: None
languages found : ['./MyXcodeProjectDir/en.lproj', './MyXcodeProjectDir/fr.lproj']
Job done for language: ./MyXcodeProjectDir/en.lproj
Job done for language: ./MyXcodeProjectDir/fr.lproj
```

## Hints

By default `git` won't display diff for `.string` files encoded in UTF-16. However, you can [turn on UTF-16 diffs](http://blog.xk72.com/post/31456986659/diff-strings-files-in-git) if you want to.

Create a `.gitattributes` file at your repository root

```ruby
*.strings diff=localizablestrings
```

Then edit your `~/.gitconfig` file add add the following :

```ruby
[diff "localizablestrings"]
textconv = "iconv -f utf-16 -t utf-8"
```

## Known Issues

* The Apple `genstrings` command doesn't like path that contains spaces.
  So avoid subfolders containing spaces, otherwise the Localizable.string will not be complete
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
[build-coverage-image]: https://img.shields.io/codecov/c/github/dulaccc/igenstrings.svg
[travis]: https://travis-ci.org/dulaccc/igenstrings
[codecov]: https://codecov.io/github/dulaccc/igenstrings?branch=master
[pypi-version-image]: https://img.shields.io/pypi/v/igenstrings.svg
[pypi]: https://pypi.python.org/pypi/igenstrings
[docs-image]: https://readthedocs.org/projects/igenstrings/badge/?version=latest
[docs]: http://igenstrings.readthedocs.org/en/latest/

[Cookiecutter]: https://github.com/audreyr/cookiecutter
[cookiecutter-pypackage]: https://github.com/audreyr/cookiecutter-pypackage
[github-dulaccc]: https://github.com/dulaccc
[twitter-dulaccc]: https://twitter.com/dulaccc
