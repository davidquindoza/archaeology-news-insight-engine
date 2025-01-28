import requests
from google.cloud import bigquery
from typing import List, Any
import time

#Text to SQL Generation
class ArchaeologyQA:
    def __init__(self, hf_api_token: str):
        self.api_url = "https://api-inference.huggingface.co/models/codellama/CodeLlama-34b-Instruct-hf"
        self.headers = {
            "Authorization": f"Bearer {hf_api_token}",
            "Content-Type": "application/json"
        }
        self.system_prompt = """You are an expert in BigQuery SQL. Convert questions to BigQuery SQL queries for an archaeology news database. The results will be used as context for an LLM to answer user questions.
IMPORTANT:
1. Always use standard BigQuery SQL syntax
2. Only generate SELECT queries - never DELETE, UPDATE, or INSERT
3. ALWAYS include title, source, publish_date, url, and full_content in your SELECT statement
4. Table name must be fully qualified: `project.dataset.fact_enriched_news`
5. Always use TIMESTAMP functions for date handling (e.g., TIMESTAMP_SUB, TIMESTAMP_ADD)
6. For text searches, use REGEXP_CONTAINS for pattern matching
7. For relevancy ranking, use ranking criteria in ORDER BY

Schema for fact_enriched_news:
- title (STRING): News article title
- source (STRING): Publisher name
- publish_date (TIMESTAMP): Publication timestamp
- url (STRING): Article URL
- full_content (STRING): Complete article text (REQUIRED for LLM context)

Common patterns:
- Base SELECT: SELECT title, source, publish_date, url, full_content FROM...
- Recent articles: WHERE publish_date >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
- Text search: WHERE REGEXP_CONTAINS(LOWER(title || full_content), r'(?i)search_term')
- Relevancy: ORDER BY publish_date DESC, 
- Limit results: LIMIT 10

Return only the SQL query, no explanations or comments."""

    def _make_api_call(self, prompt: str, max_retries: int = 3) -> str:
        """Make an API call to Hugging Face with retry logic"""
        headers = self.headers.copy()
        headers["x-wait-for-model"] = "true"  # Wait for model if it's cold

        for attempt in range(max_retries):
            try:
                response = requests.post(
                    self.api_url,
                    headers=headers,
                    json={
                        "inputs": f"[INST] <<SYS>>{self.system_prompt}<</SYS>>\n\n{prompt}[/INST]"
                    }
                )
                
                if response.status_code == 200:
                    # Extract the generated text from the response
                    result = response.json()
                    if isinstance(result, list) and len(result) > 0:
                        return result[0].get('generated_text', '').strip()
                    return ''
                
                elif response.status_code == 503:  # Model is loading
                    if attempt < max_retries - 1:
                        time.sleep(20)  # Wait before retry
                        continue
                    
                response.raise_for_status()
                
            except Exception as e:
                if attempt == max_retries - 1:
                    raise Exception(f"API call failed after {max_retries} attempts: {str(e)}")
                time.sleep(5)
                
        return ""

    def generate_sql(self, question: str) -> str:
        """Generate SQL query from natural language question"""
        prompt = f"Question: {question}\nSQL:"
        response = self._make_api_call(prompt)
        
        # Extract SQL query from response if needed
        sql_start = response.find('```sql')
        if sql_start != -1:
            sql_end = response.find('```', sql_start + 6)
            if sql_end != -1:
                return response[sql_start + 6:sql_end].strip()
        
        return response.strip()

    def execute_sql(self, sql: str) -> List[Any]:
        """Execute SQL query using BigQuery"""
        client = bigquery.Client()
        query_job = client.query(sql)
        return list(query_job.result())

    def format_response(self, question: str, results: List[Any]) -> str:
        """Format the final response using the LLM"""
        # Convert results to a readable format
        articles = [
            f"Title: {row.title}\nSource: {row.source}\nContent: {row.full_content[:200]}..."
            for row in results
        ]
        articles_text = "\n\n".join(articles)
        
        prompt = f"""Based on these archaeology articles, please answer the question: {question}

        Articles found:
        {articles_text}

        Provide a concise summary that directly answers the question and cites the sources."""
        
        return self._make_api_call(prompt)

    def answer_question(self, question: str) -> dict:
        """Main function to process a question and return an answer"""
        try:
            print("1. Generating SQL...")
            sql = self.generate_sql(question)
            print(f"Generated SQL: {sql}\n")

            print("2. Executing SQL...")
            results = self.execute_sql(sql)
            print(f"Found {len(results)} results\n")

            print("3. Formatting response...")
            answer = self.format_response(question, results)
            
            return {
                "success": True,
                "sql": sql,
                "results_count": len(results),
                "answer": answer
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

# Usage example
if __name__ == "__main__":
    # Initialize the service with your Hugging Face API token
    qa_service = ArchaeologyQA(hf_api_token="your_hf_token_here")
    
    # Test question
    test_question = "What recent discoveries were made in Mexico?"
    result = qa_service.answer_question(test_question)
    
    if result["success"]:
        print("\nFinal Answer:", result["answer"])
    else:
        print("\nError:", result["error"])