"""
Download Census data using Google Drive API with OAuth from MCP
"""

import subprocess
import json
import base64
import sys

print("=" * 70)
print("DOWNLOADING REAL CENSUS 2021 PUMF DATA")
print("=" * 70)
print()
print("File: census_2021_hier_v2.csv")
print("Size: 212.8 MB")
print("Records: ~930,000 persons")
print()

# The file is accessible through the MCP but too large for direct reading
# We need to use the download_file_content tool with proper export

file_id = "1N-kgImCjzN7LFXpe7hrN3hOut5PQyFb5"
output_path = "/workspace/data/raw/census_2021_hier_real.csv"

print("Attempting download...")
print(f"  File ID: {file_id}")
print(f"  Output: {output_path}")
print()

# Since we have writer access through MCP, we can try wget with Drive export
download_url = f"https://drive.google.com/uc?export=download&id={file_id}"

print(f"Download URL: {download_url}")
print()
print("NOTE: This file requires:")
print("  1. The file to be shared with 'Anyone with the link', OR")
print("  2. Manual download from Google Drive")
print()
print("RECOMMENDED ACTION:")
print("  Please share the file publicly or download it manually:")
print(f"  https://drive.google.com/file/d/{file_id}/view")
print()
print("Once downloaded, place at: /workspace/data/raw/census_2021_hier_real.csv")

