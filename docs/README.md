# Phoebus PyOlog Documentation

## Overview

Phoebus PyOlog is a Python client library for the Phoebus Olog logbook service.

## Installation

```bash
pip install phoebus-pyolog
```

## Quick Start

```python
from pyolog import OlogClient

# Create client
client = OlogClient(base_url="http://localhost:8080")
client.set_auth('username', 'password')

# Get service info
info = client.get_service_info()
print(info)

# Create a log entry
log = client.create_log(
    title="Test Log Entry",
    logbooks=["operations"],
    description="This is a test log entry.",
)
print(f"Created log: {log['id']}")
```

## API Reference

See the source code documentation for detailed API reference.

## Testing

To run tests, you need a running Olog service and environment variables:

```bash
export OLOG_USERNAME=admin
export OLOG_PASSWORD=adminPass
pytest tests/ -v
```
