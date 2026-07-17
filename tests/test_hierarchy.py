from app.parser.parser import PDFParser
from app.parser.classifier import DocumentClassifier
from app.parser.hierarchy_builder import HierarchyBuilder


def print_tree(node, indent=0):

    print("    " * indent + node.title)

    for paragraph in node.content:
        print("    " * (indent + 1) + "- " + paragraph[:60])

    for child in node.children:
        print_tree(child, indent + 1)


# -------------------------
# Parse PDF
# -------------------------
parser = PDFParser(r"C:\Users\rashm\Downloads\ct200_manual.pdf")

blocks = parser.extract_blocks()

# -------------------------
# Classify blocks
# -------------------------
classifier = DocumentClassifier()

classified_blocks = classifier.classify(blocks)

# -------------------------
# Build hierarchy
# -------------------------
builder = HierarchyBuilder()

root = builder.build(classified_blocks)

# -------------------------
# Print tree
# -------------------------
print_tree(root)