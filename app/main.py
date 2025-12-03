# app/main.py
from fastapi import FastAPI
from api.search import router as search_router

app = FastAPI(title="Meta Spyder Search Engine API")

# Include the search routes
app.include_router(search_router, tags=["Search"])

@app.get("/")
def read_root():
    return {"status": "Service Running", "message": "Navigate to /search?q={query}"}

