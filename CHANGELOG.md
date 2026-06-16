# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-06-16

Re-release of the 0.0.3 fix under a higher version number. `0.1.0` was already
published on PyPI and outranks `0.0.3` under PEP 440, so `0.0.3` could never be
the default install (`pip install django-crud-sundae` resolved to `0.1.0`,
which predates the fix). `0.2.0` supersedes `0.1.0` and ships the fix as the
latest release.

### Fixed
- List views no longer raise `NoReverseMatch` when CRUD actions are removed via
  `excluded_actions`. `CRUDSundaeView.get_context_data` reversed `<model>-create`
  (and `<model>-list`) unconditionally, and the `object_list` template tag
  reversed `<model>-bulk_update` unconditionally — so excluding `create` or
  `bulk_update` (e.g. for a list-only view) crashed the page. These reverses are
  now guarded and fall back to `None`, which the built-in templates already
  handle (`{% if create_view_url %}`).

## [0.0.3] - 2026-06-16

Superseded by 0.2.0 (see above) — published but not the latest version on PyPI.

### Fixed
- Same `NoReverseMatch` fix described under 0.2.0.

### Changed
- Version metadata in `pyproject.toml`, `setup.py`, and `sundae/__init__.py` is
  now consistent (previously `setup.py`/`__init__.py` reported `0.1.0` while the
  published package was `0.0.2`).

[0.2.0]: https://github.com/leonh/django-crud-sundae/releases/tag/v0.2.0
[0.0.3]: https://github.com/leonh/django-crud-sundae/releases/tag/v0.0.3
