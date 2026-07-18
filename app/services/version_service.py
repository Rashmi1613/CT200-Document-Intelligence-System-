from app.database import get_connection


class VersionService:

    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    def get_latest_version(self, document_id):
        """
        Returns the latest version number for a document.
        """

        self.cursor.execute(
            """
            SELECT MAX(version_number) AS latest
            FROM document_versions
            WHERE document_id=?
            """,
            (document_id,)
        )

        row = self.cursor.fetchone()

        if row["latest"] is None:
            return 0

        return row["latest"]

    def get_document(self, document_name):
        """
        Returns document row if it exists.
        """

        self.cursor.execute(
            """
            SELECT *
            FROM documents
            WHERE name=?
            """,
            (document_name,)
        )

        return self.cursor.fetchone()

    def get_sections(self, document_version_id):
        """
        Returns every section belonging to one version.
        """

        self.cursor.execute(
            """
            SELECT *
            FROM sections
            WHERE document_version_id=?
            ORDER BY id
            """,
            (document_version_id,)
        )

        return self.cursor.fetchall()
    def get_latest_version_id(self, document_id):
        self.cursor.execute(
        """
        SELECT id
        FROM document_versions
        WHERE document_id=?
        ORDER BY version_number DESC
        LIMIT 1
        """,
        (document_id,)
        )

        row = self.cursor.fetchone()
        return row["id"] if row else None


    def get_max_logical_node_id(self):
         self.cursor.execute(
         """
        SELECT MAX(logical_node_id) AS max_id
        FROM sections
        """
         )

         row = self.cursor.fetchone()

         if row["max_id"] is None:
             return 0
  
         return row["max_id"]


    def build_lookup(self, document_version_id):
        """
        Returns:
          {
            (title, level): logical_node_id
          }
        """

        sections = self.get_sections(document_version_id)

        lookup = {}

        for section in sections:
            lookup[(section["title"], section["level"])] = section["logical_node_id"]

        return lookup
def get_latest_version_id(self, document_id):

    self.cursor.execute(
        """
        SELECT id
        FROM document_versions
        WHERE document_id=?
        ORDER BY version_number DESC
        LIMIT 1
        """,
        (document_id,)
    )

    row = self.cursor.fetchone()

    return row["id"] if row else None


def get_version_id(self, document_id, version_number):

    self.cursor.execute(
        """
        SELECT id
        FROM document_versions
        WHERE document_id=?
        AND version_number=?
        """,
        (document_id, version_number)
    )

    row = self.cursor.fetchone()

    return row["id"] if row else None


def get_top_level_sections(self, document_version_id):

    self.cursor.execute(
        """
        SELECT
            logical_node_id,
            title,
            type,
            level
        FROM sections
        WHERE document_version_id=?
        AND level=1
        ORDER BY logical_node_id
        """,
        (document_version_id,)
    )

    return self.cursor.fetchall()