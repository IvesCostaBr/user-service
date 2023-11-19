from dotenv import load_dotenv
from src.routes import user
import os, logging

load_dotenv()

from src.utils import *
from fastapi import FastAPI, Request, responses, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

app = FastAPI(
    title="Auth API",
    description="Api of authentication user",
    version="1.0.0",
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Custom-Header"],
)

app.include_router(user.router, prefix="/api/user")


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="API Auth",
        version="1.0.0",
        description=f"Tenant -> {os.environ.get('PROJECT')} API",
        routes=app.routes,
        servers=[
            {"url": "http://localhost:8000", "description": "Local environment"},
            {
                "url": "http://staging-api.uoleti.io",
                "description": "Staging environment",
            },
            {"url": "http://api.uoleti.io", "description": "Production environment"},
        ],
    )
    openapi_schema["components"]["securitySchemes"] = {
        "FirebaseAuth": {
            "type": "http",
            "scheme": "bearer",
            "name": "Authorization",
            "description": "Token de autenticação",
        },
        "ApiKeyAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-KEY",
            "description": "Chave de autenticação API personalizada",
        },
    }
    for route in openapi_schema["paths"]:
        for method in openapi_schema["paths"][route]:
            openapi_schema["paths"][route][method]["security"] = [{"FirebaseAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

@app.exception_handler(HTTPException)
async def exception_handler(request: Request, exc: HTTPException):
    """Exception generic handler."""
    return responses.JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

@app.get("/heath-check")
def heath_check():
    return {"status": "ok"}
