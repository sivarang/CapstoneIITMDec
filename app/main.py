from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.api.routes import router

app = FastAPI(title="NetAssist")

# Register all API routes
app.include_router(router)

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
