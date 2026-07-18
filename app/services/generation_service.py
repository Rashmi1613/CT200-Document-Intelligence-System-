import hashlib

from app.database import get_connection


class GenerationService:

    def __init__(self):

        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    # ------------------------------------------------
    # Selection metadata
    # ------------------------------------------------

    def get_selection(self, selection_id):

        self.cursor.execute(
        """
        SELECT
            id,
            name,
            document_version_id
        FROM selection_groups
        WHERE id=?
        """,
        (selection_id,)
        )

        return self.cursor.fetchone()

    # ------------------------------------------------
    # Node ids
    # ------------------------------------------------

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

        rows = self.cursor.fetchall()

        return [
            row["logical_node_id"]
            for row in rows
        ]

    # ------------------------------------------------
    # Node contents
    # ------------------------------------------------

    def get_nodes(
        self,
        document_version_id,
        node_ids
    ):

        if not node_ids:
            return []

        placeholders = ",".join(
            ["?"] * len(node_ids)
        )

        query = f"""
        SELECT
            logical_node_id,
            title,
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

    # ------------------------------------------------
    # Build Context
    # ------------------------------------------------

    def build_context(self, selection_id):

        selection = self.get_selection(selection_id)

        if selection is None:
            return None

        node_ids = self.get_node_ids(selection_id)

        nodes = self.get_nodes(
            selection["document_version_id"],
            node_ids
        )

        context = ""

        for node in nodes:

            context += (
                f"Title: {node['title']}\n"
                f"{node['content']}\n\n"
            )

        source_hash = hashlib.sha256(
            context.encode("utf-8")
        ).hexdigest()

        return {

            "selection_name": selection["name"],

            "document_version_id":
                selection["document_version_id"],

            "context": context,

            "source_hash": source_hash
        }

    # ------------------------------------------------
    # Duplicate detection
    # ------------------------------------------------

    def find_existing_generation(
        self,
        selection_id,
        source_hash
    ):

        self.cursor.execute(
        """
        SELECT *
        FROM generations
        WHERE selection_id=?
        AND source_hash=?
        LIMIT 1
        """,
        (
            selection_id,
            source_hash
        )
        )

        return self.cursor.fetchone()

    # ------------------------------------------------
    # Save Generation
    # ------------------------------------------------

    def save_generation(
        self,
        selection_id,
        source_hash,
        prompt,
        response,
        model_name,
        status
    ):

        self.cursor.execute(
        """
        INSERT INTO generations(

            selection_id,

            source_hash,

            prompt,

            response,

            model_name,

            status

        )

        VALUES(?,?,?,?,?,?)

        """,
        (
            selection_id,
            source_hash,
            prompt,
            response,
            model_name,
            status
        )
        )

        self.conn.commit()

        return self.cursor.lastrowid

    # ------------------------------------------------
    # Retrieve Generation
    # ------------------------------------------------

    def get_generation(
        self,
        generation_id
    ):

        self.cursor.execute(
        """
        SELECT *
        FROM generations
        WHERE id=?
        """,
        (generation_id,)
        )

        return self.cursor.fetchone()