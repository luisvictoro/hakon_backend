#!/usr/bin/env python3
"""
Script to create a default admin user in the database
"""

import os
import sys
from dotenv import load_dotenv

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

load_dotenv()

from app.database import SessionLocal, init_db
from app.models.user import User
from app.services.auth import get_password_hash, get_user

def create_admin_user():
    """Create default admin user if it doesn't exist"""
    try:
        # Initialize database
        init_db()
        
        # Create database session
        db = SessionLocal()
        
        # Check if admin user already exists
        admin_user = get_user(db, "admin")
        
        if admin_user:
            print("Admin user already exists!")
            return
        
        # Create admin user
        hashed_password = get_password_hash("admin")
        admin_user = User(username="admin", hashed_password=hashed_password)
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print("Admin user created successfully!")
        print(f"Username: admin")
        print(f"Password: admin")
        
    except Exception as e:
        print(f"Error creating admin user: {e}")
        if 'db' in locals():
            db.rollback()
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    create_admin_user()