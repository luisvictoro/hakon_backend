from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import logging

load_dotenv()

logger = logging.getLogger(__name__)

# Handle database URL for Heroku
DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL") or os.getenv("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def create_default_admin():
    """Create default admin user if it doesn't exist"""
    try:
        from app.models.user import User
        from app.services.auth import get_password_hash, get_user
        
        db = SessionLocal()
        
        # Check if admin user already exists
        admin_user = get_user(db, "admin")
        
        if not admin_user:
            # Create admin user
            hashed_password = get_password_hash("admin")
            admin_user = User(username="admin", hashed_password=hashed_password)
            
            db.add(admin_user)
            db.commit()
            logger.info("Default admin user created successfully")
        else:
            logger.info("Admin user already exists")
            
    except Exception as e:
        logger.error(f"Error creating admin user: {e}")
        if 'db' in locals():
            db.rollback()
    finally:
        if 'db' in locals():
            db.close()

def init_db():
    """Initialize database tables safely"""
    try:
        # Check if tables already exist
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        
        if not existing_tables:
            # No tables exist, create them
            Base.metadata.create_all(bind=engine)
            logger.info("Database tables created successfully")
        else:
            logger.info(f"Database tables already exist: {existing_tables}")
        
        # Create default admin user
        create_default_admin()
            
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise
