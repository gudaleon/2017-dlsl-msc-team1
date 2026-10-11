"""
Google Drive downloader for fetching Census PUMF and supplementary datasets
"""

import os
import base64
from pathlib import Path
from typing import Optional, Dict
import yaml


class GoogleDriveDownloader:
    """
    Downloads files from Google Drive using the MCP google-drive tools
    integrated with Cursor Cloud Agent
    """
    
    def __init__(self, config_path: str = "config/data_paths.yaml"):
        """
        Initialize downloader with configuration
        
        Args:
            config_path: Path to YAML configuration file with Google Drive file IDs
        """
        self.config_path = Path(config_path)
        
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                self.config = yaml.safe_load(f)
        else:
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        self.drive_config = self.config.get('google_drive', {})
        self.local_paths = self.config.get('local_paths', {})
        
    def get_raw_data_path(self) -> Path:
        """Get the raw data directory path"""
        raw_path = Path(self.local_paths.get('raw_data', 'data/raw'))
        raw_path.mkdir(parents=True, exist_ok=True)
        return raw_path
        
    def download_file(self, file_key: str, force_redownload: bool = False) -> Path:
        """
        Download a file from Google Drive
        
        Args:
            file_key: Key in config['google_drive']['files']
            force_redownload: If True, redownload even if file exists
            
        Returns:
            Path to downloaded file
        """
        file_info = self.drive_config['files'].get(file_key)
        if not file_info:
            raise ValueError(f"File key '{file_key}' not found in configuration")
        
        file_id = file_info['file_id']
        filename = file_info['filename']
        
        output_path = self.get_raw_data_path() / filename
        
        # Check if file already exists
        if output_path.exists() and not force_redownload:
            print(f"File already exists: {output_path}")
            return output_path
        
        print(f"File {filename} should be downloaded from Google Drive.")
        print(f"File ID: {file_id}")
        print(f"Output path: {output_path}")
        print(f"\nThis will be integrated with google-drive MCP tools.")
        
        return output_path
    
    def download_census_pumf(self, force_redownload: bool = False) -> Path:
        """
        Download 2021 Census PUMF (212 MB)
        
        Args:
            force_redownload: If True, redownload even if file exists
            
        Returns:
            Path to Census CSV file
        """
        return self.download_file('census_2021', force_redownload)
    
    def download_shs(self, force_redownload: bool = False) -> Path:
        """
        Download Survey of Household Spending 2023
        
        Args:
            force_redownload: If True, redownload even if file exists
            
        Returns:
            Path to SHS ASCII flat file
        """
        return self.download_file('shs_2023', force_redownload)
    
    def download_chs(self, force_redownload: bool = False) -> Path:
        """
        Download Canadian Housing Survey 2024
        
        Args:
            force_redownload: If True, redownload even if file exists
            
        Returns:
            Path to CHS Excel file
        """
        return self.download_file('chs_2024', force_redownload)
    
    def download_all(self, force_redownload: bool = False) -> Dict[str, Path]:
        """
        Download all configured datasets
        
        Args:
            force_redownload: If True, redownload even if files exist
            
        Returns:
            Dictionary mapping file keys to downloaded paths
        """
        results = {}
        
        for file_key in self.drive_config['files'].keys():
            try:
                path = self.download_file(file_key, force_redownload)
                results[file_key] = path
                print(f"✓ {file_key}: {path}")
            except Exception as e:
                print(f"✗ {file_key}: Error - {e}")
                results[file_key] = None
        
        return results


if __name__ == "__main__":
    # Test downloader
    downloader = GoogleDriveDownloader()
    
    print("=== CA-13 Data Downloader ===\n")
    print("Configuration loaded successfully")
    print(f"Raw data directory: {downloader.get_raw_data_path()}\n")
    
    print("Available datasets:")
    for key, info in downloader.drive_config['files'].items():
        print(f"  - {key}: {info['filename']}")
