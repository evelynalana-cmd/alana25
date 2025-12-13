import pandas as pd
from app.data.db import connect_database

def insert_dataset(dataset_name, department, row_count, size_mb, last_updated=None, description=None):
    """Insert new dataset metadata into database."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO datasets_metadata 
        (dataset_name, department, row_count, size_mb, last_updated, description)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (dataset_name, department, row_count, size_mb, last_updated, description))
    conn.commit()
    dataset_id = cursor.lastrowid
    conn.close()
    return dataset_id

def get_all_datasets():
    """Get all datasets as DataFrame."""
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM datasets_metadata ORDER BY id",
        conn
    )
    conn.close()
    return df

def get_datasets_by_department(department):
    """Get datasets filtered by department."""
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM datasets_metadata WHERE department = ?",
        conn,
        params=(department,)
    )
    conn.close()
    return df

def update_dataset(dataset_id, **kwargs):
    """Update dataset by ID."""
    conn = connect_database()
    cursor = conn.cursor()
    
    allowed_fields = ['dataset_name', 'department', 'row_count', 'size_mb', 'last_updated', 'description']
    updates = []
    values = []
    
    for field, value in kwargs.items():
        if field in allowed_fields and value is not None:
            updates.append(f"{field} = ?")
            values.append(value)
    
    if updates:
        values.append(dataset_id)
        query = f"UPDATE datasets_metadata SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, values)
        conn.commit()
    
    conn.close()

def delete_dataset(dataset_id):
    """Delete dataset by ID."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM datasets_metadata WHERE id = ?", (dataset_id,))
    conn.commit()
    conn.close()
