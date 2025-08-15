# Migration Guide

## Package Structure Migration

This project has been migrated from a simple script-based structure to a modern Python package using `pyproject.toml`.

### Before (Legacy):
```
python_client/
├── olog_client.py
├── requirements.txt
├── test_olog_endpoints.py
└── pytest.ini
```

### After (Modern):
```
src/pyolog/
├── __init__.py
├── client.py
tests/
├── __init__.py
├── test_client.py
pyproject.toml
noxfile.py
.pre-commit-config.yaml
```

## Installation Changes

### Before:
```bash
cd python_client
pip install -r requirements.txt
python test_olog_endpoints.py
```

### After:
```bash
# Install package
pip install phoebus-pyolog

# Or install from source with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/
```

## Import Changes

### Before:
```python
from olog_client import OlogClient
```

### After:
```python
from pyolog import OlogClient
```

## Development Workflow

### Before:
```bash
cd python_client
pip install -r requirements.txt
pytest test_olog_endpoints.py
```

### After:
```bash
# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest tests/

# Run linting
nox -s lint

# Run all tests across Python versions
nox -s tests

# Build package
nox -s build
```

## Dependencies

All dependencies are now managed in `pyproject.toml`:
- **Runtime**: `requests`, `charset-normalizer`, `chardet`
- **Testing**: `pytest`, `pytest-cov`, `pytest-mock`
- **Development**: `pre-commit`, `ruff`, `mypy`
- **Documentation**: `sphinx`, `sphinx-rtd-theme`, `myst-parser`
