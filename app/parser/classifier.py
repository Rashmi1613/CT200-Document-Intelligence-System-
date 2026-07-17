from enum import Enum
import re

class BlockType(Enum):
    TITLE = "TITLE"
    HEADING = "HEADING"
    PARAGRAPH = "PARAGRAPH"
    TABLE = "TABLE"
    LIST = "LIST"





class DocumentClassifier:

    def classify(self, blocks):
        classified_blocks = []

        for block in blocks:
            classified_blocks.append(self.classify_block(block))

        return classified_blocks

    def classify_block(self, block):

        text = block["text"].strip()
        font_size = block["font_size"]
        is_bold = block["is_bold"]

        # ---------- TITLE ----------
        if font_size >= 20:
            block["type"] = BlockType.TITLE.value
            block["level"] = 0
            return block

        # ---------- HEADING ----------
        heading_level = self.get_heading_level(text)

        if heading_level is not None and is_bold:
            block["type"] = BlockType.HEADING.value
            block["level"] = heading_level
            return block

        # ---------- PARAGRAPH ----------
        block["type"] = BlockType.PARAGRAPH.value
        block["level"] = None

        return block
    def get_heading_level(self, text):

        match = re.match(r'^(\d+(?:\.\d+)*)', text)

        if not match:
            return None

        numbering = match.group(1)

        return len(numbering.split("."))