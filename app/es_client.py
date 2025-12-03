# app/es_client.py
import os
from elasticsearch import Elasticsearch

# Use the service name defined in docker-compose.yml
# which resolves internally to the container's IP
ES_HOST = os.getenv("ES_HOST", "http://elasticsearch:9200")

def get_es_client():
    """Returns a configured Elasticsearch client instance."""
    try:
        # We disabled security in docker-compose, so no auth is needed for local dev
        client = Elasticsearch(
            hosts=[ES_HOST],
            timeout=30,
            max_retries=10,
            retry_on_timeout=True
        )
        # Check connection
        if client.ping():
            print(f"Connected to Elasticsearch at {ES_HOST}")
        else:
            print("Could not connect to Elasticsearch!")
        return client
    except Exception as e:
        print(f"Error connecting to Elasticsearch: {e}")
        return None

