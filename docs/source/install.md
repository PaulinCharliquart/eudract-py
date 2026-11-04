# Install

## From PyPI

The stable release is available on [PyPI](https://pypi.org/project/eudract-py/):

```
pip install eudract-py
```

## Latest development version

To install the latest version from the repository:

```
git clone https://github.com/PaulinCharliquart/eudract-py.git
cd eudract-py
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -e .
```

## Optional dependencies

The project defines the following optional extras:

| Extra    | Description                                                        | Packages                                        |
| -------- | ------------------------------------------------------------------ | ----------------------------------------------- |
| `test`   | Run the test suite and linter                                      | `pytest`, `ruff`                                |
| `doc`    | Build the documentation                                            | `sphinx`, `furo`, `myst-parser`, `copybutton`   |
| `dev`    | Everything needed for development (`test` + `doc`)                 | `eudract-py[test]`, `eudract-py[doc]`            |

Install them with, for example:

```
pip install -e .[dev]
```
