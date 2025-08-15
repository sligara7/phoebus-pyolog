"""
Simple Olog Client Usage Examples

This file demonstrates how to use the refactored SimpleOlogClient
for Bluesky integration and other data acquisition frameworks.
"""

import os
import sys
sys.path.insert(0, 'src')

from pyolog import SimpleOlogClient


def example_basic_usage():
    """Basic SimpleOlogClient usage example."""
    print("=== Basic SimpleOlogClient Usage ===")
    
    # Create a simple client (uses defaults or environment variables)
    client = SimpleOlogClient()
    
    print(f"Client base URL: {client.client.base_url}")
    print(f"Client verify SSL: {client.client.verify_ssl}")
    
    # Set authentication if needed
    # client.set_auth("username", "password")
    
    return client


def example_with_configuration():
    """Example using configuration parameters."""
    print("\n=== SimpleOlogClient with Configuration ===")
    
    # Create client with explicit configuration
    client = SimpleOlogClient(
        base_url="https://olog.example.com:8443",
        client_info="Bluesky Data Collection",
        verify_ssl=False,
        timeout=120
    )
    
    print(f"Configured base URL: {client.client.base_url}")
    print(f"Configured client info: {client.client.client_info}")
    
    return client


def example_property_access():
    """Example of accessing Olog properties."""
    print("\n=== Accessing Olog Properties ===")
    
    client = SimpleOlogClient()
    
    try:
        # Get available logbooks, tags, and properties
        logbooks = client.logbooks
        tags = client.tags
        properties = client.properties
        
        print(f"Available logbooks: {logbooks}")
        print(f"Available tags: {tags}")
        print(f"Available properties: {properties}")
        
    except Exception as e:
        print(f"Note: Could not fetch properties (server not available): {e}")


def example_log_creation():
    """Example of creating log entries."""
    print("\n=== Creating Log Entries ===")
    
    client = SimpleOlogClient()
    
    # Example 1: Simple log entry
    try:
        log_entry = client.log(
            text="Test log entry from SimpleOlogClient",
            logbooks=["General"],
            tags=["test", "bluesky"],
            verify=False  # Skip verification for demo
        )
        print("Created simple log entry")
        
    except Exception as e:
        print(f"Note: Could not create log entry (server not available): {e}")
    
    # Example 2: Log entry with properties
    try:
        log_with_props = client.log(
            text="Scan completed successfully",
            logbooks=["Beamline"],
            tags=["scan", "completed"],
            properties={
                "scan_info": {
                    "scan_id": "12345",
                    "duration": "30 minutes",
                    "operator": "scientist"
                }
            },
            verify=False
        )
        print("Created log entry with properties")
        
    except Exception as e:
        print(f"Note: Could not create log with properties: {e}")


def example_search():
    """Example of searching log entries."""
    print("\n=== Searching Log Entries ===")
    
    client = SimpleOlogClient()
    
    try:
        # Search for recent entries
        results = client.find(
            text="*test*",
            logbook="General"
        )
        print(f"Found {len(results)} log entries matching search")
        
        # Search by ID (if you know one)
        # result = client.find(id=12345)
        # print(f"Found log entry by ID: {result}")
        
    except Exception as e:
        print(f"Note: Could not search (server not available): {e}")


def example_bluesky_integration():
    """Example showing typical Bluesky integration pattern."""
    print("\n=== Bluesky Integration Pattern ===")
    
    # This is how you might integrate with Bluesky
    client = SimpleOlogClient(
        base_url=os.getenv("OLOG_BASE_URL", "http://localhost:8080"),
        verify_ssl=False,  # Often needed for development
        auto_load_env=True  # Load from environment variables
    )
    
    # Set authentication (would typically come from secure source)
    # client.set_auth(username, password)
    
    # Typical Bluesky scan logging
    def log_scan_start(scan_id, plan_name, detectors):
        """Log the start of a scan."""
        try:
            return client.log(
                text=f"Starting {plan_name} scan",
                logbooks=["BeamlineOps"],
                tags=["scan_start", plan_name],
                properties={
                    "scan_metadata": {
                        "scan_id": str(scan_id),
                        "plan_name": plan_name,
                        "detectors": ", ".join(detectors)
                    }
                },
                ensure=True  # Create logbooks/tags if they don't exist
            )
        except Exception as e:
            print(f"Could not log scan start: {e}")
            return None
    
    def log_scan_complete(scan_id, status, duration):
        """Log the completion of a scan."""
        try:
            return client.log(
                text=f"Scan {scan_id} completed with status: {status}",
                logbooks=["BeamlineOps"],
                tags=["scan_complete", status],
                properties={
                    "scan_results": {
                        "scan_id": str(scan_id),
                        "status": status,
                        "duration": str(duration)
                    }
                },
                ensure=True
            )
        except Exception as e:
            print(f"Could not log scan completion: {e}")
            return None
    
    # Example usage
    scan_id = 12345
    detectors = ["det1", "det2"]
    
    print("Simulating Bluesky scan logging...")
    log_start = log_scan_start(scan_id, "count", detectors)
    print("- Logged scan start")
    
    log_complete = log_scan_complete(scan_id, "success", "45 seconds")
    print("- Logged scan completion")


if __name__ == "__main__":
    print("SimpleOlogClient Examples")
    print("=" * 40)
    
    example_basic_usage()
    example_with_configuration()
    example_property_access()
    example_log_creation()
    example_search()
    example_bluesky_integration()
    
    print("\nAll examples completed!")
    print("\nNote: Many examples will show 'server not available' messages")
    print("when run without a live Olog server. This is expected for demo purposes.")
