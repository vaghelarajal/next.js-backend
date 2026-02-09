from fastapi import FastAPI
from middleware import setup_cors_middleware
from routes import auth_router

app = FastAPI(title="Auth API", version="1.0.0")

# Setup middleware
setup_cors_middleware(app)

# Include routers
app.include_router(auth_router)


@app.get("/")
def root():
    return {"status": "ok", "message": "API running"}
