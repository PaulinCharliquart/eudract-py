[![PyPI version](https://badge.fury.io/py/eudract-py.svg)](https://badge.fury.io/py/eudract-py)
[![Python versions](https://img.shields.io/pypi/pyversions/eudract-py.svg)](https://pypi.org/project/eudract-py/)
[![License](https://img.shields.io/github/license/PaulinCharliquart/eudract-py)](https://github.com/PaulinCharliquart/eudract-py/blob/main/LICENSE)
[![Documentation](https://img.shields.io/badge/docs-here-blue)](https://paulincharliquart.github.io/eudract-py/)

# eudract-py

Eudract-py is a Python library for searching and retrieving clinical trials from the
[EU Clinical Trials Register (EudraCT)](https://www.clinicaltrialsregister.eu/about.html).

## Features

* Search clinical trials by keyword
* Fetch full trial protocol details by EudraCT number
* Fetch all trials (concurrently)
* Local SQLite caching to avoid repeated network requests
* EudraCT number validation

## Installation

```bash
pip install eudract-py
```

To install the latest development version:

```bash
git clone https://github.com/PaulinCharliquart/eudract-py.git
cd eudract-py
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -e .[dev]
```

## Usage

### Search for trials

Search clinical trials and return the full protocol details as a list of
dictionaries.

```python
from eudract import Eudract

eu = Eudract()

trials = eu.search("covid", size=10)
```

### Get trial info

Get the details of a single trial by its EudraCT number.

```python
from eudract import Eudract

eu = Eudract()

trial = eu.fetch_study("2015-001314-10")
```

## Documentation

Full documentation is available at
https://paulincharliquart.github.io/eudract-py/.

## Issues

Report issues [here](https://github.com/PaulinCharliquart/eudract-py/issues).

## Contributing

Pull requests are welcome. For major changes, please open an issue first to
discuss what you would like to change.

Please make sure to update tests as appropriate and run the linter:

```bash
ruff check src tests examples
ruff format --check src tests examples
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
