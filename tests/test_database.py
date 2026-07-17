from app.database import create_tables, save_document
from app.parser.parser import PDFParser
from app.parser.classifier import DocumentClassifier
from app.parser.hierarchy_builder import HierarchyBuilder

create_tables()

parser = PDFParser(r"C:\Users\rashm\Downloads\ct200_manual.pdf")    
blocks = parser.extract_blocks()

classifier = DocumentClassifier()
classified = classifier.classify(blocks)

builder = HierarchyBuilder()
root = builder.build(classified)

document_id = save_document(root)

print(f"Document saved successfully! ID = {document_id}")