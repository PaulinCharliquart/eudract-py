[![PyPI version](https://badge.fury.io/py/eudract-py.svg)](https://badge.fury.io/py/eudract-py)
[![GitHub license](https://img.shields.io/github/license/PaulinCharliquart/eudract-py)](https://github.com/PaulinCharliquart/eudract-py/blob/main/LICENSE)

# eudract-py

Eudract-py is a Python library for searching clinical trials on [EUDRACT](https://www.clinicaltrialsregister.eu/about.html).


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install eudract-py:

```pip install eudract-py```


To install latest development version:

```
git clone https://github.com/PaulinCharliquart/eudract-py.git
cd eudract-py
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip instal .[dev]
```


## Usage


### Search for trials  

Search clinical trials and return summary or full protocol details.

```python
from eudract import Eudract

eu = Eudract()

eu.search("EFC14280")

```

### Trial info
Get info for a trial by eudract id.

```python
from eudract import Eudract

eu = Eudract()

eu.fetch_study("2015-001314-10")

```

## Issues

Report issue [here](https://github.com/PaulinCharliquart/eudract-py/issues).



## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.


## License
[MIT](https://choosealicense.com/licenses/mit/)