#!/usr/bin/env python3

import os
import json
import sys
sys.path.append('src')
from pyolog import OlogClient

def debug_template_creation():
    # Setup client
    username = os.getenv("OLOG_USERNAME")
    password = os.getenv("OLOG_PASSWORD")
    
    if not username or not password:
        print("Error: OLOG_USERNAME and OLOG_PASSWORD environment variables must be set")
        return
    
    client = OlogClient(base_url="http://localhost:8080", client_info="Debug Template Test")
    client.set_auth(username, password)
    
    # First, let's get existing templates to see the structure
    print("=== Existing Templates ===")
    try:
        templates = client.get_templates()
        for template in templates:
            print(f"Template: {json.dumps(template, indent=2)}")
            print("-" * 50)
    except Exception as e:
        print(f"Error getting templates: {e}")
    
    # Now try to create a minimal template
    print("\n=== Creating New Template ===")
    try:
        template_data = {
            "name": "debug-test-template",
            "title": "Debug Test Template",
            "logbooks": [{"name": "operations"}],
            "tags": [],
            "properties": []
        }
        print(f"Sending template data: {json.dumps(template_data, indent=2)}")
        
        # Try the creation
        result = client.create_template(
            name="debug-test-template",
            title="Debug Test Template", 
            logbooks=["operations"],
            tags=[],
            properties=[]
        )
        print(f"Success! Created template: {json.dumps(result, indent=2)}")
        
    except Exception as e:
        print(f"Error creating template: {e}")
        print(f"Error type: {type(e)}")

if __name__ == "__main__":
    debug_template_creation()
