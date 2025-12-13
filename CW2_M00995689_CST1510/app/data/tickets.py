import pandas as pd
from app.data.db import connect_database

def insert_ticket(ticket_id, created_date, title, category, priority, status, assigned_to=None, description=None):
    """Insert new ticket into database."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO it_tickets 
        (ticket_id, created_date, title, category, priority, status, assigned_to, description)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (ticket_id, created_date, title, category, priority, status, assigned_to, description))
    conn.commit()
    row_id = cursor.lastrowid
    conn.close()
    return row_id

def get_all_tickets():
    """Get all tickets as DataFrame."""
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM it_tickets ORDER BY id DESC",
        conn
    )
    conn.close()
    return df

def get_tickets_by_status(status):
    """Get tickets filtered by status."""
    conn = connect_database()
    df = pd.read_sql_query(

        conn,
        params=(status,)
    )
    conn.close()
    return df

def get_tickets_by_priority(priority):
    """Get tickets filtered by priority."""
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM it_tickets WHERE priority = ? ORDER BY created_date DESC",
        conn,
        params=(priority,)
    )
    conn.close()
    return df

def get_tickets_by_assigned(assigned_to):
    """Get tickets filtered by assigned person."""
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM it_tickets WHERE assigned_to = ? ORDER BY created_date DESC",
        conn,
        params=(assigned_to,)
    )
    conn.close()
    return df

def update_ticket(row_id, **kwargs):
    """Update ticket by row ID."""
    conn = connect_database()
    cursor = conn.cursor()
    
    allowed_fields = ['ticket_id', 'created_date', 'title', 'category', 'priority', 'status', 'assigned_to', 'description']
    updates = []
    values = []
    
    for field, value in kwargs.items():
        if field in allowed_fields and value is not None:
            updates.append(f"{field} = ?")
            values.append(value)
    
    if updates:
        values.append(row_id)
        query = f"UPDATE it_tickets SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, values)
        conn.commit()
    
    conn.close()

def delete_ticket(row_id):
    """Delete ticket by row ID."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM it_tickets WHERE id = ?", (row_id,))
    conn.commit()
    conn.close()
