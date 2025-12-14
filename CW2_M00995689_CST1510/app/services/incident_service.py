from app.data.db import connect_database

def get_all_incidents():
    conn = connect_database()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, date, incident_type, severity, status, description, reported_by
        FROM incidents
        ORDER BY date DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def insert_incident(date, incident_type, severity, status, description, reported_by):
    conn = connect_database()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO incidents (date, incident_type, severity, status, description, reported_by)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (str(date), incident_type, severity, status, description, reported_by))
    conn.commit()
    conn.close()

def update_incident_status(incident_id, new_status):
    conn = connect_database()
    cur = conn.cursor()
    cur.execute("UPDATE incidents SET status = ? WHERE id = ?", (new_status, incident_id))
    conn.commit()
    conn.close()

def delete_incident(incident_id):
    conn = connect_database()
    cur = conn.cursor()
    cur.execute("DELETE FROM incidents WHERE id = ?", (incident_id,))
    conn.commit()
    conn.close()