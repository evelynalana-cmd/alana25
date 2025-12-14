import bcrypt
from app.data.db import connect_database

username = "admin"
password = "admin123"
role = "admin"

hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

conn = connect_database()
cur = conn.cursor()
cur.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, hashed, role))
conn.commit()
conn.close()