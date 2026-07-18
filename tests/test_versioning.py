from app.parser.parser import PDFParser
from app.parser.classifier import DocumentClassifier
from app.parser.hierarchy_builder import HierarchyBuilder
from app.database import create_tables, save_document

# Create database tables
create_tables()

# Parse PDF
parser = PDFParser(r"C:\Users\rashm\Downloads\ct200_manual.pdf")
blocks = parser.extract_blocks()

# Classify blocks
classifier = DocumentClassifier()
classified_blocks = classifier.classify(blocks)

# Build hierarchy
builder = HierarchyBuilder()
root = builder.build(classified_blocks)

# Save document
version_id = save_document(root)

print(f"Document saved successfully!")
print(f"Document Version ID: {version_id}")