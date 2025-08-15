"""
A simple API to the Olog client in python - Bluesky integration wrapper

This module provides a simplified interface to the Phoebus Olog client
that is compatible with Bluesky and other data acquisition frameworks.
"""

import io
import os
import time
from typing import Any, Dict, List, Optional, Union
from .client import OlogClient


"""
A simple API to the Olog client in python - Bluesky integration wrapper

This module provides a simplified interface to the Phoebus Olog client
that is compatible with Bluesky and other data acquisition frameworks.
"""

import io
import os
import time
from typing import Any, Dict, List, Optional, Union
from .client import OlogClient


class SimpleOlogClient:
    """
    Simple client interface to Phoebus Olog

    This class provides a simplified interface to the Olog service
    for creating and searching log entries, designed for compatibility
    with Bluesky and other data acquisition frameworks.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize a session

        Initiate a session to communicate with the Olog server. The `args`
        and `kwargs` are passed to the `OlogClient` as initialization
        parameters.

        Parameters
        ----------
        *args : arguments
            Positional arguments passed to OlogClient
        **kwargs : keyword arguments
            Keyword arguments passed to OlogClient

        See Also
        --------
        OlogClient : Modern client interface to the Olog
        """
        self.client = OlogClient(*args, **kwargs)

    def set_auth(self, username: str, password: str):
        """Set authentication credentials."""
        self.client.set_auth(username, password)

    @property
    def tags(self) -> List[str]:
        """
        Return a list of tag names

        Returns a list of the tag names associated with the Olog instance.

        Returns
        -------
        list
            Tag names as strings
        """
        try:
            tag_list = self.client.get_tags()
            return [tag.get('name', '') for tag in tag_list if 'name' in tag]
        except Exception:
            return []

    @property
    def logbooks(self) -> List[str]:
        """
        Return logbook names

        Returns a list of logbook names associated with the Olog instance.

        Returns
        -------
        list
            Logbook names as strings
        """
        try:
            logbook_list = self.client.get_logbooks()
            return [lb.get('name', '') for lb in logbook_list if 'name' in lb]
        except Exception:
            return []

    @property
    def properties(self) -> Dict[str, List[str]]:
        """
        Return property names and their attributes

        Returns a dictionary of property names and their associated attributes.

        Returns
        -------
        dict
            Dictionary with keys as property names and values as
            lists of the property's attribute names
        """
        try:
            prop_list = self.client.get_properties()
            result = {}
            for prop in prop_list:
                if 'name' in prop:
                    attributes = []
                    if 'attributes' in prop:
                        attributes = [attr.get('name', '') for attr in prop['attributes']
                                    if isinstance(attr, dict) and 'name' in attr]
                    result[prop['name']] = attributes
            return result
        except Exception:
            return {}

    def create_logbook(self, logbook: str, owner: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a logbook

        Create a logbook in the current Olog instance.

        Parameters
        ----------
        logbook : str
            Name of logbook to create
        owner : str, optional
            Owner of logbook

        Returns
        -------
        dict
            The created logbook information
        """
        return self.client.create_logbook(logbook, owner=owner)

    def create_tag(self, tag: str, active: bool = True) -> Dict[str, Any]:
        """
        Create a tag

        Create a tag in the current Olog instance.

        Parameters
        ----------
        tag : str
            Name of tag to create
        active : bool, optional
            State of the tag (default: True)

        Returns
        -------
        dict
            The created tag information
        """
        state = "Active" if active else "Inactive"
        return self.client.create_tag(tag, state=state)

    def create_property(self, property_name: str, keys: List[str]) -> Dict[str, Any]:
        """
        Create a property

        Create a property in the current Olog instance.

        Parameters
        ----------
        property_name : str
            Name of property to create
        keys : list of str
            Attribute names for the property

        Returns
        -------
        dict
            The created property information
        """
        attributes = [{"name": key, "value": "", "state": "Active"} for key in keys]
        return self.client.create_property(property_name, attributes=attributes)

    def find(self, **kwargs) -> List[Dict[str, Any]]:
        """
        Find log entries

        Find (search) for log entries based on keyword arguments.

        Parameters
        ----------
        id : int
            Search for log entry with specific ID
        search : str
            Search log entry text for string  
        text : str
            Search log entry text (alias for search)
        tag : str
            Find log entries with matching tag
        logbook : str
            Find log entries in specified logbook
        property : str
            Find log entries with specified property
        start : float or str
            Find log entries created after this time
        stop : float or str  
            Find log entries created before this time
        from_date : str
            Start date in YYYY-MM-DD format
        to_date : str
            End date in YYYY-MM-DD format
        owner : str
            Find log entries by owner
        level : str
            Find log entries with specified level

        Returns
        -------
        list
            List of log entry dictionaries matching search criteria

        Examples
        --------
        Search for log entry with ID 100::

            >>> soc = SimpleOlogClient()
            >>> result = soc.find(id=100)

        Search for log entries containing "Timing" with tag "magnets"::

            >>> soc = SimpleOlogClient()
            >>> result = soc.find(text='*Timing*', tag='magnets')
        """
        # Handle parameter mapping for compatibility
        search_params = {}
        
        for key, value in kwargs.items():
            if key == 'search':
                search_params['text'] = value
            elif key == 'start':
                if isinstance(value, (int, float)):
                    # Convert timestamp to date string
                    import datetime
                    date_str = datetime.datetime.fromtimestamp(value).strftime('%Y-%m-%d')
                    search_params['from'] = date_str
                else:
                    search_params['from'] = value
            elif key == 'stop':
                if isinstance(value, (int, float)):
                    # Convert timestamp to date string  
                    import datetime
                    date_str = datetime.datetime.fromtimestamp(value).strftime('%Y-%m-%d')
                    search_params['to'] = date_str
                else:
                    search_params['to'] = value
            elif key == 'id':
                # For single ID lookup, use get_log instead
                try:
                    log_entry = self.client.get_log(str(value))
                    return [log_entry] if log_entry else []
                except Exception:
                    return []
            else:
                search_params[key] = value

        try:
            result = self.client.search_logs(**search_params)
            # Extract logs from the search result
            if isinstance(result, dict) and 'logs' in result:
                return result['logs']
            elif isinstance(result, list):
                return result
            else:
                return []
        except Exception:
            return []

    def log(self, text: Optional[str] = None, logbooks: Optional[Union[str, List[str]]] = None,
            tags: Optional[Union[str, List[str]]] = None, 
            properties: Optional[Dict[str, Dict[str, str]]] = None,
            attachments: Optional[List[Union[str, io.IOBase]]] = None,
            verify: bool = True, ensure: bool = False) -> Dict[str, Any]:
        """
        Create log entry

        Create a single log entry in the Olog instance.

        Parameters
        ----------
        text : str, optional
            The body of the log entry
        logbooks : str or list of str
            The logbooks to add the log entry to
        tags : str or list of str, optional
            The tags to add to the log entry
        properties : dict, optional
            The properties to add to the log entry.
            Format: {property_name: {attr_name: attr_value, ...}}
        attachments : list of str or file-like objects, optional
            File paths or file-like objects to attach
        verify : bool, optional
            Check that properties, tags and logbooks exist (default: True)
        ensure : bool, optional
            Create missing properties, tags or logbooks (default: False)

        Returns
        -------
        dict
            The created log entry information

        Raises
        ------
        ValueError
            If required logbooks are not provided or if verify=True and
            referenced items don't exist
        """
        if ensure:
            verify = False

        # Validate and convert parameters
        if not logbooks:
            raise ValueError("At least one logbook must be specified")
            
        if isinstance(logbooks, str):
            logbooks = [logbooks]
        if isinstance(tags, str):
            tags = [tags]

        # Verify/ensure logbooks exist
        if verify or ensure:
            existing_logbooks = self.logbooks
            for logbook in logbooks:
                if logbook not in existing_logbooks:
                    if ensure:
                        self.create_logbook(logbook)
                    elif verify:
                        raise ValueError(f"Logbook '{logbook}' does not exist")

        # Verify/ensure tags exist  
        if tags and (verify or ensure):
            existing_tags = self.tags
            for tag in tags:
                if tag not in existing_tags:
                    if ensure:
                        self.create_tag(tag)
                    elif verify:
                        raise ValueError(f"Tag '{tag}' does not exist")

        # Verify/ensure properties exist
        if properties and (verify or ensure):
            existing_properties = self.properties
            for prop_name, prop_attrs in properties.items():
                if prop_name not in existing_properties:
                    if ensure:
                        self.create_property(prop_name, list(prop_attrs.keys()))
                    elif verify:
                        raise ValueError(f"Property '{prop_name}' does not exist")

        # Convert properties to expected format
        formatted_properties = []
        if properties:
            for prop_name, attrs in properties.items():
                formatted_attrs = [{"name": k, "value": v} for k, v in attrs.items()]
                formatted_properties.append({
                    "name": prop_name,
                    "attributes": formatted_attrs
                })

        # Handle attachments
        file_paths = []
        if attachments:
            for attachment in attachments:
                if isinstance(attachment, str):
                    # File path
                    if os.path.exists(attachment):
                        file_paths.append(attachment)
                elif hasattr(attachment, 'read'):
                    # File-like object - save to temporary file
                    import tempfile
                    with tempfile.NamedTemporaryFile(delete=False) as tmp:
                        content = attachment.read()
                        if hasattr(content, 'encode'):
                            content = content.encode()
                        tmp.write(content)
                        file_paths.append(tmp.name)

        # Create the log entry
        if file_paths:
            return self.client.create_log_with_files(
                title=text or "",
                logbooks=logbooks,
                file_paths=file_paths,
                description=text or "",
                tags=tags,
                properties=formatted_properties
            )
        else:
            return self.client.create_log(
                title=text or "",
                logbooks=logbooks,
                description=text or "",
                tags=tags,
                properties=formatted_properties
            )

    def update(self, log_id: Union[int, str], text: Optional[str] = None,
               logbooks: Optional[Union[str, List[str]]] = None,
               tags: Optional[Union[str, List[str]]] = None,
               properties: Optional[Dict[str, Dict[str, str]]] = None,
               attachments: Optional[List[Union[str, io.IOBase]]] = None,
               verify: bool = True, ensure: bool = False) -> Dict[str, Any]:
        """
        Update an existing log entry

        This OVERWRITES the existing entry; it does not append.

        Parameters
        ----------
        log_id : int or str
            The ID of the log entry to update
        text : str, optional
            The new body of the log entry
        logbooks : str or list of str, optional
            The logbooks for the log entry
        tags : str or list of str, optional
            The tags for the log entry
        properties : dict, optional
            The properties for the log entry
        attachments : list, optional
            File paths or file-like objects to attach
        verify : bool, optional
            Check that properties, tags and logbooks exist
        ensure : bool, optional
            Create missing properties, tags or logbooks

        Returns
        -------
        dict
            The updated log entry information
        """
        # Convert types
        if isinstance(logbooks, str):
            logbooks = [logbooks]
        if isinstance(tags, str):
            tags = [tags]

        # Convert properties to expected format
        formatted_properties = []
        if properties:
            for prop_name, attrs in properties.items():
                formatted_attrs = [{"name": k, "value": v} for k, v in attrs.items()]
                formatted_properties.append({
                    "name": prop_name,
                    "attributes": formatted_attrs
                })

        return self.client.update_log(
            log_id=str(log_id),
            title=text,
            tags=tags,
            properties=formatted_properties
        )
