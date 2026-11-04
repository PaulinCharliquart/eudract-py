# Changelog

## Unreleased

* Added: custom exceptions (``EudractError``, ``StudyNotFoundError``)

* Added: retries with backoff and configurable timeout on requests

* Added: ``test``, ``doc`` and ``dev`` optional dependencies

* Updated: package now uses a ``src/`` layout with a dynamic version

* Updated: replaced ``print`` with proper logging and added a User-Agent header

* Updated: full TLS certificate verification (removed ``verify=False``)

* Updated: ``fetch_all`` now uses the cache and skips missing studies

* Updated: documentation overhaul

## v1.3.0

* Added: new fonction to validate eudract number

* Fixed: return None when eudract number is not valid or not found

## v1.2.0

* Added:  cache, max results

* Updated: Results are returned as list of dictionary

## v1.1.0

* Updated: Full protocol search available

## v1.0.0

First version
