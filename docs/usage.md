# Usage

To use igenstrings from the commandline :

```sh
$ igenstrings ./MyXcodeProjectDir
```

To use igenstrings from Python :

```python
from igenstrings.merger import Merger

# create the merger instance
project_dir = './MyXcodeProjectDir'
excluded_paths = []
merger = Merger(project_dir, excluded_paths)

# perform the merge
merger.merge_localized_strings()
```
