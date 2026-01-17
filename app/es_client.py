# app/es_client.py

import os
from elasticsearch import Elasticsearch

# --- Configuration ---
# Read host and port from environment variables set in the .env file or docker-compose.yaml
ES_HOST = os.getenv("ES_HOST", "elasticsearch")
ES_PORT = int(os.getenv("ES_PORT", 9200))
INDEX_NAME = os.getenv("ES_INDEX", "web_index")

def get_es_client() -> Elasticsearch:
    """
    Initializes and returns a connected Elasticsearch client instance.
    Uses service names and environment variables defined in Docker Compose.
    """
    try:
        # Connect using the service name 'elasticsearch' within the Docker network
        client = Elasticsearch(
            hosts=[{"host": ES_HOST, "port": ES_PORT}],
            # Security is disabled in the docker-compose.yaml for local development
            verify_certs=False 
        )
        
        if not client.ping():
            raise ConnectionError("Failed to ping Elasticsearch cluster.")
            
        print(f"Successfully connected to Elasticsearch at http://{ES_HOST}:{ES_PORT}")
        return client

    except Exception as e:
        print(f"CRITICAL ERROR connecting to Elasticsearch: {e}")
        # In a real app, you might want to exit the app if the connection fails
        # raise e 
        return None

def index_document(client: Elasticsearch, document: dict, doc_id: str = None):
    """
    Indexes a single document into the configured Elasticsearch index.
    """
    if client:
        response = client.index(
            index=INDEX_NAME,
            id=doc_id,
            document=document,
            refresh=True # Makes the document immediately searchable
        )
        print(f"Indexed document {response['_id']}")
        return response
    else:
        print("Client not available, cannot index document.")


# You can add other utility functions here:
# def create_index(client): ...
# def search_documents(client, query): ...
# def delete_document(client, doc_id): ...

