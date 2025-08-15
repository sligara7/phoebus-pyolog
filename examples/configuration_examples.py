"""
Configuration Examples for Phoebus PyOlog Client

This file demonstrates various ways to configure the OlogClient
using environment variables, configuration files, and explicit parameters.
"""

import os
from pathlib import Path
from pyolog import OlogClient, load_config_from_env, load_config_from_file


def example_explicit_configuration():
    """Example: Configure client with explicit parameters."""
    print("=== Explicit Configuration ===")
    
    client = OlogClient(
        base_url="https://olog.example.com:8443",
        client_info="My Application v1.0",
        verify_ssl=True,
        timeout=60
    )
    
    # Set authentication
    client.set_auth("username", "password")
    
    print(f"Base URL: {client.base_url}")
    print(f"Client Info: {client.client_info}")
    print(f"SSL Verification: {client.verify_ssl}")
    print(f"Timeout: {client.timeout}")
    print()


def example_environment_configuration():
    """Example: Configure client using environment variables."""
    print("=== Environment Variable Configuration ===")
    
    # Set environment variables (in practice, these would be set externally)
    os.environ["OLOG_BASE_URL"] = "https://olog-env.example.com:8443"
    os.environ["OLOG_CLIENT_INFO"] = "Environment Client v2.0"
    os.environ["OLOG_VERIFY_SSL"] = "false"
    os.environ["OLOG_TIMEOUT"] = "90"
    
    # Create client that automatically loads from environment
    client = OlogClient()
    
    # Alternative: Use class method
    # client = OlogClient.from_env()
    
    print(f"Base URL: {client.base_url}")
    print(f"Client Info: {client.client_info}")
    print(f"SSL Verification: {client.verify_ssl}")
    print(f"Timeout: {client.timeout}")
    print()


def example_config_file():
    """Example: Configure client using a configuration file."""
    print("=== Configuration File Example ===")
    
    # Get the path to the example config file
    config_path = Path(__file__).parent / "olog_config.json"
    
    if config_path.exists():
        # Create client from config file
        client = OlogClient.from_config(config_path)
        
        print(f"Base URL: {client.base_url}")
        print(f"Client Info: {client.client_info}")
        print(f"SSL Verification: {client.verify_ssl}")
        print(f"Timeout: {client.timeout}")
    else:
        print(f"Config file not found: {config_path}")
    print()


def example_toml_config():
    """Example: Configure client using a TOML configuration file."""
    print("=== TOML Configuration File Example ===")
    
    # Get the path to the example TOML config file
    config_path = Path(__file__).parent / "olog_config.toml"
    
    if config_path.exists():
        try:
            # Create client from TOML config file
            client = OlogClient.from_config(config_path)
            
            print(f"Base URL: {client.base_url}")
            print(f"Client Info: {client.client_info}")
            print(f"SSL Verification: {client.verify_ssl}")
            print(f"Timeout: {client.timeout}")
        except ImportError as e:
            print(f"TOML support not available: {e}")
            print("Install with: pip install 'phoebus-pyolog[toml]'")
    else:
        print(f"Config file not found: {config_path}")
    print()


def example_mixed_configuration():
    """Example: Mix environment variables, config file, and explicit parameters."""
    print("=== Mixed Configuration Example ===")
    
    # Set some environment variables
    os.environ["OLOG_BASE_URL"] = "https://olog-mixed.example.com:8443"
    os.environ["OLOG_TIMEOUT"] = "45"
    
    config_path = Path(__file__).parent / "olog_config.json"
    
    if config_path.exists():
        # Configuration precedence:
        # 1. explicit parameters (highest)
        # 2. config file
        # 3. environment variables
        # 4. defaults (lowest)
        client = OlogClient(
            config_file=config_path,
            verify_ssl=False,  # Override config file setting
            auto_load_env=True  # Load base URL from environment
        )
        
        print(f"Base URL: {client.base_url} (from environment)")
        print(f"Client Info: {client.client_info} (from config file)")
        print(f"SSL Verification: {client.verify_ssl} (from explicit parameter)")
        print(f"Timeout: {client.timeout} (from config file)")
    else:
        print(f"Config file not found: {config_path}")
    print()


def example_manual_config_loading():
    """Example: Manually load and merge configurations."""
    print("=== Manual Configuration Loading ===")
    
    # Load configurations manually
    env_config = load_config_from_env()
    print(f"Environment config: {env_config}")
    
    config_path = Path(__file__).parent / "olog_config.json"
    if config_path.exists():
        file_config = load_config_from_file(config_path)
        print(f"File config: {file_config}")
        
        # Merge configurations (file overrides environment)
        merged_config = {**env_config, **file_config}
        print(f"Merged config: {merged_config}")
        
        # Create client with merged config
        client = OlogClient(**merged_config)
        print(f"Final Base URL: {client.base_url}")
    print()


def example_custom_prefix():
    """Example: Use custom environment variable prefix."""
    print("=== Custom Environment Prefix ===")
    
    # Set environment variables with custom prefix
    os.environ["MYAPP_BASE_URL"] = "https://myapp-olog.example.com:8443"
    os.environ["MYAPP_CLIENT_INFO"] = "MyApp Olog Client"
    
    # Load with custom prefix
    client = OlogClient.from_env(env_prefix="MYAPP_")
    
    print(f"Base URL: {client.base_url}")
    print(f"Client Info: {client.client_info}")
    print()


if __name__ == "__main__":
    print("Phoebus PyOlog Configuration Examples")
    print("=" * 40)
    print()
    
    example_explicit_configuration()
    example_environment_configuration()
    example_config_file()
    example_toml_config()
    example_mixed_configuration()
    example_manual_config_loading()
    example_custom_prefix()
    
    print("All examples completed!")
