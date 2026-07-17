from fastapi import FastAPI

app = FastAPI(
    title="CT200 Document Intelligence System",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "CT200 Document Intelligence System is running"
    }