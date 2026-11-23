# Changelog

This file gets automatically updated in ZEN-creator's continuous integration 
procedures. Do not edit the file manually.

## [v3.0.0] - 2026-11-23 

### New Features ✨
- Cite only the datasets of a dataset collection that were read while an attribute was built. `Element._build_attribute` opens a usage record for each attribute (new module `zen_creator/datasets/usage.py`), reading `self.data["<name>"]` or `self.data.get(...)` in a `DatasetCollection` records that dataset, and `SourceInformation.cited_metadata` reduces the cited metadata to the datasets in the record, so an attribute that read none shows only its description. A single `MetaData`, and a source created outside an attribute build, are still cited in full. [[🔀 PR #71](https://github.com/ZEN-universe/ZEN-creator/pull/71) @jacob-mannhardt]
- Add `DatasetCollection.mark_used(*names)` to record datasets that were selected by looping over `self.data`, which does not record them by itself. The name of a nested collection records all of its datasets. [[🔀 PR #71](https://github.com/ZEN-universe/ZEN-creator/pull/71) @jacob-mannhardt]
- Add `zen_creator.instance_cache`, which caches a method per instance and arguments and records the datasets read for the cached value again on every call. A `functools.cached_property` defined on a `DatasetCollection` is wrapped automatically to do the same. [[🔀 PR #71](https://github.com/ZEN-universe/ZEN-creator/pull/71) @jacob-mannhardt]
- List every citation of an element once in a "Citations" section at the top of `sources.md`, with attributes referring to them by author-year labels. The new `References` class shortens persons to their surname and organizations to their abbreviation or name, writes "et al." for more than two authors, and adds a/b suffixes when two different citations get the same label; `SourceInformation.to_str`, `AssumptionInformation.to_str` and `Attribute.sources_to_str` take an optional `references` argument and keep inline citations without it. [[🔀 PR #71](https://github.com/ZEN-universe/ZEN-creator/pull/71) @jacob-mannhardt]

### Bug Fixes 🐛
- Write `sources.md` with explicit UTF-8 encoding. Non-ASCII author names were written with the system code page on Windows. [[🔀 PR #71](https://github.com/ZEN-universe/ZEN-creator/pull/71) @jacob-mannhardt]

### Documentation Changes 📝
- Add the section "Only the datasets that were read" to `logic_and_structure.rst`. It explains how datasets are recorded and how to avoid missing citations: datasets loaded outside `_get_data()`, loops over `self.data`, and hand-made caches. [[🔀 PR #71](https://github.com/ZEN-universe/ZEN-creator/pull/71) @jacob-mannhardt]

### Maintenance Tasks 🧹
- Add unit tests for dataset usage tracking (`tests/unit/test_dataset_usage.py`) and for the reference list and author-year labels (`tests/unit/test_references.py`). [[🔀 PR #71](https://github.com/ZEN-universe/ZEN-creator/pull/71) @jacob-mannhardt]

### BREAKING CHANGES ⚠️
- Reject `functools.cache` and `functools.lru_cache` on methods of `DatasetCollection` subclasses with a `TypeError` when the class is defined. Their cached values would drop the datasets read from `sources.md`; use `zen_creator.instance_cache` instead. [[🔀 PR #71](https://github.com/ZEN-universe/ZEN-creator/pull/71) @jacob-mannhardt]

## [v2.1.0] - 2026-10-16 

### New Features ✨
- add `detailed_resutls` argument to the `compare_trees` function which determines whether value missmatches are reported for csv inputs in detailed row/column form. [[🔀 PR #69](https://github.com/ZEN-universe/ZEN-creator/pull/69) @csfunke]

### Bug Fixes 🐛
- fix print in the `compare_trees` function. The function previously used the logger, which means that outputs were not printed unless the logger setings were changed. [[🔀 PR #69](https://github.com/ZEN-universe/ZEN-creator/pull/69) @csfunke]

## [v2.0.0] - 2026-10-12 

### New Features ✨
- settings can be defined and accessed throughout the model [[🔀 PR #65](https://github.com/ZEN-universe/ZEN-creator/pull/65) @jacob-mannhardt]
- allow for nested metadata, a DatasetCollection can contain another DatasetCollection [[🔀 PR #65](https://github.com/ZEN-universe/ZEN-creator/pull/65) @jacob-mannhardt]
- auto-build attributes when required: when the attribute of an element that has not been constructed yet is required in another element, the attribute is auto-built to avoid returning stale data. [[🔀 PR #65](https://github.com/ZEN-universe/ZEN-creator/pull/65) @jacob-mannhardt]
- the structure of the model can be returned through ``model_structure`` [[🔀 PR #65](https://github.com/ZEN-universe/ZEN-creator/pull/65) @jacob-mannhardt]

### BREAKING CHANGES ⚠️
- the use of settings and config has changed [[🔀 PR #65](https://github.com/ZEN-universe/ZEN-creator/pull/65) @jacob-mannhardt]

## [v1.5.0] - 2026-06-17 

### New Features ✨
- add lower capacity limit parameter. [[🔀 PR #52](https://github.com/ZEN-universe/ZEN-creator/pull/52) @jojoethz]

### Maintenance Tasks 🧹
- update test solutions to account for new parameter. [[🔀 PR #52](https://github.com/ZEN-universe/ZEN-creator/pull/52) @jojoethz]
- upgrade `black` to patch security vulnerability. [[🔀 PR #55](https://github.com/ZEN-universe/ZEN-creator/pull/55) @csfunke]

## [v1.4.0] - 2026-06-15 

### New Features ✨
- write sources to sources.md along attribute.json files. [[🔀 PR #53](https://github.com/ZEN-universe/ZEN-creator/pull/53) @manud99]

## [v1.3.1] - 2026-06-13 

### Bug Fixes 🐛
- fix default config creation for custom element configs. Calling ``Config()`` now creates default values for all element-specific configurations. [[🔀 PR #50](https://github.com/ZEN-universe/ZEN-creator/pull/50) @csfunke]
- repair ``sources_to_str()`` for elements by updating function call name. [[🔀 PR #50](https://github.com/ZEN-universe/ZEN-creator/pull/50) @csfunke]

### Documentation Changes 📝
- document element-specific configurations by adding them to the template files. [[🔀 PR #50](https://github.com/ZEN-universe/ZEN-creator/pull/50) @csfunke]

## [v1.3.0] - 2026-06-11 

### New Features ✨
- allows custom configs for elements and datasets. [[🔀 PR #48](https://github.com/ZEN-universe/ZEN-creator/pull/48) @csfunke]

### Maintenance Tasks 🧹
- refactors default config by splitting it into multiple files. [[🔀 PR #48](https://github.com/ZEN-universe/ZEN-creator/pull/48) @csfunke]

## [v1.2.1] - 2026-05-21 

### Bug Fixes 🐛
- edit dataset config structure to allow more flexible dataset handling. [[🔀 PR #44](https://github.com/ZEN-universe/ZEN-creator/pull/44) @csfunke]

### Documentation Changes 📝
- add detailed README.md. [[🔀 PR #44](https://github.com/ZEN-universe/ZEN-creator/pull/44) @csfunke]
- refactor and update documentation to match the latest versions of ZEN-creator. [[🔀 PR #34](https://github.com/ZEN-universe/ZEN-creator/pull/34) @csfunke]

### Maintenance Tasks 🧹
- add end-to-end test for `model.from_config()`. The test demonstrates the usage of this constructor. [[🔀 PR #42](https://github.com/ZEN-universe/ZEN-creator/pull/42) @csfunke]
- move constants out of Attribute class. [[🔀 PR #39](https://github.com/ZEN-universe/ZEN-creator/pull/39) @manud99]

## [v1.2.0] - 2026-04-13 

### New Features ✨
- enable source tracking in attributes. Sources and data descriptions can now be cleanly printed to a markdown-like string for each element. [[🔀 PR #29](https://github.com/ZEN-universe/ZEN-creator/pull/29) @csfunke]

## [v1.1.1] - 2026-04-13 

### Bug Fixes 🐛
- fix tolerance in compare_csv function. [[🔀 PR #27](https://github.com/ZEN-universe/ZEN-creator/pull/27) @csfunke]
- remove model-specific sectors that belong to the ZEN-europe model. [[🔀 PR #27](https://github.com/ZEN-universe/ZEN-creator/pull/27) @csfunke]

## [v1.1.0] - 2026-04-13 

### New Features ✨
- add certain "user-oriented" objects and methods to the __init__.py file of ZEN-creator. These objects and methods can thus be imported directly from the ZEN-creator module with clean syntax. [[🔀 PR #25](https://github.com/ZEN-universe/ZEN-creator/pull/25) @csfunke]
- revise type hints of the public facing objects/methods and add a `py.typed` file. This ensures that MyPy views ZEN-creator as a typed module. [[🔀 PR #25](https://github.com/ZEN-universe/ZEN-creator/pull/25) @csfunke]

### Maintenance Tasks 🧹
- fix bugs in the automatic changelog updates. The previous version still had some relic references to ZEN-garden rather than ZEN-creator. [[🔀 PR #23](https://github.com/ZEN-universe/ZEN-creator/pull/23) @csfunke]

## [v1.0.0] - 2026-04-08 

### BREAKING CHANGES ⚠️
- Release first public version of ZEN-creator on Py-PI.