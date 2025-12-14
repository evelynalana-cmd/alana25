import sqlite3

def add_password_column(db_path="DATA/intelligence_platform.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("ALTER TABLE users ADD COLUMN password TEXT")
    conn.commit()
    conn.close()
    print("✓ 'password' column added to users table.")

if __name__ == "__main__":
    add_password_column()