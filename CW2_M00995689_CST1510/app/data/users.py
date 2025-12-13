import sqlite3
from app.data.db import connect_database, close_database

def insert_user(username, password_hash, role='user'):
    """
    Insert a new user into the database.
    """
    conn = connect_database()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (username, password_hash, role)
            VALUES (?, ?, ?)
        """, (username, password_hash, role))
        conn.commit()
        user_id = cursor.lastrowid
        print(f"✓ User '{username}' inserted with ID: {user_id}")
        return user_id
    except sqlite3.IntegrityError:
        print(f"✗ Error: Username '{username}' already exists")
        return None
    finally:
        close_database(conn)

def get_user_by_username(username):
    """
    Retrieve a user by username.
    """
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, username, password_hash, role, created_at
        FROM users
        WHERE username = ?
    """, (username,))
    user = cursor.fetchone()
    close_database(conn)
    return user

def get_user_by_id(user_id):
    """
    Retrieve a user by ID.
    """
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, username, password_hash, role, created_at
        FROM users
        WHERE id = ?
    """, (user_id,))
    user = cursor.fetchone()
    close_database(conn)
    return user

def get_all_users():
    """
    Retrieve all users ordered by most recent creation.
    """
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, username, role, created_at
        FROM users
        ORDER BY created_at DESC
    """)
    users = cursor.fetchall()
    close_database(conn)
    return users

def update_user_role(username, new_role):
    """
    Update a user's role.
    """
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users
        SET role = ?
        WHERE username = ?
    """, (new_role, username))
    conn.commit()
    ok = cursor.rowcount > 0
    close_database(conn)
    print(f"{'✓' if ok else '✗'} User '{username}' role updated to '{new_role}'")
    return ok

def update_user_password(username, new_password_hash):
    """
    Update a user's password hash.
    """
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users
        SET password_hash = ?
        WHERE username = ?
    """, (new_password_hash, username))
    conn.commit()
    ok = cursor.rowcount > 0
    close_database(conn)
    print(f"{'✓' if ok else '✗'} Password updated for user '{username}'")
    return ok

def delete_user(username):
    """
    Delete a user from the database.
    """
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM users
        WHERE username = ?
    """, (username,))
    conn.commit()
    ok = cursor.rowcount > 0
    close_database(conn)
    print(f"{'✓' if ok else '✗'} User '{username}' deleted")
    return ok

def user_exists(username):
    """
    Check if a username exists in the database.
    """
    return get_user_by_username(username) is not None

# ============ TEST HARNESS ============

if __name__ == "__main__":
    # Clean slate for demo
    if user_exists("alice"):
        delete_user("alice")

    # Create
    insert_user("alice", "bcrypt_hash_example", "admin")

    # Read
    print("By username:", get_user_by_username("alice"))
    print("All users:", get_all_users())

    # Update
    update_user_role("alice", "manager")
    update_user_password("alice", "new_bcrypt_hash_example")

    # Delete
    delete_user("alice")
    print("Exists after delete:", user_exists("alice"))