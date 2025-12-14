import sqlite3
import bcrypt
from app.data.db import connect_database   # your db connection helper

def get_user_by_username(username):
    """Retrieve user by username."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, password_hash, role, created_at FROM users WHERE username = ?",
        (username,)
    )
    user = cursor.fetchone()
    conn.close()
    return user

def insert_user(username, password, role="user"):
    """Insert new user with hashed password."""
    conn = connect_database()
    cursor = conn.cursor()
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    cursor.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, hashed, role)
    )
    conn.commit()
    conn.close()

def get_all_users():
    """Retrieve all users."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password_hash, role, created_at FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

def update_user_password(username, new_password):
    """Update a user's password (hashed)."""
    conn = connect_database()
    cursor = conn.cursor()
    hashed = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
    cursor.execute(
        "UPDATE users SET password_hash = ? WHERE username = ?",
        (hashed, username)
    )
    conn.commit()
    conn.close()

def delete_user(username):
    """Delete a user by username."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    conn.close()