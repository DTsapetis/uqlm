#!/usr/bin/env python3
"""
Script to create version.json file for gh-pages repository.
This script extracts version information from pyproject.toml and creates
a version.json file with version details for the documentation site.
"""

import json
import sys
import re
from pathlib import Path
from datetime import datetime


def extract_version_from_pyproject():
    """Extract version from pyproject.toml file."""
    pyproject_path = Path("pyproject.toml")
    
    if not pyproject_path.exists():
        raise FileNotFoundError("pyproject.toml not found in current directory")
    
    try:
        with open(pyproject_path, "r") as f:
            lines = f.readlines()
        
        # Look for version line (line 3)
        if len(lines) >= 3:
            version_line = lines[2].strip()  # Line 3 (0-indexed)
            # Extract version using regex
            match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', version_line)
            if match:
                return match.group(1)
        
        raise ValueError("Version not found in pyproject.toml line 3")
    except Exception as e:
        raise Exception(f"Error reading pyproject.toml: {e}")


def create_version_json(version, output_path="version.json", site_url="https://dtsapetis.github.io/uqlm"):
    """
    Create a version.json file with version information.
    
    Args:
        version (str): The version string (e.g., "0.1.8")
        output_path (str): Path where to save the version.json file
        site_url (str): Base URL for the documentation site
    """
    
    # Create version data structure
    version_data = {
        "version": version,
        "tag": f"v{version}",
        "release_date": datetime.now().isoformat(),
        "documentation_url": f"{site_url}/latest/",
        "version_url": f"{site_url}/v{version}/",
        "github_release_url": f"https://github.com/DTsapetis/uqlm/releases/tag/v{version}",
        "package_info": {
            "name": "uqlm",
            "description": "Uncertainty Quantification for Language Models",
            "python_version": ">=3.9,<3.13"
        }
    }
    
    # Write to file
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, "w") as f:
        json.dump(version_data, f, indent=2)
    
    print(f"Created {output_path} with version {version}")
    return version_data


def main():
    """Main function to run the script."""
    if len(sys.argv) > 1:
        version = sys.argv[1]
    else:
        try:
            version = extract_version_from_pyproject()
        except Exception as e:
            print(f"Error: {e}")
            print("Usage: python create_version_json.py [version] [output_path]")
            sys.exit(1)
    
    output_path = sys.argv[2] if len(sys.argv) > 2 else "version.json"
    
    try:
        version_data = create_version_json(version, output_path)
        print(f"Successfully created {output_path}")
        print(f"Version: {version_data['version']}")
        print(f"Tag: {version_data['tag']}")
    except Exception as e:
        print(f"Error creating version.json: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 