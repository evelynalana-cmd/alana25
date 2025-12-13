import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path("DATA") / "intelligence_platform.db"

# ============ CREATE ============

def insert_incident(date, incident_type, severity, status, description, reported_by=None):
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cyber_incidents 
        (date, incident_type, severity, status, description, reported_by)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (date, incident_type, severity, status, description, reported_by))
    conn.commit()
    incident_id = cursor.lastrowid
    conn.close()
    print(f"✓ Incident created with ID: {incident_id}")
    return incident_id

# ============ READ ============

def get_incident_by_id(incident_id):
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cyber_incidents WHERE id = ?", (incident_id,))
    result = cursor.fetchone()
    conn.close()
    return result

def get_all_incidents():
    conn = sqlite3.connect(str(DB_PATH))
    df = pd.read_sql_query("SELECT * FROM cyber_incidents ORDER BY date DESC, id DESC", conn)
    conn.close()
    return df

def get_incidents_by_type(incident_type):
    conn = sqlite3.connect(str(DB_PATH))
    df = pd.read_sql_query("SELECT * FROM cyber_incidents WHERE incident_type = ? ORDER BY date DESC", conn, params=(incident_type,))
    conn.close()
    return df

def get_incidents_by_status(status):
    conn = sqlite3.connect(str(DB_PATH))
    df = pd.read_sql_query("SELECT * FROM cyber_incidents WHERE status = ? ORDER BY date DESC", conn, params=(status,))
    conn.close()
    return df

# ============ UPDATE ============

def update_incident_status(incident_id, new_status):
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    cursor.execute("UPDATE cyber_incidents SET status = ? WHERE id = ?", (new_status, incident_id))
    conn.commit()
    ok = cursor.rowcount > 0
    conn.close()
    print(f"{'✓' if ok else '✗'} Status updated for incident {incident_id}")
    return ok

def update_incident_severity(incident_id, new_severity):
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    cursor.execute("UPDATE cyber_incidents SET severity = ? WHERE id = ?", (new_severity, incident_id))
    conn.commit()
    ok = cursor.rowcount > 0
    conn.close()
    print(f"{'✓' if ok else '✗'} Severity updated for incident {incident_id}")
    return ok

# ============ DELETE ============

def delete_incident(incident_id):
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cyber_incidents WHERE id = ?", (incident_id,))
    conn.commit()
    ok = cursor.rowcount > 0
    conn.close()
    print(f"{'✓' if ok else '✗'} Deleted incident {incident_id}")
    return ok

if __name__ == "__main__":
    # Insert a test incident
    test_id = insert_incident(
        date="2025-12-11 19:30:00",
        incident_type="Phishing",
        severity="High",
        status="Open",
        description="Suspicious email reported",
        reported_by="alice"
    )

    # Read back
    print("By ID:", get_incident_by_id(test_id))
    print("All incidents:")
    print(get_all_incidents())

    # Update
    update_incident_status(test_id, "Resolved")
    update_incident_severity(test_id, "Critical")

    # Delete
    delete_incident(test_id)