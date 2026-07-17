from app.parser.parser import PDFParser

parser = PDFParser(r"C:\Users\rashm\Downloads\ct200_manual.pdf")

blocks = parser.extract_blocks()

for block in blocks:
    print("=" * 80)
    print(block)