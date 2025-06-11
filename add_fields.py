#!/usr/bin/env python3
"""
Script to add a 'status' field to each entry in the LLM_Friendly_App_Ideas.json file.
This script will read the JSON file, add the new field with a default value,
and save the updated JSON back to the file.
"""

import json
import os
from enum import Enum


class Status(Enum):
    """Enum for the status of an app idea."""
    IDEA = 'Idea'
    PLANNED = 'Planned'
    COMPLETED = 'Completed'


def add_status_field_to_json(filename="LLM_Friendly_App_Ideas.json"):
    """
    Add a 'status' field to each entry in the JSON file.
    
    Args:
        filename (str): Path to the JSON file to modify
    """
    
    # Check if file exists
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found!")
        return False
    
    try:
        # Read the JSON file
        print(f"Reading {filename}...")
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Verify it's a list
        if not isinstance(data, list):
            print("Error: JSON file should contain a list of objects")
            return False
        
        # Add the new field to each entry
        print(f"Adding 'status' field to {len(data)} entries...")
        entries_modified = 0
        
        for entry in data:
            if isinstance(entry, dict):
                # Only add field if it doesn't already exist
                if 'status' not in entry:
                    entry['status'] = Status.IDEA.value
                    entries_modified += 1
        
        if entries_modified == 0:
            print("No entries needed updating.")
            return True
            
        # Write the updated JSON back to the file
        print(f"Writing updated data back to {filename}...")
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
        
        print(f"✅ Successfully updated {entries_modified} entries!")
        print(f"Added 'status' field to all relevant entries in {filename}")
        return True
        
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format - {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Main function to run the script."""
    print("🚀 Starting JSON field addition process...")
    
    # You can modify the filename here if needed
    filename = "LLM_Friendly_App_Ideas.json"
    
    success = add_status_field_to_json(filename)
    
    if success:
        print("\n✨ Process completed successfully!")
    else:
        print("\n❌ Process failed. Please check the error messages above.")

if __name__ == "__main__":
    main() 