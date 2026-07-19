from fastapi import FastAPI

from app.api.routes import router
from fastapi import FastAPI

app = FastAPI(title="NetAssist")

from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <head><title>NetAssist</title></head>
        <body style="font-family:Arial;padding:40px">
            <h1>🚀 NetAssist</h1>
            <h3>CAPSTONEFinal</h3>
            <p>Router Support Agent is running successfully.</p>

            <p><a href="/docs">Open API Documentation</a></p>
        </body>
    </html>
    """
