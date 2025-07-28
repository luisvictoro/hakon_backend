# FastAPI Application

A FastAPI application with user authentication and vulnerability management.

## Features

- User authentication with JWT tokens
- Vulnerability management system
- PostgreSQL database integration
- RESTful API endpoints

## Setup

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your database URL and other settings
```

3. Run the application:
```bash
uvicorn app.main:app --reload
```

### Database Setup

The application will automatically create database tables on startup. If you encounter database errors:

1. Test database connection:
```bash
python test_db.py
```

2. Check that your `DATABASE_URL` environment variable is set correctly.

## Deployment

### Heroku Deployment

1. Make sure you have the Heroku CLI installed
2. Create a new Heroku app:
```bash
heroku create your-app-name
```

3. Add PostgreSQL addon:
```bash
heroku addons:create heroku-postgresql:mini
```

4. Deploy:
```bash
git add .
git commit -m "Fix database initialization issues"
git push heroku main
```

5. Check logs:
```bash
heroku logs --tail
```

## API Endpoints

- `GET /` - Health check
- `GET /health` - Detailed health check
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/check-auth` - Check authentication status

## Troubleshooting

### Common Issues

1. **Database Connection Errors**: Ensure `DATABASE_URL` is set correctly
2. **Table Already Exists**: The app handles this automatically, but check logs for details
3. **Pydantic Warnings**: Fixed by updating `orm_mode` to `from_attributes` in schemas

### Recent Fixes

- Fixed database initialization to handle existing tables gracefully
- Updated Pydantic schemas to use V2 syntax (`from_attributes` instead of `orm_mode`)
- Added proper error handling and logging
- Specified package versions in requirements.txt for better compatibility

## Environment Variables

- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - JWT secret key
- `ALGORITHM` - JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration time
