from fastapi import FastAPI

from app.api.routes import router
from fastapi import FastAPI

app = FastAPI(title="NetAssist")

@app.get("/")
def root():
    return {
        "application": "NetAssist",
        "company": "CAPSTONEFinal",
        "status": "Running",
        "docs": "/docs"
    }
