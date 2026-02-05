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

## Notes

- JWT tokens expire after 30 minutes
- Password reset tokens expire after 10 minutes
- Reset tokens can only be used once
- Email sending falls back gracefully if SMTP fails
- Database tables are created automatically on first run"# next.js-backend" 
