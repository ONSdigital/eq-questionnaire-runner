# Linting Process

## Overview

Most of the linting is done by MegaLinter, it is a static analysis tool that runs multiple linters and formatters on different file types in the repository. It's designed to maintain code quality and consistency across the entire codebase by checking different file types with appropriate linters. Python linting is treated separately which will be explained in this doc.

- **Tool**: [MegaLinter](https://megalinter.io/)
- **Docker Image**: `ghcr.io/oxsecurity/megalinter:vX.X.X`
- **Repository**: <https://github.com/oxsecurity/megalinter>

### Primary Configuration File
- **File**: [.mega-linter.yml](.mega-linter.yml) (repository root)
- **Reference**: <https://megalinter.io/latest/config-file/>

## MegaLinter Summary

| Filetype        | Linter               | Config File        | Ignore Files                          |
|-----------------|----------------------|--------------------|---------------------------------------|
| JavaScript/JSON | ESLint v9            | `eslint.config.js` | `eslint.config.js`, `.prettierignore` |
| HTML            | djLint               | `pyproject.toml`   | `pyproject.toml`                      |
| JSON            | jsonlint             | `.mega-linter.yml` | (none)                                |
| Markdown        | markdownlint         | `.mega-linter.yml` | `.markdownlintignore`                 |
| YAML            | yamllint             | `.mega-linter.yml` | (none)                                |
| All Files       | editorconfig-checker | `.editorconfig`    | (none)                                |
| GitHub Actions  | Zizmor               | `.mega-linter.yml` | (none)                                |
| Dockerfile      | hadolint             | `.mega-linter.yml` | `.dockerignore`                       |

## Non MegaLinter Summary

Python linting is handled separately from MegaLinter, this is intentionally disabled in MegaLinter as recommended in the
[ONS Python template repo](https://github.com/ONSdigital/ons-python-template#3-megalinter).
To run Python linting: `make lint-python`

| Filetype | Linter                    | Config File                               | Ignore Files             |
|----------|---------------------------|-------------------------------------------|--------------------------|
| Python   | ruff, pylint, mypy, black | `pyproject.toml`, `.pylintrc`, `mypy.ini` | `.pylintrc`, `setup.cfg` |

## How to Run MegaLinter

### Prerequisites
- Docker installed and running

### Running locally

```bash
make megalint
```
- Runs all enabled linters
- Reports issues but does not modify files
- Output saved to `megalinter-reports/` directory

### Running locally with autofix enabled
```bash
make megalint-apply
```
Runs all enabled linters with `APPLY_FIXES=all` set which automatically fixes issues where possible

### Clean Up Reports
```bash
make clean-megalint
```
- Deletes the `megalinter-reports/` directory
- Use before re-running to get fresh results

## CI/CD (GitHub Actions)

MegaLinter runs automatically on every pull request to `main` via the GitHub Actions workflow:

**Workflow File**: [.github/workflows/mega-linter.yml](.github/workflows/mega-linter.yml)
