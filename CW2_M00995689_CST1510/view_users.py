import sqlite3

def show_users(db_path="DATA/intelligence_platform.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get column names
    cursor.execute("PRAGMA table_info(users)")
    columns = cursor.fetchall()
    print("🧾 Columns in 'users' table:")
    for col in columns:
        print(f"- {col[1]}")

    # Try selecting all rows
    try:
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        print("\n👥 Registered users:")
        for row in rows:
            print(row)
    except Exception as e:
        print(f"⚠️ Error reading users: {e}")

    conn.close()

if __name__ == "__main__":
    show_users()