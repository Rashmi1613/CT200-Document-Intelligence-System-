import sqlite3

conn = sqlite3.connect("documents.db")
cursor = conn.cursor()

print("\nDOCUMENTS\n")

for row in cursor.execute("SELECT * FROM documents"):
    print(row)

print("\nSECTIONS\n")

for row in cursor.execute("""
SELECT id, parent_id, title, level
FROM sections
ORDER BY id
"""):
    print(row)

conn.close()