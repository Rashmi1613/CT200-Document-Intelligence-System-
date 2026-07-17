from app.parser.parser import PDFParser
from app.parser.classifier import DocumentClassifier


parser = PDFParser(r"C:\Users\rashm\Downloads\ct200_manual.pdf")
blocks = parser.extract_blocks()

classifier = DocumentClassifier()

classified = classifier.classify(blocks)

for block in classified:

    print("=" * 80)
    print(f"TYPE      : {block['type']}")
    print(f"LEVEL     : {block['level']}")
    print(f"PAGE      : {block['page']}")
    print(f"TEXT      : {block['text']}")