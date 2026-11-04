# Examples

## Search for trials

Search returns the full protocol details for every matching trial as a list of
dictionaries.

```python
from eudract import Eudract

eu = Eudract()

# return all trials matching "covid" as a list of dictionaries
trials = eu.search("covid")

# limit the number of results
trials = eu.search("covid", size=10)
```

The `query` argument is a plain text search; the underlying register also
supports its own
[query syntax](https://www.clinicaltrialsregister.eu/ctr-search/search?query=&query_field=1)
(e.g. `"covid AND asthma"`).

## Get a single trial

Get the details of a trial by its EudraCT number.

```python
from eudract import Eudract

eu = Eudract()

# return a dictionary with the trial summary
trial = eu.fetch_study("2015-001314-10")
```

An invalid or unknown EudraCT number returns `None`:

```python
trial = eu.fetch_study("not-a-number")   # -> None
```

## Fetch the whole register

Download every trial in the register. The results are fetched concurrently and
returned as a map (lazy iterator) of dictionaries.

```python
from eudract import Eudract

eu = Eudract()

trials = eu.fetch_all(max_worker=10)

for trial in trials:
    print(trial)
```

## Using the cache

Pass `cache_file` to store results in a local SQLite database and avoid
re-fetching the same trial from the network.

```python
from eudract import Eudract

eu = Eudract()

# the trial is downloaded and stored in euract.db
trial = eu.fetch_study("2015-001314-10", cache_file="euract.db")

# the next call reads from the local database instead of the network
trial = eu.fetch_study("2015-001314-10", cache_file="euract.db")

# search results are cached the same way
trials = eu.search("covid", size=5, cache_file="euract.db")
```

## Validating EudraCT numbers

The `validate_id` helper checks that a string looks like a valid EudraCT
number and belongs to the current century.

```python
from eudract.utils import validate_id

validate_id("2015-001314-10")  # -> True
validate_id("2000-000000-00")  # -> False (older than the supported range)
validate_id("garbage")         # -> False
```

## Structure of a trial

Each trial is returned as a dictionary whose keys are the sections of the
EudraCT protocol (e.g. `"A. PROTOCOL INFORMATION"`, `"B. SPONSOR INFORMATION"`,
`"E. GENERAL INFORMATION ON THE TRIAL"`, ...), each mapping to a dictionary of
the individual fields found in that section.
