from google.cloud import bigquery
from typing import List, Dict, Any
from config import config

class NewsService:
    def __init__(self):
        self.client = bigquery.Client()
        
    def get_recent_news(self, limit: int = 9) -> List[Dict[str, Any]]:
        """
        Fetches recent news articles including full content
        """
        query = f"""
            SELECT 
                title,
                source,
                publish_date,
                url,
                full_content,
                SUBSTR(full_content, 1, 200) as summary
            FROM `{config.get_full_table_path('enriched')}`
            WHERE enrichment_status = 'success'
              AND full_content IS NOT NULL
            ORDER BY publish_date DESC
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
            
            news_items = []
            for row in results:
                news_items.append({
                    'title': row.title,
                    'source': row.source,
                    'date': row.publish_date.strftime('%Y-%m-%d') if row.publish_date else None,
                    'url': row.url,
                    'summary': row.summary + "..." if row.summary else None,
                    'full_content': row.full_content
                })
            
            return news_items
            
        except Exception as e:
            print(f"Error fetching news: {str(e)}")
            return []