import sqlite3
from pathlib import Path

# Database path
DB_PATH = Path("DATA") / "intelligence_platform.db"
USERS_FILE = Path("DATA") / "users.txt"

def migrate_users():
    """
    Read data from users.txt (Week 7) and insert into SQLite users table.
    
    File format: username,password_hash,role (one user per line)
    """
    
    # Check if users.txt exists
    if not USERS_FILE.exists():
        print(f"Error: {USERS_FILE} not found!")
        return
    
    # Connect to database
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    # Ensure users table exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    print(f"\nMigrating users from {USERS_FILE}...")
    print("-" * 50)
    
    migrated_count = 0
    error_count = 0
    
    # Read users.txt and insert into database
    with open(USERS_FILE, 'r') as file:
        for line_number, line in enumerate(file, 1):
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            try:
                # Parse line: username,password_hash,role (or username,password_hash)
                parts = line.split(',')
                
                if len(parts) == 2:
                    username, password_hash = parts
                    role = 'user'  # Default role
                elif len(parts) == 3:
                    username, password_hash, role = parts
                else:
                    raise ValueError(f"Invalid format on line {line_number}")
                
                # Insert into database (using parameterized query for security)
                cursor.execute("""
                    INSERT INTO users (username, password_hash, role)
                    VALUES (?, ?, ?)
                """, (username, password_hash, role))
                
                print(f"✓ Migrated: {username} (role: {role})")
                migrated_count += 1
                
            except sqlite3.IntegrityError:
                print(f"⚠ Skipped: {parts[0] if parts else 'unknown'} (already exists)")
                error_count += 1
            except Exception as e:
                print(f"✗ Error on line {line_number}: {e}")
                error_count += 1
    
    # Commit changes
    conn.commit()
    
    # Verify migration
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    
    print("-" * 50)
    print(f"\nMigration Summary:")
    print(f"  ✓ Users successfully migrated: {migrated_count}")
    print(f"  ⚠ Errors/Skipped: {error_count}")
    print(f"  📊 Total users in database: {total_users}")
    
    # Close connection
    conn.close()
    
    print("\nMigration complete!\n")

if __name__ == "__main__":
    migrate_users()