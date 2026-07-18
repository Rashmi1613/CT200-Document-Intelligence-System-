from app.database import get_connection


class SelectionService:

    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    # ----------------------------
    # Version lookup
    # ----------------------------

    def get_document_version_id(self, document_id, version):

        self.cursor.execute(
            """
            SELECT id
            FROM document_versions
            WHERE document_id=?
            AND version_number=?
            """,
            (document_id, version)
        )

        row = self.cursor.fetchone()

        return row["id"] if row else None

    # ----------------------------
    # Create selection
    # ----------------------------

    def create_selection(
        self,
        name,
        document_version_id,
        logical_node_ids
    ):

        self.cursor.execute(
            """
            INSERT INTO selection_groups(
                name,
                document_version_id
            )
            VALUES(?,?)
            """,
            (
                name,
                document_version_id
            )
        )

        selection_id = self.cursor.lastrowid

        for node_id in logical_node_ids:

            self.cursor.execute(
                """
                INSERT INTO selection_items(
                    selection_id,
                    logical_node_id
                )
                VALUES(?,?)
                """,
                (
                    selection_id,
                    node_id
                )
            )

        self.conn.commit()

        return selection_id

    # ----------------------------
    # Selection metadata
    # ----------------------------

    def get_selection(self, selection_id):

        self.cursor.execute(
            """
            SELECT
                sg.id,
                sg.name,
                sg.document_version_id,
                dv.version_number
            FROM selection_groups sg
            JOIN document_versions dv
            ON sg.document_version_id=dv.id
            WHERE sg.id=?
            """,
            (selection_id,)
        )

        return self.cursor.fetchone()

    # ----------------------------
    # Node ids
    # ----------------------------

    def get_node_ids(self, selection_id):

        self.cursor.execute(
            """
            SELECT logical_node_id
            FROM selection_items
            WHERE selection_id=?
            ORDER BY id
            """,
            (selection_id,)
        )

        return [
            row["logical_node_id"]
            for row in self.cursor.fetchall()
        ]

    # ----------------------------
    # Node details
    # ----------------------------

    def get_nodes(
        self,
        document_version_id,
        node_ids
    ):

        if not node_ids:
            return []

        placeholders = ",".join(["?"] * len(node_ids))

        query = f"""
        SELECT
            logical_node_id,
            title,
            type,
            level,
            content
        FROM sections
        WHERE document_version_id=?
        AND logical_node_id IN ({placeholders})
        ORDER BY logical_node_id
        """

        self.cursor.execute(
            query,
            [document_version_id] + node_ids
        )

        return self.cursor.fetchall()