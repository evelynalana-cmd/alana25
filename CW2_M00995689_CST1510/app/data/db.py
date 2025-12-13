import sqlite3
from pathlib import Path

# Define the database path
DB_PATH = Path("DATA") / "intelligence_platform.db"

def connect_database(db_path=DB_PATH):
    """
    Connect to the SQLite database.
    
    Args:
        db_path: Path to the database file (default: DATA/intelligence_platform.db)
    
    Returns:
        sqlite3.Connection: Database connection object
    """
    # Create DATA directory if it doesn't exist
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Connect to database (creates file if it doesn't exist)
    conn = sqlite3.connect(str(db_path))
    
    # Enable foreign key constraints
    conn.execute("PRAGMA foreign_keys = ON")
    
    return conn

def close_database(conn):
    """
    Close the database connection.
    
    Args:
        conn: Database connection object
    """
    if conn:
        conn.close()

def test_connection():
    """Test if database connection works."""
    try:
        conn = connect_database()
        print(f"✓ Database connection successful!")
        print(f"✓ Database location: {DB_PATH.resolve()}")
        close_database(conn)
        return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False

# Test connection when module is imported
if __name__ == "__main__":
    test_connection()