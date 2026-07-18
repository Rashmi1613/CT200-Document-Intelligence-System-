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

    # -------------------------
    # Documents
    # -------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT UNIQUE NOT NULL
    )
    """)

    # -------------------------
    # Document Versions
    # -------------------------

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

    # -------------------------
    # Sections
    # -------------------------

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
            REFERENCES document_versions(id)
    )
    """)

    # -------------------------
    # Named Selections
    # -------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS selection_groups(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT NOT NULL,

        document_version_id INTEGER NOT NULL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(document_version_id)
            REFERENCES document_versions(id)
    )
    """)

    # -------------------------
    # Selection Items
    # -------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS selection_items(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        selection_id INTEGER NOT NULL,

        logical_node_id INTEGER NOT NULL,

        FOREIGN KEY(selection_id)
            REFERENCES selection_groups(id)
    )
""")

# -------------------------
# LLM Generations
# -------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS generations(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    selection_id INTEGER NOT NULL,

    source_hash TEXT NOT NULL,

    prompt TEXT NOT NULL,

    response TEXT,

    model_name TEXT,

    status TEXT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(selection_id)
        REFERENCES selection_groups(id)
)
""")

conn.commit()
conn.close()


def save_document(root):

    from app.services.version_service import VersionService

    version_service = VersionService()

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

    if row is None:

        cursor.execute(
            """
            INSERT INTO documents(name)
            VALUES(?)
            """,
            (root.title,)
        )

        document_id = cursor.lastrowid
        version_number = 1

        lookup = {}
        max_logical_node_id = 0

    else:

        document_id = row["id"]

        version_number = (
            version_service.get_latest_version(document_id) + 1
        )

        latest_version_id = (
            version_service.get_latest_version_id(document_id)
        )

        lookup = version_service.build_lookup(
            latest_version_id
        )

        max_logical_node_id = (
            version_service.get_max_logical_node_id()
        )

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

    save_section(
        cursor=cursor,
        document_version_id=document_version_id,
        node=root,
        parent_id=None,
        lookup=lookup,
        max_logical_node_id=[max_logical_node_id]
    )

    conn.commit()
    conn.close()

    return document_version_id


def save_section(
    cursor,
    document_version_id,
    node,
    parent_id,
    lookup,
    max_logical_node_id
):

    content = "\n".join(node.content)

    content_hash = hashlib.sha256(
        content.encode("utf-8")
    ).hexdigest()

    # -------------------------
    # Reuse logical node IDs
    # -------------------------

    key = (node.title, node.level)

    if key in lookup:
        logical_node_id = lookup[key]
    else:
        max_logical_node_id[0] += 1
        logical_node_id = max_logical_node_id[0]

    # -------------------------
    # Save section
    # -------------------------

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

    # IMPORTANT:
    # Store logical_node_id as parent_id
    # so children remain linked across versions.

    for child in node.children:

        save_section(
            cursor=cursor,
            document_version_id=document_version_id,
            node=child,
            parent_id=logical_node_id,
            lookup=lookup,
            max_logical_node_id=max_logical_node_id
        )