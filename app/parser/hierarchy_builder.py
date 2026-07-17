from app.parser.node import Node


class HierarchyBuilder:

    def build(self, classified_blocks):

        root = None
        stack = []

        for block in classified_blocks:

            block_type = block["type"]

            # -------------------------------
            # TITLE
            # -------------------------------
            if block_type == "TITLE":

                root = Node(
                    title=block["text"],
                    node_type="TITLE",
                    level=0
                )

                stack = [root]

            # -------------------------------
            # HEADING
            # -------------------------------
            elif block_type == "HEADING":

                node = Node(
                    title=block["text"],
                    node_type="HEADING",
                    level=block["level"]
                )

                while stack and stack[-1].level >= node.level:
                    stack.pop()

                stack[-1].add_child(node)

                stack.append(node)

            # -------------------------------
            # PARAGRAPH
            # -------------------------------
            elif block_type == "PARAGRAPH":

                if stack:
                    stack[-1].add_content(block["text"])

        return root