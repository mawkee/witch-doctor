# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- CI/CD pipeline with GitHub Actions (lint, test, build, publish)
- `_reset()` method for test isolation
- Test fixtures with autouse for automatic state cleanup
- Concurrency tests (threading)
- Edge case tests (special container names, duplicate registration, invalid types)
- Performance benchmark tests with pytest-benchmark
- CHANGELOG.md with retroactive version history

### Fixed

- Typing: `List[any]` changed to `List[Any]`
- Test isolation: tests no longer share state

### Changed

- Test count increased from 14 to 48
- Test/code ratio improved from 1.18 to 3.81

## [1.2.1] - 2024

### Changed

- Updated documentation and docstrings for the `resolve` method

## [1.2.0] - 2024

### Added

- `resolve()` method to explicitly retrieve an instance of a registered interface
- Support for resolving from specific container by name

## [1.1.0] - 2024

### Changed

- Performance improvements for function signature inspection
- Cached function signatures to avoid repeated introspection

### Added

- Pre-commit hooks configuration

## [1.0.0] - 2024

### Added

- Named container support with `container()` method
- `load_container()` method to switch between container contexts
- `InjectionType` enum with `SINGLETON` and `FACTORY` options
- Support for constructor arguments via `args` parameter

### Changed

- Breaking: New registration API with injection types

## [0.1.2] - 2023

### Fixed

- Set `__wrapped__` attribute on decorated functions

## [0.1.1] - 2023

### Fixed

- Version number correction
- Respect original function signature in decorated functions

## [0.1.0] - 2023

### Added

- Initial release
- Basic dependency injection decorator `@WitchDoctor.injection`
- Interface registration with `register()` method
- ABC-based interface validation
- Type hint based dependency resolution
