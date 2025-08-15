"""
Phoebus Olog Python Client

A comprehensive Python client for interacting with the Phoebus Olog REST API.
Supports all CRUD operations for logs, logbooks, tags, properties, levels, and templates.
"""

import json
import mimetypes
import os
from pathlib import Path
from typing import Any, Optional, Union

import requests


def load_config_from_env(prefix: str = "OLOG_") -> dict[str, Any]:
    """
    Load configuration from environment variables.
    
    Args:
        prefix: Environment variable prefix (default: "OLOG_")
        
    Returns:
        Dictionary of configuration values
        
    Environment variables:
        OLOG_BASE_URL: Base URL of the Olog service
        OLOG_CLIENT_INFO: Client identification string
        OLOG_VERIFY_SSL: Whether to verify SSL certificates (true/false)
        OLOG_TIMEOUT: Request timeout in seconds
    """
    config = {}
    
    # Map environment variables to config keys
    env_mapping = {
        f"{prefix}BASE_URL": "base_url",
        f"{prefix}CLIENT_INFO": "client_info",
        f"{prefix}VERIFY_SSL": "verify_ssl",
        f"{prefix}TIMEOUT": "timeout"
    }
    
    for env_var, config_key in env_mapping.items():
        value = os.getenv(env_var)
        if value is not None:
            # Convert boolean and numeric values
            if config_key == "verify_ssl":
                config[config_key] = value.lower() in ("true", "1", "yes", "on")
            elif config_key == "timeout":
                try:
                    config[config_key] = int(value)
                except ValueError:
                    pass  # Keep as string, let validation handle it
            else:
                config[config_key] = value
                
    return config


def load_config_from_file(config_path: Union[str, Path]) -> dict[str, Any]:
    """
    Load configuration from a JSON or TOML file.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Dictionary of configuration values
        
    Example JSON config file:
    {
        "base_url": "https://olog.example.com:8443",
        "client_info": "My Application v1.0",
        "verify_ssl": true,
        "timeout": 60
    }
    """
    config_path = Path(config_path)
    
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            if config_path.suffix.lower() == '.json':
                return json.load(f)
            elif config_path.suffix.lower() in ('.toml', '.tml'):
                try:
                    import tomllib
                    with open(config_path, 'rb') as fb:
                        return tomllib.load(fb)
                except ImportError:
                    try:
                        import tomli
                        with open(config_path, 'rb') as fb:
                            return tomli.load(fb)
                    except ImportError:
                        raise ImportError(
                            "TOML support requires 'tomllib' (Python 3.11+) or 'tomli' package"
                        )
            else:
                # Assume JSON format for unknown extensions
                return json.load(f)
    except Exception as e:
        raise ValueError(f"Failed to parse configuration file {config_path}: {e}")


class OlogClient:
    """
    Python client for Phoebus Olog service.

    Provides methods to interact with all Olog API endpoints including:
    - Log entries (create, read, update, search)
    - Logbooks management
    - Tags management
    - Properties management
    - Levels management
    - Log templates
    - File attachments
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        client_info: Optional[str] = None,
        verify_ssl: Optional[bool] = None,
        timeout: Optional[int] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        config_file: Optional[Union[str, Path]] = None,
        env_prefix: str = "OLOG_",
        auto_load_env: bool = True,
    ):
        """
        Initialize the Olog client.

        Configuration is loaded in this order of precedence:
        1. Explicit parameters passed to __init__
        2. Configuration file (if config_file specified)
        3. Environment variables (if auto_load_env=True)
        4. Default values

        Args:
            base_url: Base URL of the Olog service
            client_info: Client identification string
            verify_ssl: Whether to verify SSL certificates
            timeout: Request timeout in seconds
            username: Username for authentication
            password: Password for authentication
            config_file: Path to configuration file (JSON or TOML)
            env_prefix: Environment variable prefix (default: "OLOG_")
            auto_load_env: Whether to automatically load from environment variables
        """
        # Start with default values
        config = {
            "base_url": "http://localhost:8080",
            "client_info": "Python Olog Client",
            "verify_ssl": False,
            "timeout": 30,
            "username": None,
            "password": None,
        }
        
        # Load from environment variables if enabled
        if auto_load_env:
            env_config = load_config_from_env(env_prefix)
            config.update(env_config)
        
        # Load from configuration file if specified
        if config_file:
            file_config = load_config_from_file(config_file)
            config.update(file_config)
        
        # Override with explicit parameters (highest precedence)
        explicit_params = {
            "base_url": base_url,
            "client_info": client_info,
            "verify_ssl": verify_ssl,
            "timeout": timeout,
            "username": username,
            "password": password,
        }
        
        for key, value in explicit_params.items():
            if value is not None:
                config[key] = value

        # Set instance attributes
        self.base_url = config["base_url"].rstrip("/")
        self.client_info = config["client_info"]
        self.verify_ssl = config["verify_ssl"]
        self.timeout = config["timeout"]
        self.session = requests.Session()

        # Set default headers
        self.session.headers.update(
            {"Content-Type": "application/json", "X-Olog-Client-Info": self.client_info}
        )
        
        # Set authentication if provided
        if config["username"] and config["password"]:
            self.session.auth = (config["username"], config["password"])
        else:
            self.session.auth = None

    @classmethod
    def from_config(
        cls,
        config_file: Union[str, Path],
        **kwargs
    ) -> 'OlogClient':
        """
        Create an OlogClient instance from a configuration file.
        
        Args:
            config_file: Path to configuration file (JSON or TOML)
            **kwargs: Additional parameters to override config file values
            
        Returns:
            Configured OlogClient instance
        """
        return cls(config_file=config_file, **kwargs)
    
    @classmethod
    def from_env(
        cls,
        env_prefix: str = "OLOG_",
        **kwargs
    ) -> 'OlogClient':
        """
        Create an OlogClient instance from environment variables.
        
        Args:
            env_prefix: Environment variable prefix (default: "OLOG_")
            **kwargs: Additional parameters to override environment values
            
        Returns:
            Configured OlogClient instance
        """
        return cls(env_prefix=env_prefix, auto_load_env=True, **kwargs)

    def set_auth(self, username: str, password: str):
        """Set Basic Auth credentials for the session."""
        self.session.auth = (username, password)

    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make HTTP request with error handling."""
        url = f"{self.base_url}{endpoint}"

        # Set default request parameters
        kwargs.setdefault("verify", self.verify_ssl)
        kwargs.setdefault("timeout", self.timeout)

        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            msg = f"Request failed ({type(e).__name__}): {e}"
            raise Exception(msg) from e

    def _get_json(self, endpoint: str, **kwargs) -> Any:
        """GET request returning JSON data."""
        response = self._make_request("GET", endpoint, **kwargs)
        return response.json() if response.content else None

    def _post_json(self, endpoint: str, data: Any = None, **kwargs) -> Any:
        """POST request with JSON data."""
        if data is not None:
            kwargs["json"] = data
        response = self._make_request("POST", endpoint, **kwargs)
        return response.json() if response.content else None

    def _put_json(self, endpoint: str, data: Any = None, **kwargs) -> Any:
        """PUT request with JSON data."""
        if data is not None:
            kwargs["json"] = data
        response = self._make_request("PUT", endpoint, **kwargs)
        return response.json() if response.content else None

    def _delete(self, endpoint: str, **kwargs) -> bool:
        """DELETE request."""
        response = self._make_request("DELETE", endpoint, **kwargs)
        return response.status_code == 200

    # Service Information
    def get_service_info(self) -> dict[str, Any]:
        """Get service information and health status."""
        return self._get_json("/Olog")

    def get_service_configuration(self) -> dict[str, Any]:
        """Get service configuration."""
        return self._get_json("/Olog/configuration")

    # Logbooks Management
    def get_logbooks(self) -> list[dict[str, Any]]:
        """Get all logbooks."""
        return self._get_json("/Olog/logbooks")

    def get_logbook(self, logbook_name: str) -> dict[str, Any]:
        """Get specific logbook by name."""
        return self._get_json(f"/Olog/logbooks/{logbook_name}")

    def create_logbook(
        self, name: str, owner: Optional[str] = None, state: str = "Active"
    ) -> dict[str, Any]:
        """
        Create a new logbook.

        Args:
            name: Logbook name
            owner: Owner of the logbook
            state: State (Active/Inactive)
        """
        logbook_data = {"name": name, "owner": owner, "state": state}
        return self._put_json(f"/Olog/logbooks/{name}", logbook_data)

    def update_logbooks(self, logbooks: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Update multiple logbooks."""
        return self._put_json("/Olog/logbooks", logbooks)

    def delete_logbook(self, logbook_name: str) -> bool:
        """Delete a logbook."""
        return self._delete(f"/Olog/logbooks/{logbook_name}")

    # Tags Management
    def get_tags(self) -> list[dict[str, Any]]:
        """Get all tags."""
        return self._get_json("/Olog/tags")

    def get_tag(self, tag_name: str) -> dict[str, Any]:
        """Get specific tag by name."""
        return self._get_json(f"/Olog/tags/{tag_name}")

    def create_tag(self, name: str, state: str = "Active") -> dict[str, Any]:
        """
        Create a new tag.

        Args:
            name: Tag name
            state: State (Active/Inactive)
        """
        tag_data = {"name": name, "state": state}
        return self._put_json(f"/Olog/tags/{name}", tag_data)

    def update_tags(self, tags: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Update multiple tags."""
        return self._put_json("/Olog/tags", tags)

    def delete_tag(self, tag_name: str) -> bool:
        """Delete a tag."""
        return self._delete(f"/Olog/tags/{tag_name}")

    # Properties Management
    def get_properties(self, inactive: bool = False) -> list[dict[str, Any]]:
        """
        Get all properties.

        Args:
            inactive: Include inactive properties
        """
        params = {"inactive": inactive} if inactive else {}
        return self._get_json("/Olog/properties", params=params)

    def get_property(self, property_name: str) -> dict[str, Any]:
        """Get specific property by name."""
        return self._get_json(f"/Olog/properties/{property_name}")

    def create_property(
        self,
        name: str,
        owner: Optional[str] = None,
        attributes: Optional[list[dict[str, str]]] = None,
        state: str = "Active",
    ) -> dict[str, Any]:
        """
        Create a new property.

        Args:
            name: Property name
            owner: Property owner
            attributes: List of attributes with name, value, state
            state: State (Active/Inactive)
        """
        property_data = {
            "name": name,
            "owner": owner,
            "state": state,
            "attributes": attributes or [],
        }
        return self._put_json(f"/Olog/properties/{name}", property_data)

    def update_properties(
        self, properties: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Update multiple properties."""
        return self._put_json("/Olog/properties", properties)

    def delete_property(self, property_name: str) -> bool:
        """Delete a property."""
        return self._delete(f"/Olog/properties/{property_name}")

    # Levels Management
    def get_levels(self) -> list[dict[str, Any]]:
        """Get all levels."""
        return self._get_json("/Olog/levels")

    def get_level(self, level_name: str) -> dict[str, Any]:
        """Get specific level by name."""
        return self._get_json(f"/Olog/levels/{level_name}")

    def create_level(self, name: str, default_level: bool = False) -> dict[str, Any]:
        """
        Create a new level.

        Args:
            name: Level name
            default_level: Whether this is the default level
        """
        level_data = {"name": name, "defaultLevel": default_level}
        return self._put_json(f"/Olog/levels/{name}", level_data)

    def create_levels(self, levels: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Create multiple levels."""
        return self._put_json("/Olog/levels", levels)

    def delete_level(self, level_name: str) -> bool:
        """Delete a level."""
        return self._delete(f"/Olog/levels/{level_name}")

    # Log Templates Management
    def get_templates(self) -> list[dict[str, Any]]:
        """Get all log templates."""
        return self._get_json("/Olog/templates")

    def get_template(self, template_id: str) -> dict[str, Any]:
        """Get specific template by ID."""
        return self._get_json(f"/Olog/templates/{template_id}")

    def create_template(
        self,
        name: str,
        title: str,
        logbooks: list[str],
        source: Optional[str] = None,
        level: Optional[str] = None,
        tags: Optional[list[str]] = None,
        properties: Optional[list[dict[str, Any]]] = None,
    ) -> dict[str, Any]:
        """
        Create a new log template.

        Args:
            name: Template name
            title: Template title
            logbooks: List of logbook names
            source: Template source
            level: Level name
            tags: List of tag names
            properties: List of properties
        """
        template_data = {
            "name": name,
            "title": title,
            "logbooks": [{"name": lb} for lb in logbooks],
            "source": source,
            "level": level,
            "tags": [{"name": tag} for tag in (tags or [])],
            "properties": properties or [],
        }
        return self._put_json("/Olog/templates", template_data)

    def delete_template(self, template_id: str) -> bool:
        """Delete a template."""
        return self._delete(f"/Olog/templates/{template_id}")

    # Log Entries Management
    def search_logs(self, **search_params) -> dict[str, Any]:
        """
        Search log entries with various parameters.

        Common search parameters:
            start: Start index for pagination
            size: Number of results to return
            from: Start date (YYYY-MM-DD)
            to: End date (YYYY-MM-DD)
            text: Text search
            logbook: Logbook name
            tag: Tag name
            owner: Owner name
            level: Level name
        """
        # Handle common parameter name variations
        if "from_date" in search_params:
            search_params["from"] = search_params.pop("from_date")
        if "to_date" in search_params:
            search_params["to"] = search_params.pop("to_date")

        return self._get_json("/Olog/logs/search", params=search_params)

    def get_log(self, log_id: str) -> dict[str, Any]:
        """Get specific log entry by ID."""
        return self._get_json(f"/Olog/logs/{log_id}")

    def get_archived_log(self, log_id: str) -> dict[str, Any]:
        """Get archived log entry by ID."""
        return self._get_json(f"/Olog/logs/archived/{log_id}")

    def create_log(
        self,
        title: str,
        logbooks: list[str],
        description: str = "",
        level: Optional[str] = None,
        tags: Optional[list[str]] = None,
        properties: Optional[list[dict[str, Any]]] = None,
        markup: Optional[str] = None,
        in_reply_to: str = "-1",
    ) -> dict[str, Any]:
        """
        Create a new log entry.

        Args:
            title: Log title (required)
            logbooks: List of logbook names (required)
            description: Log description
            level: Level name
            tags: List of tag names
            properties: List of properties
            markup: Markup type for description
            in_reply_to: ID of log this is replying to
        """
        log_data = {
            "title": title,
            "description": description,
            "logbooks": [{"name": lb} for lb in logbooks],
            "level": level,
            "tags": [{"name": tag} for tag in (tags or [])],
            "properties": properties or [],
        }

        params = {}
        if markup:
            params["markup"] = markup
        if in_reply_to != "-1":
            params["inReplyTo"] = in_reply_to

        return self._put_json("/Olog/logs", log_data, params=params)

    def create_log_with_files(
        self,
        title: str,
        logbooks: list[str],
        file_paths: list[str],
        description: str = "",
        level: Optional[str] = None,
        tags: Optional[list[str]] = None,
        properties: Optional[list[dict[str, Any]]] = None,
        markup: Optional[str] = None,
        in_reply_to: str = "-1",
    ) -> dict[str, Any]:
        """
        Create a new log entry with file attachments.

        Args:
            title: Log title (required)
            logbooks: List of logbook names (required)
            file_paths: List of file paths to attach
            description: Log description
            level: Level name
            tags: List of tag names
            properties: List of properties
            markup: Markup type for description
            in_reply_to: ID of log this is replying to
        """
        log_data = {
            "title": title,
            "description": description,
            "logbooks": [{"name": lb} for lb in logbooks],
            "level": level,
            "tags": [{"name": tag} for tag in (tags or [])],
            "properties": properties or [],
        }

        # Prepare multipart data with proper file handle management
        file_handles = []
        files = []
        
        try:
            for file_path in file_paths:
                if os.path.exists(file_path):
                    filename = os.path.basename(file_path)
                    mime_type = (
                        mimetypes.guess_type(file_path)[0] or "application/octet-stream"
                    )
                    file_handle = open(file_path, "rb")
                    file_handles.append(file_handle)
                    files.append(("files", (filename, file_handle, mime_type)))

            params = {}
            if markup:
                params["markup"] = markup
            if in_reply_to != "-1":
                params["inReplyTo"] = in_reply_to

            # For multipart, we need to handle the request differently
            multipart_data = {"logEntry": (None, json.dumps(log_data), "application/json")}
            multipart_data.update(dict(files))

            # Remove Content-Type header for multipart
            headers = dict(self.session.headers)
            headers.pop("Content-Type", None)

            response = self._make_request(
                "PUT",
                "/Olog/logs/multipart",
                files=multipart_data,
                params=params,
                headers=headers,
            )

            return response.json() if response.content else None
        
        finally:
            # Always close file handles, even if an exception occurs
            for file_handle in file_handles:
                file_handle.close()

    def update_log(
        self,
        log_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        level: Optional[str] = None,
        tags: Optional[list[str]] = None,
        properties: Optional[list[dict[str, Any]]] = None,
        markup: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Update an existing log entry.

        Args:
            log_id: ID of log to update
            title: New title
            description: New description
            level: New level
            tags: New tags list
            properties: New properties list
            markup: Markup type
        """
        # Get current log to preserve existing data
        current_log = self.get_log(log_id)

        # Update only provided fields
        if title is not None:
            current_log["title"] = title
        if description is not None:
            current_log["description"] = description
        if level is not None:
            current_log["level"] = level
        if tags is not None:
            current_log["tags"] = [{"name": tag} for tag in tags]
        if properties is not None:
            current_log["properties"] = properties

        params = {}
        if markup:
            params["markup"] = markup

        return self._post_json(f"/Olog/logs/{log_id}", current_log, params=params)

    def group_logs(self, log_ids: list[int]) -> bool:
        """Group multiple log entries together."""
        response = self._make_request("POST", "/Olog/logs/group", json=log_ids)
        return response.status_code == 200

    # Attachment Management
    def upload_attachment(
        self, log_id: str, file_path: str, description: str = ""
    ) -> dict[str, Any]:
        """
        Upload a single attachment to an existing log.

        Args:
            log_id: ID of the log entry
            file_path: Path to file to upload
            description: File description
        """
        if not os.path.exists(file_path):
            msg = f"File not found: {file_path}"
            raise FileNotFoundError(msg)

        filename = os.path.basename(file_path)

        # Use the create_log_with_files approach for existing logs by updating
        # First try simple multipart approach
        try:
            with open(file_path, "rb") as f:
                files = {"file": (filename, f, "application/octet-stream")}
                data = {"filename": filename, "fileMetadataDescription": description}

                # Remove Content-Type header for multipart
                headers = dict(self.session.headers)
                headers.pop("Content-Type", None)

                response = self._make_request(
                    "POST",
                    f"/Olog/logs/attachments/{log_id}",
                    files=files,
                    data=data,
                    headers=headers,
                )
                return response.json() if response.content else None
        except Exception:
            # If that fails, try alternative multipart format
            with open(file_path, "rb") as f:
                multipart_data = [
                    ("file", (filename, f, "application/octet-stream")),
                    ("filename", (None, filename)),
                    ("fileMetadataDescription", (None, description)),
                ]

                # Remove Content-Type header for multipart
                headers = dict(self.session.headers)
                if "Content-Type" in headers:
                    del headers["Content-Type"]

                response = self._make_request(
                    "POST",
                    f"/Olog/logs/attachments/{log_id}",
                    files=multipart_data,
                    headers=headers,
                )
                return response.json() if response.content else None

    def upload_multiple_attachments(
        self, log_id: str, file_paths: list[str]
    ) -> dict[str, Any]:
        """
        Upload multiple attachments to an existing log.

        Args:
            log_id: ID of the log entry
            file_paths: List of file paths to upload
        """
        files = []
        
        try:
            for file_path in file_paths:
                if os.path.exists(file_path):
                    filename = os.path.basename(file_path)
                    mime_type = (
                        mimetypes.guess_type(file_path)[0] or "application/octet-stream"
                    )
                    files.append(("file", (filename, open(file_path, "rb"), mime_type)))

            # Remove Content-Type header for multipart
            headers = dict(self.session.headers)
            headers.pop("Content-Type", None)

            response = self._make_request(
                "POST",
                f"/Olog/logs/attachments-multi/{log_id}",
                files=files,
                headers=headers,
            )

            return response.json() if response.content else None
        
        finally:
            # Close file handles
            for _, file_tuple in files:
                file_tuple[1].close()

    def download_attachment(
        self, log_id: str, attachment_name: str, save_path: Optional[str] = None
    ) -> bytes:
        """
        Download an attachment from a log entry.

        Args:
            log_id: ID of the log entry
            attachment_name: Name of the attachment
            save_path: Optional path to save the file
        """
        response = self._make_request(
            "GET", f"/Olog/logs/attachments/{log_id}/{attachment_name}"
        )

        if save_path:
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            with open(save_path, "wb") as f:
                f.write(response.content)

        return response.content

    def download_attachment_by_id(
        self, attachment_id: str, save_path: Optional[str] = None
    ) -> bytes:
        """
        Download an attachment by its ID.

        Args:
            attachment_id: ID of the attachment
            save_path: Optional path to save the file
        """
        response = self._make_request("GET", f"/Olog/attachment/{attachment_id}")

        if save_path:
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            with open(save_path, "wb") as f:
                f.write(response.content)

        return response.content

    # Help and Documentation
    def get_help(self, topic: str, language: str = "en") -> str:
        """
        Get help documentation for a specific topic.

        Args:
            topic: Help topic
            language: Language code (default: en)
        """
        params = {"lang": language} if language != "en" else {}
        response = self._make_request("GET", f"/Olog/help/{topic}", params=params)
        return response.text

    # Utility Methods
    def close(self):
        """Close the session."""
        self.session.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
