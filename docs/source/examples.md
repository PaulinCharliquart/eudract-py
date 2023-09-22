# Examples

## Search first 10 results

```
from eudract import Eudract
eu = Eudract()

# return all trials with full details for "covid" in list of dictionary
eu.search("covid", size=10) 

```

## Get trial info

Get info for a trial by eudract id.

```python
from eudract import Eudract

eu = Eudract()

# return trial summary in dict
eu.fetch_study("2015-001314-10") 
```

## Use cache

Cache file can be used using `cache_file` argument.
Results will be cached to a sqlite database.

```python
eu.fetch_study("2015-001314-10", cache_file="euract.db")

```
