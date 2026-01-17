# app/main.py (Revised)

from fastapi import FastAPI, HTTPException
from .es_client import get_es_client, index_document, INDEX_NAME

app = FastAPI()

# Initialize the client globally when the app starts
es_client = get_es_client()

@app.get("/")
def read_root():
    """Basic health check and welcome message."""
    es_status = "Connected" if es_client and es_client.ping() else "Disconnected/Error"
    return {"Status": "Service Online", "Elasticsearch Connection": es_status}

@app.get("/search/{query}")
def search_index(query: str):
    """Endpoint to perform a simple search in Elasticsearch."""
    if not es_client:
        raise HTTPException(status_code=503, detail="Elasticsearch service unavailable")
    
    # ... (Search logic using es_client remains similar to previous example) ...
    search_body = { "query": { "match": { "content": query } } }
    
    try:
        response = es_client.search(index=INDEX_NAME, body=search_body)
        return response['hits']['hits']
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

# Example endpoint to demonstrate indexing data (you'd use your crawler for real data)
@app.post("/add_mock_data/")
def add_mock_data():
    if es_client:
        doc = {"content": "This is some mock data we just added.", "title": "Mock Title"}
        index_document(es_client, doc, doc_id="mock_id_1")
        return {"message": "Mock data indexed"}
    return {"message": "Failed to index mock data."}

