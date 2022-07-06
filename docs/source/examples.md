# Examples

## Search first 10 results

```
from eudract import Eudract
eu = Eudract()

# return all trials with full details for "covid" in array of dict
eu.search("covid", "full", True, size=10) 

```

## Get trial info

Get info for a trial by eudract id.

```python
from eudract import Eudract

eu = Eudract()

# return trial summary in plain text format
eu.info("2015-001314-10", "summary", False) 

# return trial full in dict
eu.info("2015-001314-10", "full", True) 
```

## Use cache

Cache file can be used using `cache_file` argument.
Results will be cached to a sqlite database.

```python
eu.info("2015-001314-10", level="summary", to_dict=False, cache_file="euract.db")

```
