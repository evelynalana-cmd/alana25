import bcrypt
from pathlib import Path
from app.data.db import connect_database
from app.data.users import get_user_by_username, insert_user
from app.data.schema import create_users_table

def register_user(username, password, role='user'):
    """Register new user with password hashing."""
    password_hash = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')
    
    insert_user(username, password_hash, role)
    return True, f"User '{username}' registered successfully."

def login_user(username, password):
    """Authenticate user."""
    user = get_user_by_username(username)
    if not user:
        return False, "User not found."
    
    stored_hash = user[2]
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
        return True, "Login successful!"
    return False, "Incorrect password."

def migrate_users_from_file(filepath='DATA/users.txt'):
    """Migrate users from text file to database."""
    filepath = Path(filepath)
    
    if not filepath.exists():
        return False, f"File not found: {filepath}"
    
    conn = connect_database()
    create_users_table(conn)
    cursor = conn.cursor()
    
    migrated_count = 0
    skipped_count = 0
    
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            parts = line.split(':')
            if len(parts) >= 3:
                username, password_hash, role = parts[0], parts[1], parts[2]
                
                cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
                if cursor.fetchone():
                    skipped_count += 1
                    continue
                
                cursor.execute(
                    "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                    (username, password_hash, role)
                )
                migrated_count += 1
    
    conn.commit()
    conn.close()
    
    return True, f"Migration complete: {migrated_count} users migrated, {skipped_count} skipped (already exist)"
