python
# app/api/search.py
from fastapi import APIRouter, Query
from es_client import get_es_client

router = APIRouter()
ES_INDEX = "web_pages" # Must match index defined in the crawler

@router.get("/search")
async def search_endpoint(q: str = Query(..., min_length=1, max_length=100)):
    es = get_es_client()
    if not es:
        return {"status": "error", "message": "Search service unavailable"}

    # Example Elasticsearch search query
    search_body = {
        "query": {
            "multi_match": {
                "query": q,
                "fields": ["title", "content", "url"]
            }
        },
        "size": 20
    }

    try:
        resp = es.search(index=ES_INDEX, body=search_body)
        results = []
        for hit in resp['hits']['hits']:
            results.append({
                "score": hit['_score'],
                "url": hit['_source']['url'],
                "title": hit['_source']['title'],
                "snippet": hit['_source']['content'][:200] + "..."
            })
        return {"query": q, "total_hits": resp['hits']['total']['value'], "results": results}

    except Exception as e:
        return {"status": "error", "message": f"Search failed: {e}"}
