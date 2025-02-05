import streamlit as st
from typing import Dict, Any

class Config:
    """Configuration management for the application using Streamlit secrets"""
    
    def __init__(self):
        # Verify required secrets exist
        self._verify_secrets()
    
    def _verify_secrets(self):
        """Verify all required secrets are present"""
        required_vars = [
            'PROJECT_ID',
            'DATASET_ID',
            'ENRICHED_TABLE_ID',
            'NEWS_TABLE_ID',
            'LOCATIONS_TABLE_ID',
            'CLOUD_FUNCTION_URL'
        ]
        
        missing = [var for var in required_vars if var not in st.secrets]
        if missing:
            raise KeyError(f"Missing required secrets: {', '.join(missing)}")
            
        if 'gcp_service_account' not in st.secrets:
            raise KeyError("Missing GCP service account configuration in secrets")
    
    @property
    def gcp_credentials(self) -> Dict[str, Any]:
        """Get Google Cloud credentials dictionary"""
        return dict(st.secrets["gcp_service_account"])
    
    @property
    def project_id(self) -> str:
        """Get Google Cloud project ID"""
        return st.secrets["PROJECT_ID"]
    
    @property
    def dataset_id(self) -> str:
        """Get BigQuery dataset ID"""
        return st.secrets["DATASET_ID"]
    
    @property
    def cloud_function_url(self) -> str:
        """Get Cloud Function URL"""
        return st.secrets["CLOUD_FUNCTION_URL"]
    
    @property
    def table_ids(self) -> Dict[str, str]:
        """Get all table IDs"""
        return {
            'news': st.secrets["NEWS_TABLE_ID"],
            'enriched': st.secrets["ENRICHED_TABLE_ID"],
            'locations': st.secrets["LOCATIONS_TABLE_ID"]
        }
    
    def get_full_table_path(self, table_type: str) -> str:
        """Get fully qualified BigQuery table path"""
        table_id = self.table_ids.get(table_type)
        if not table_id:
            raise ValueError(f"Unknown table type: {table_type}")
        return f"{self.project_id}.{self.dataset_id}.{table_id}"

# Create a global config instance
config = Config()