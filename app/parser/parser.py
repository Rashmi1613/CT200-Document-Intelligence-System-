import fitz  # PyMuPDF


class PDFParser:

    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path

    def extract_blocks(self):
        document = fitz.open(self.pdf_path)

        extracted_blocks = []

        for page_number, page in enumerate(document, start=1):

            blocks = page.get_text("dict")["blocks"]

            for block in blocks:

                # Ignore images
                if "lines" not in block:
                    continue

                block_text = ""
                font_size = None
                is_bold = False

                for line in block["lines"]:
                    for span in line["spans"]:

                        block_text += span["text"] + " "

                        if font_size is None:
                            font_size = span["size"]

                        if "Bold" in span["font"]:
                            is_bold = True

                block_text = block_text.strip()

                if not block_text:
                    continue

                extracted_blocks.append({
                    "page": page_number,
                    "text": block_text,
                    "font_size": font_size,
                    "is_bold": is_bold,
                    "bbox": block["bbox"]
                })

        document.close()

        return extracted_blocks