from app.database import get_connection


class DatabaseService:

    def save_document(self, root):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        INSERT INTO documents(name,version)

        VALUES(?,?)

        """,
        (
            root.title,
            1
        ))

        document_id = cursor.lastrowid

        self.save_section(
            cursor,
            document_id,
            root,
            None
        )

        conn.commit()

        conn.close()

        return document_id

    def save_section(
        self,
        cursor,
        document_id,
        node,
        parent_id
    ):

        cursor.execute("""

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

            "\n".join(node.content)
        ))

        node_id = cursor.lastrowid

        for child in node.children:

            self.save_section(

                cursor,

                document_id,

                child,

                node_id
            )