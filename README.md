# eudract-py

A simple python package to search for clinical trials in [EUDRACT](https://www.clinicaltrialsregister.eu/about.html).


## Installation

The easiet way to install *eudract-py* is to use pip:

```pip install eudract-py```


## Usage


### Search for trials  

Search clinical trials and return summary or full protocol details.

```python
from eudract import Eudract

eu = Eudract()

eu.search("EFC14280", "summary", "text") # return trial summary in plain text format

eu.search("EFC14280", "summary", "json") # return trial summary in json

eu.search("covid", "summary", "json") # return all trial summaries with covid term in json


eu.search() # return all EUDRACT protocols

```


## Issues

Report issue [here](https://github.com/PaulinCharliquart/eudract-py/issues).



## Contributing

Any contribution is welcome!
