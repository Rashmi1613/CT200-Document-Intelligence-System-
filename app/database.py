import sqlite3

DATABASE_NAME = "documents.db"


def get_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT NOT NULL,

        version INTEGER NOT NULL,

        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sections(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        document_id INTEGER,

        parent_id INTEGER,

        title TEXT,

        type TEXT,

        level INTEGER,

        content TEXT,

        FOREIGN KEY(document_id)
            REFERENCES documents(id),

        FOREIGN KEY(parent_id)
            REFERENCES sections(id)
    )
    """)

    conn.commit()
    conn.close()


def save_document(root):

    conn = get_connection()
    cursor = conn.cursor()

    # Save document
    cursor.execute(
        """
        INSERT INTO documents(name, version)
        VALUES(?, ?)
        """,
        (root.title, 1)
    )

    document_id = cursor.lastrowid

    # Save all sections recursively
    save_section(
        cursor,
        document_id,
        root,
        None
    )

    conn.commit()
    conn.close()

    return document_id


def save_section(cursor, document_id, node, parent_id):

    content = "\n".join(node.content)

    cursor.execute(
        """
        INSERT INTO sections(
            document_id,
            parent_id,
            title,
            type,
            level,
            content
        )
        VALUES(?,?,?,?,?,?)
        """,
        (
            document_id,
            parent_id,
            node.title,
            node.type,
            node.level,
            content
        )
    )

    node_id = cursor.lastrowid

    for child in node.children:
        save_section(
            cursor,
            document_id,
            child,
            node_id
        )