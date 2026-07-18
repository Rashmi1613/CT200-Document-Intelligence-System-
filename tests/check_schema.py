from app.database import get_connection

conn = get_connection()
cursor = conn.cursor()

print("=== TABLES ===")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
for row in cursor.fetchall():
    print(row["name"])

print("\n=== SECTIONS SCHEMA ===")
cursor.execute("PRAGMA table_info(sections)")
for row in cursor.fetchall():
    print(dict(row))

conn.close()