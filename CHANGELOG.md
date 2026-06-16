# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.3] - 2026-06-16

### Fixed
- List views no longer raise `NoReverseMatch` when CRUD actions are removed via
  `excluded_actions`. `CRUDSundaeView.get_context_data` reversed `<model>-create`
  (and `<model>-list`) unconditionally, and the `object_list` template tag
  reversed `<model>-bulk_update` unconditionally — so excluding `create` or
  `bulk_update` (e.g. for a list-only view) crashed the page. These reverses are
  now guarded and fall back to `None`, which the built-in templates already
  handle (`{% if create_view_url %}`).

### Changed
- Version metadata in `pyproject.toml`, `setup.py`, and `sundae/__init__.py` is
  now consistent (previously `setup.py`/`__init__.py` reported `0.1.0` while the
  published package was `0.0.2`).

[0.0.3]: https://github.com/leonh/django-crud-sundae/releases/tag/v0.0.3
