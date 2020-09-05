# pytemplate-reverse

A package to "reverse-enginner" simple strings based on a template.

Reverse-engineer a string based on a template, can be usefull to extract information from a generated string when you know how the information will be formated in said string, like the a file name. 

Usage sample:

``` python
from template_reverse import ReverseTemplate

segments = [
    "shrek3_0_600.avi",
    "shrek3_1_560.avi",
    "shrek3_2_780.avi"
]
rt = ReverseTemplate("{video_name}_{segment_id}_{segment_duration_in_secs}.avi")

total_duration = 0

for segment in segments:
    values = rt.reverse(segment)
    print("Checking out movie", values["video_name"], "part ", values["segment_id"])
    total_duration += int(values["segment_duration_in_secs"])

print("Total video duration so far", total_duration)
```

# Build locally

Requires Python 3.

This package is simple enough that it should work with any version. I recommend you to install python using [pyenv](https://github.com/pyenv/pyenv) with [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv). If you are on windows check [pyenv-win](https://github.com/pyenv-win/pyenv-win) out.

## Install 

``` bash
cd /path/to/pytemplate-reverse
pip install . # Thats it :)
```

If you want to develop on it and run tests use the following:

``` bash
pip install -r test-requirements.txt -e .
# `-r test-requirements.txt` Will install the dependencies required to run the tests
# `-e .` Install in editable mode, so you can edit the contents of /src/pytemplate_reverse without having to install the package again to see changes
pytest
```

To get coverage and lint run pytest with the following plugins:

``` 
pytest --black --cov=src
```
