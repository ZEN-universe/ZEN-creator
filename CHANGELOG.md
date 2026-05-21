# Changelog

This file gets automatically updated in ZEN-creator's continuous integration 
procedures. Do not edit the file manually.

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