from app.database import get_connection
conn = get_connection()
cursor = conn.cursor()
print("=== DOCUMENTS ===")
cursor.execute("SELECT * FROM documents")
for row in cursor.fetchall():
    print(dict(row))
print("\n=== DOCUMENT VERSIONS ===")
cursor.execute("SELECT * FROM document_versions")
for row in cursor.fetchall():
    print(dict(row))
print("\n=== SECTIONS ===")
cursor.execute("""SELECT document_version_id, logical_node_id, title, content_hash FROM sections ORDER BY document_version_id, logical_node_id""")
for row in cursor.fetchall():
    print(dict(row))
conn.close()