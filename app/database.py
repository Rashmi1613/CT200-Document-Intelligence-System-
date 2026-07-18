import sqlite3
import hashlib

DATABASE_NAME = "documents.db"


def get_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    # One row per document
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT UNIQUE NOT NULL
    )
    """)

    # Every upload creates a new version
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS document_versions(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        document_id INTEGER,

        version_number INTEGER,

        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(document_id)
            REFERENCES documents(id)
    )
    """)

    # Sections for each version
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sections(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        document_version_id INTEGER,

        logical_node_id INTEGER,

        parent_id INTEGER,

        title TEXT,

        type TEXT,

        level INTEGER,

        content TEXT,

        content_hash TEXT,

        FOREIGN KEY(document_version_id)
            REFERENCES document_versions(id),

        FOREIGN KEY(parent_id)
            REFERENCES sections(id)
    )
    """)

    conn.commit()
    conn.close()


def save_document(root):

    conn = get_connection()
    cursor = conn.cursor()

    # -------------------------
    # Check if document exists
    # -------------------------

    cursor.execute(
        "SELECT id FROM documents WHERE name=?",
        (root.title,)
    )

    row = cursor.fetchone()

    if row:
        document_id = row["id"]

        cursor.execute(
            """
            SELECT MAX(version_number)
            FROM document_versions
            WHERE document_id=?
            """,
            (document_id,)
        )

        latest = cursor.fetchone()[0]

        version_number = latest + 1

    else:

        cursor.execute(
            """
            INSERT INTO documents(name)
            VALUES(?)
            """,
            (root.title,)
        )

        document_id = cursor.lastrowid
        version_number = 1

    # -------------------------
    # Create new version
    # -------------------------

    cursor.execute(
        """
        INSERT INTO document_versions(
            document_id,
            version_number
        )
        VALUES(?,?)
        """,
        (
            document_id,
            version_number
        )
    )

    document_version_id = cursor.lastrowid

    logical_node_counter = [1]

    save_section(
        cursor,
        document_version_id,
        root,
        None,
        logical_node_counter
    )

    conn.commit()
    conn.close()

    return document_version_id


def save_section(
    cursor,
    document_version_id,
    node,
    parent_id,
    logical_node_counter
):

    content = "\n".join(node.content)

    content_hash = hashlib.sha256(
        content.encode("utf-8")
    ).hexdigest()

    logical_node_id = logical_node_counter[0]
    logical_node_counter[0] += 1

    cursor.execute(
        """
        INSERT INTO sections(

            document_version_id,
            logical_node_id,
            parent_id,
            title,
            type,
            level,
            content,
            content_hash

        )
        VALUES(?,?,?,?,?,?,?,?)
        """,
        (
            document_version_id,
            logical_node_id,
            parent_id,
            node.title,
            node.type,
            node.level,
            content,
            content_hash
        )
    )

    section_id = cursor.lastrowid

    for child in node.children:
        save_section(
            cursor,
            document_version_id,
            child,
            section_id,
            logical_node_counter
        )