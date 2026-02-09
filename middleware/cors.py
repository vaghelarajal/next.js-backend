from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv()


def setup_cors_middleware(app: FastAPI) -> None:
    """Configure CORS middleware for the application"""
    frontend_urls = os.getenv("FRONTEND_URLS", "").split(",")
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=frontend_urls,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
