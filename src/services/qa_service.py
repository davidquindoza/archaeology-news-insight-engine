import requests
from google.cloud import bigquery

#Text to SQL Generation
def generate_sql(question: str) -> str:
    system_prompt = """You are an expert in converting English questions to SQL queries for an archaeology news database.
    IMPORTANT: You are only allowed to generate SELECT queries. Never generate DELETE, UPDATE, or INSERT queries.

    The database has an enriched_table with the following schema:
    - title (STRING): The title of the news article
    - source (STRING): The source/publisher of the article
    - publish_date (TIMESTAMP): When the article was published
    - url (STRING): Link to original article
    - full_content (STRING): The complete article text
    
    Return only the SQL query, nothing else."""

    response = requests.post('http:/ api ',
        json={
            "model": "llama2",
            "prompt": f"{system_prompt}\n\nQuestion: {question}\nSQL:",
            "stream": False
        })
    
    return response.json()['response'].strip()

#Execute SQL
def execute_sql(sql: str):
    client = bigquery.Client()
    query_job = client.query(sql)
    return list(query_job.result())

#Format Response
def format_response(question: str, results) -> str:
    # Convert results to a readable format
    articles = [f"Title: {row.title}\nSource: {row.source}\nContent: {row.full_content[:200]}..."
                for row in results]
    articles_text = "\n\n".join(articles)
    
    prompt = f"""Based on these archaeology articles, please answer the question: {question}

    Articles found:
    {articles_text}

    Provide a concise summary that directly answers the question and cites the sources."""

    response = requests.post('http:/ api ',
        json={
            "model": "llama2",
            "prompt": prompt,
            "stream": False
        })
    
    return response.json()['response'].strip()

# Main function to test
def answer_question(question: str):
    try:
        print("1. Generating SQL...")
        sql = generate_sql(question)
        print(f"Generated SQL: {sql}\n")

        print("2. Executing SQL...")
        results = execute_sql(sql)
        print(f"Found {len(results)} results\n")

        print("3. Formatting response...")
        answer = format_response(question, results)
        print(f"\nFinal Answer: {answer}")

    except Exception as e:
        print(f"Error: {str(e)}")

# Test it
if __name__ == "__main__":
    test_question = "What recent discoveries were made in Mexico?"
    answer_question(test_question)