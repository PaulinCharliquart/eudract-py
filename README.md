# eudract-py

A simple python package to search for clinical trials in EUDRACT database.


## Installation

The easiet way to install *eudract-py* is to use pip:

```pip install eudract-py```


## Usage


### Search for trials  

Search clinical trials and return summary or full protocol details.

```python
from eudract import Eudract

eu = Eudract()

eu.search_trials("EFC14280")

search_trials() # return all EUDRACT protocols

```


## Issues

Report issue [here]([https://github.com/PaulinCharliquart/eudract-py/issues).




