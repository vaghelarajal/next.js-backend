# FastAPI Authentication System

A complete authentication system built with FastAPI, featuring JWT tokens, password reset, email notifications, and user profile management.

## Features

- **User Registration & Login** with email validation
- **JWT Authentication** with Bearer tokens
- **Password Reset** via email with secure tokens
- **Profile Management** with protected endpoints
- **Email Notifications** with HTML templates
- **Token Security** - one-time use reset tokens
- **CORS Support** for frontend integration
- **PostgreSQL Database** with SQLAlchemy ORM
- **Input Validation** with Pydantic schemas

## Project Structure

```
app/
├── config/          # Database & settings configuration
├── middleware/      # CORS, auth, logging, rate limiting
├── models/          # Database models (SQLAlchemy)
├── routes/          # API endpoints
├── schemas/         # Pydantic validation models
├── services/        # Business logic (email, tokens)
└── utils/           # Security & utility functions
```

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables in `.env`:
```env
DATABASE_URL=postgresql://user:password@localhost/dbname
SECRET_KEY=your-secret-key
FRONTEND_URLS=http://localhost:3000
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
FRONTEND_RESET_URL=http://localhost:3000/reset-password
```

3. Run the application:
```bash
python start_server.py
```

## API Endpoints

- `POST /auth/signup` - Register new user
- `POST /auth/login` - Login and get JWT token
- `POST /auth/forgot-password` - Request password reset
- `POST /auth/reset-password` - Reset password with token
- `PUT /auth/profile` - Update user profile (protected)
- `GET /auth/me` - Get current user info (protected)

## Folder Details

- **config/** - Database connection and application settings
- **middleware/** - Request/response middleware (CORS, auth, logging, rate limiting)
- **models/** - Database models (User, UsedToken)
- **routes/** - API route handlers
- **schemas/** - Request/response validation
- **services/** - Business logic (email sending, token management)
- **utils/** - Security functions (password hashing, JWT tokens)

## Notes

- JWT tokens expire after 30 minutes
- Password reset tokens expire after 10 minutes
- Reset tokens can only be used once
- Email sending falls back gracefully if SMTP fails
- Database tables are created automatically on first run 
