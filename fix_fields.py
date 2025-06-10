#!/usr/bin/env python3
"""
Script to fix and properly add 'desire' and 'retention' fields to each entry in the JSON file.
This script will read the JSON file, fix any formatting issues, and ensure the new fields
have empty string default values.
"""

import json
import os

def fix_and_add_fields(filename="LLM_Friendly_App_Ideas.json"):
    """
    Fix JSON formatting and ensure 'desire' and 'retention' fields are properly added.
    
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
        
        # Fix and add the new fields to each entry
        print(f"Fixing and adding 'desire' and 'retention' fields to {len(data)} entries...")
        entries_modified = 0
        
        for entry in data:
            if isinstance(entry, dict):
                # Fix any existing incorrect values and ensure proper string values
                entry['desire'] = ""
                entry['retention'] = ""
                entries_modified += 1
        
        # Write the updated JSON back to the file with proper formatting
        print(f"Writing corrected data back to {filename}...")
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
        
        print(f"✅ Successfully fixed and updated {entries_modified} entries!")
        print(f"All entries now have proper 'desire' and 'retention' fields with empty string values")
        return True
        
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format - {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Main function to run the script."""
    print("🔧 Starting JSON field correction process...")
    
    # You can modify the filename here if needed
    filename = "LLM_Friendly_App_Ideas.json"
    
    success = fix_and_add_fields(filename)
    
    if success:
        print("\n✨ Process completed successfully!")
        print("All entries now have properly formatted 'desire' and 'retention' fields.")
    else:
        print("\n❌ Process failed. Please check the error messages above.")

if __name__ == "__main__":
    main() 