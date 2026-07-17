class Node:

    def __init__(self, title, node_type, level):

        self.title = title
        self.type = node_type
        self.level = level

        self.children = []
        self.content = []

    def add_child(self, node):
        self.children.append(node)

    def add_content(self, text):
        self.content.append(text)