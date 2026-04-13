# Changelog

This file gets automatically updated in ZEN-creator's continuous integration 
procedures. Do not edit the file manually.

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