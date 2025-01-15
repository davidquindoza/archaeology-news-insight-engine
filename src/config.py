import os
from typing import Dict, Any
from dotenv import load_dotenv

class Config:
    """Configuration management for the application"""
    
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()
        
        # Required environment variables
        self.required_vars = [
            'GOOGLE_APPLICATION_CREDENTIALS',
            'PROJECT_ID',
            'DATASET_ID',
            'ENRICHED_TABLE_ID',
            'NEWS_TABLE_ID',
            'LOCATIONS_TABLE_ID'
        ]
        
        # Load and validate configuration
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load and validate all configuration variables"""
        config = {}
        
        #Checker
        missing_vars = []
        for var in self.required_vars:
            value = os.getenv(var)
            if value is None:
                missing_vars.append(var)
            config[var.lower()] = value
            
        if missing_vars:
            raise EnvironmentError(
                f"Missing required environment variables: {', '.join(missing_vars)}"
            )
            
        return config
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key"""
        return self.config.get(key.lower(), default)
    
    @property
    def credentials_path(self) -> str:
        """Get Google Cloud credentials path"""
        return self.get('google_application_credentials')
    
    @property
    def project_id(self) -> str:
        """Get Google Cloud project ID"""
        return self.get('project_id')
    
    @property
    def dataset_id(self) -> str:
        """Get BigQuery dataset ID"""
        return self.get('dataset_id')
    
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

# Usage example:
if __name__ == "__main__":
    try:
        print("Loaded configuration:")
        print(f"Project ID: {config.project_id}")
        print(f"Dataset ID: {config.dataset_id}")
        print(f"Table paths:")
        for table_type, table_id in config.table_ids.items():
            print(f"  {table_type}: {config.get_full_table_path(table_type)}")
    except Exception as e:
        print(f"Error loading configuration: {str(e)}")