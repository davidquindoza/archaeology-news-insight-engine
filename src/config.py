import streamlit as st
from typing import Dict, Any
import json

class Config:
    """Configuration management for the application using Streamlit secrets"""
    
    def __init__(self):
        # Required configuration variables
        self.required_vars = [
            'PROJECT_ID',
            'DATASET_ID',
            'ENRICHED_TABLE_ID',
            'NEWS_TABLE_ID',
            'LOCATIONS_TABLE_ID',
            'CLOUD_FUNCTION_URL'
        ]
        
        # Load and validate configuration
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load and validate all configuration variables from Streamlit secrets"""
        config = {}
        
        # Check for missing variables
        missing_vars = []
        for var in self.required_vars:
            try:
                value = st.secrets[var]
                config[var.lower()] = value
            except KeyError:
                missing_vars.append(var)
            
        if missing_vars:
            raise KeyError(
                f"Missing required configuration in .streamlit/secrets.toml: {', '.join(missing_vars)}"
            )
        
        # Load GCP service account credentials
        if 'gcp_service_account' not in st.secrets:
            raise KeyError("Missing GCP service account configuration in secrets.toml")
        
        self.credentials = st.secrets.gcp_service_account
            
        return config
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key"""
        return self.config.get(key.lower(), default)
    
    @property
    def gcp_credentials(self) -> Dict[str, Any]:
        """Get Google Cloud credentials dictionary"""
        return self.credentials
    
    @property
    def project_id(self) -> str:
        """Get Google Cloud project ID"""
        return self.get('project_id')
    
    @property
    def dataset_id(self) -> str:
        """Get BigQuery dataset ID"""
        return self.get('dataset_id')
    
    @property
    def cloud_function_url(self) -> str:
        """Get Cloud Function URL"""
        return self.get('cloud_function_url')
    
    @property
    def table_ids(self) -> Dict[str, str]:
        """Get all table IDs"""
        return {
            'news': self.get('news_table_id'),
            'enriched': self.get('enriched_table_id'),
            'locations': self.get('locations_table_id')
        }
    
    def get_full_table_path(self, table_type: str) -> str:
        """Get fully qualified BigQuery table path"""
        table_id = self.table_ids.get(table_type)
        if not table_id:
            raise ValueError(f"Unknown table type: {table_type}")
        return f"{self.project_id}.{self.dataset_id}.{table_id}"

# Create a global config instance
config = Config()