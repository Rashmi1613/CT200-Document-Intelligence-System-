from fastapi import FastAPI
from app.api import browser
from app.api import selection
from app.database import create_tables
create_tables()     
app = FastAPI(
    title="CT200 Document Intelligence System",
    version="1.0.0"
)
app.include_router(browser.router)
app.include_router(selection.router)
@app.get("/")
def root():
    return {
        "message": "CT200 Document Intelligence System is running"
    }