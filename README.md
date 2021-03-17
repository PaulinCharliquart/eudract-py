[![PyPI version](https://badge.fury.io/py/eudract-py.svg)](https://badge.fury.io/py/eudract-py)
[![GitHub license](https://img.shields.io/github/license/PaulinCharliquart/eudract-py)](https://github.com/PaulinCharliquart/eudract-py/blob/main/LICENSE)

# eudract-py

Eudract-py is a Python library for searching clinical trials on [EUDRACT](https://www.clinicaltrialsregister.eu/about.html).


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install eudract-py:

```pip install eudract-py```


## Usage


### Search for trials  

Search clinical trials and return summary or full protocol details.

```python
from eudract import Eudract

eu = Eudract()

eu.search("EFC14280", "summary") # return trial summary in plain text format

eu.search("EFC14280", "summary", True) # return trial summary in dict

eu.search("covid", "full", True) # return all trial full details with covid term in array of dict

```

### Trial info
Get info for a trial by eudract id.

```python
from eudract import Eudract

eu = Eudract()

eu.info("2015-001314-10", "summary", False) # return trial summary in plain text format

eu.info("2015-001314-10", "full", True) # return trial full in dict

```

## Issues

Report issue [here](https://github.com/PaulinCharliquart/eudract-py/issues).



## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.


## License
[MIT](https://choosealicense.com/licenses/mit/)