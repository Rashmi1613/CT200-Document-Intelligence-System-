from fastapi import FastAPI
from app.api import browse
app = FastAPI(
    title="CT200 Document Intelligence System",
    version="1.0.0"
)
app.include_router(browse.router)
@app.get("/")
def root():
    return {
        "message": "CT200 Document Intelligence System is running"
    }