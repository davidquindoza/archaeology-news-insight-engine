# src/services/location_service.py

from google.cloud import bigquery
from typing import List, Dict, Any
from config import config

class LocationService:
    def __init__(self):
        self.client = bigquery.Client()
        
    def get_discovery_locations(self, limit: int = 15) -> List[Dict[str, Any]]:
        """
        Fetches unique archaeological discovery locations
        Uses ROW_NUMBER() to get one location per article
        """
        query = f"""
            WITH RankedLocations AS (
                SELECT 
                    l.location_name,
                    l.latitude,
                    l.longitude,
                    l.article_url,
                    ROW_NUMBER() OVER (PARTITION BY l.article_url ORDER BY l.extraction_date DESC) as rn
                FROM `{config.get_full_table_path('locations')}` l
                WHERE l.latitude IS NOT NULL AND l.longitude IS NOT NULL
            )
            SELECT DISTINCT
                rl.location_name,
                rl.latitude,
                rl.longitude,
                e.title,
                e.source,
                e.publish_date,
                e.url
            FROM RankedLocations rl
            JOIN `{config.get_full_table_path('enriched')}` e
            ON rl.article_url = e.url
            WHERE rl.rn = 1  -- Take only the first location per article
            ORDER BY e.publish_date DESC
            LIMIT @limit
        """
        
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("limit", "INTEGER", limit)
            ]
        )
        
        try:
            query_job = self.client.query(query, job_config=job_config)
            results = query_job.result()
            
            locations = []
            for row in results:
                locations.append({
                    'title': row.title,
                    'location': row.location_name,
                    'coordinates': [row.latitude, row.longitude],
                    'source': row.source,
                    'date': row.publish_date.strftime('%Y-%m-%d') if row.publish_date else None,
                    'url': row.url
                })
            
            return locations
            
        except Exception as e:
            print(f"Error fetching location data: {str(e)}")
            return []