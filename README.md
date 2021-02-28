# eudract-py

A simple python package to search for clinical trials in EUDRACT database.


## Installation

The easiet way to install *eudract-py* is to use pip:

```pip install eudract-py```


## Usage


### Search for trials  

Search clinical trials. Return list of EUDRACT id

```python
import eudract_py

search_trials("EFC14280")

search_trials() # return all EUDRACT id

```

### Get clinical trial info

Get clinical trial info as json or plain text.

```python
import eudract_py

full_summary("EFC14280", "text") # get plain text

full_summary("EFC14280", "json") # get json



