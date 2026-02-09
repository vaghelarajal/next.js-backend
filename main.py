from fastapi import FastAPI
from middleware import setup_cors_middleware
from routes import auth_router, products_router
from migrations.seed_data import run_migrations

app = FastAPI(title="Auth API", version="1.0.0")

# Setup middleware
setup_cors_middleware(app)

# Include routers
app.include_router(auth_router)
app.include_router(products_router)


@app.on_event("startup")
async def startup_event():
    """Run migrations when the app starts"""
    run_migrations()


@app.get("/")
def root():
    return {"status": "ok", "message": "API running"}
