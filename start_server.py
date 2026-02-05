#!/usr/bin/env python3
"""
Startup script for the FastAPI authentication server
"""

import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    """Start the FastAPI server"""
    print("🚀 Starting FastAPI Authentication Server...")
    print("📋 Server Configuration:")
    print(f"   - Host: localhost")
    print(f"   - Port: 8000")
    print(f"   - Reload: True (development mode)")
    print(f"   - Database: {os.getenv('DATABASE_URL', 'Not configured')}")
    print(f"   - Email: {os.getenv('EMAIL_ADDRESS', 'Not configured')}")
    print(f"   - Frontend URLs: {os.getenv('FRONTEND_URLS', 'Not configured')}")
    print("\n📡 Available Endpoints:")
    print("   - GET  /                    - Health check")
    print("   - POST /auth/signup         - User registration")
    print("   - POST /auth/login          - User login")
    print("   - POST /auth/forgot-password - Request password reset")
    print("   - POST /auth/reset-password - Reset password with token")
    print("   - GET  /auth/me             - Get current user (requires JWT)")
    print("   - PUT  /auth/profile        - Update profile (requires JWT)")
    print("\n🔧 API Documentation:")
    print("   - Swagger UI: http://localhost:8000/docs")
    print("   - ReDoc: http://localhost:8000/redoc")
    print("\n" + "="*60)
    
    # Start the server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()