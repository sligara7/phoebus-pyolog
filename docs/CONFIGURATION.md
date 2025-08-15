# Configuration Guide

The Phoebus PyOlog client supports multiple ways to configure connection settings, making it easy to adapt to different deployment scenarios.

## Configuration Methods

Configuration is loaded in the following order of precedence (highest to lowest):

1. **Explicit parameters** passed to the constructor
2. **Configuration file** (if specified)
3. **Environment variables** (if auto-loading is enabled)
4. **Default values**

## Constructor Parameters

```python
from pyolog import OlogClient

# Basic usage with explicit parameters
client = OlogClient(
    base_url="https://olog.example.com:8443",
    client_info="My Application v1.0",
    verify_ssl=True,
    timeout=60
)

# Set authentication
client.set_auth("username", "password")
```

## Environment Variables

Set environment variables with the `OLOG_` prefix:

```bash
export OLOG_BASE_URL="https://olog.example.com:8443"
export OLOG_CLIENT_INFO="My Application v1.0"
export OLOG_VERIFY_SSL="true"
export OLOG_TIMEOUT="60"
```

Then create a client that automatically loads from environment:

```python
from pyolog import OlogClient

# Automatically loads from OLOG_* environment variables
client = OlogClient()

# Or use the class method
client = OlogClient.from_env()

# Custom prefix
client = OlogClient.from_env(env_prefix="MY_APP_OLOG_")
```

### Supported Environment Variables

- `OLOG_BASE_URL`: Base URL of the Olog service
- `OLOG_CLIENT_INFO`: Client identification string
- `OLOG_VERIFY_SSL`: Whether to verify SSL certificates (true/false)
- `OLOG_TIMEOUT`: Request timeout in seconds

## Configuration Files

### JSON Configuration

Create a `olog_config.json` file:

```json
{
    "base_url": "https://olog.example.com:8443",
    "client_info": "My Application v1.0",
    "verify_ssl": true,
    "timeout": 60
}
```

### TOML Configuration

Create an `olog_config.toml` file:

```toml
base_url = "https://olog.example.com:8443"
client_info = "My Application v1.0"
verify_ssl = true
timeout = 60
```

### Using Configuration Files

```python
from pyolog import OlogClient

# Load from config file
client = OlogClient(config_file="olog_config.json")

# Or use the class method
client = OlogClient.from_config("olog_config.toml")

# Override config file values
client = OlogClient.from_config(
    "olog_config.json",
    verify_ssl=False  # Override the config file setting
)
```

## Authentication

**Important**: Credentials should be set programmatically using the `set_auth()` method for security reasons, not through environment variables or configuration files.

```python
from pyolog import OlogClient

# Configure connection settings via any method above
client = OlogClient(base_url="https://olog.example.com:8443")

# Set credentials programmatically
client.set_auth("your_username", "your_password")
```

## Advanced Configuration

### Combining Methods

You can combine multiple configuration methods:

```python
from pyolog import OlogClient

# Environment variables provide base config
# Config file overrides some settings
# Constructor parameters override specific values
client = OlogClient(
    config_file="production.json",
    timeout=120,  # Override timeout from config file
    auto_load_env=True  # Still load base URL from environment
)
```

### Disabling Environment Loading

```python
from pyolog import OlogClient

# Only use explicit parameters and config file
client = OlogClient(
    config_file="config.json",
    auto_load_env=False
)
```

### Custom Environment Prefix

```python
from pyolog import OlogClient

# Use custom environment variable prefix
# Looks for MYAPP_BASE_URL, MYAPP_VERIFY_SSL, etc.
client = OlogClient(env_prefix="MYAPP_")
```

## Configuration Loading Functions

You can also use the configuration loading functions directly:

```python
from pyolog import load_config_from_env, load_config_from_file

# Load configuration manually
env_config = load_config_from_env()
file_config = load_config_from_file("config.json")

# Merge configurations as needed
config = {**env_config, **file_config}

# Create client with merged config
client = OlogClient(**config)
```

## TOML Support

TOML configuration files require the `tomli` package for Python < 3.11:

```bash
pip install "phoebus-pyolog[toml]"
```

Python 3.11+ includes `tomllib` in the standard library, so no additional dependencies are needed.

## Best Practices

1. **Use environment variables** for deployment-specific settings (URLs, timeouts)
2. **Use configuration files** for application-specific defaults
3. **Set credentials programmatically** using `set_auth()` method
4. **Use explicit parameters** for runtime-specific overrides
5. **Test configuration** in development with different methods to ensure flexibility

## Examples

See the `examples/` directory for complete configuration examples:
- `examples/olog_config.json` - JSON configuration template
- `examples/olog_config.toml` - TOML configuration template  
- `examples/.env.example` - Environment variables template
- `examples/configuration_examples.py` - Usage examples
