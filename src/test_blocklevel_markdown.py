import unittest
from blocklevel_markdown import BlockType, markdown_to_blocks, block_to_block_type

class TestBlockLevelMarkdownToBlocks(unittest.TestCase):
    """Tests for blocklevel_markdown.markdown_to_blocks()"""
    def test_markdown_to_blocks_excessive_newlines(self):
        md = """
This is block 1



This is block 2
   
   

This is block 3
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is block 1",
                "This is block 2",
                "This is block 3",
            ],
        )

    def test_markdown_to_blocks_single_block(self):
        md = "Just a single paragraph with no blank lines."
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Just a single paragraph with no blank lines.",
            ],
        )

    def test_markdown_to_blocks_empty(self):
        md = "   \n\n   \n\n   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_mixed(self):
        md = """# Heading

Paragraph line 1
Paragraph line 2

* Item 1
* Item 2
* Item 3"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading",
                "Paragraph line 1\nParagraph line 2",
                "* Item 1\n* Item 2\n* Item 3",
            ],
        )

class TestBlockLevelBlockToBlockTypes(unittest.TestCase):
    """Tests for blocklevel_markdown.block_to_block_type()"""
    def test_block_to_block_type_paragraph(self):
        markdown = "This is a normal paragraph.\nIt can span multiple lines."
        self.assertEqual(
            block_to_block_type(markdown),
            BlockType.PARAGRAPH
        )

    def test_block_to_block_type_heading(self):
        markdown = "# A heading"
        self.assertEqual(
            block_to_block_type(markdown),
            BlockType.HEADING
        )

    def test_block_to_block_type_code(self):
        markdown = "```\npython\nprint('hello')\n```"
        self.assertEqual(
            block_to_block_type(markdown),
            BlockType.CODE
        )

    def test_block_to_block_type_quote(self):
        markdown = "> First quoted line\n> Second quoted line"
        self.assertEqual(
            block_to_block_type(markdown),
            BlockType.QUOTE
        )

    def test_block_to_block_type_unordered_list(self):
        markdown = "- Apples\n- Bread\n- Tea"
        self.assertEqual(
            block_to_block_type(markdown),
            BlockType.UNORDERED_LIST
        )

    def test_block_to_block_type_ordered_list(self):
        markdown = "1. First step\n2. Second step\n3. Third step"
        self.assertEqual(
            block_to_block_type(markdown),
            BlockType.ORDERED_LIST
        )
        
    def test_seven_heading_is_paragraph(self):
        markdown = "####### Paragraph"
        self.assertEqual(
            block_to_block_type(markdown),
            BlockType.PARAGRAPH
        )

    def test_invalid_code_is_paragrapg(self):
        markdown = "```python\nprint('hello')\n```"
        self.assertEqual(
            block_to_block_type(markdown),
            BlockType.PARAGRAPH
        )

    def test_mixed_quote_is_paragraph(self):
        markdown = "> Quoted\nNot quoted"
        self.assertEqual(
            block_to_block_type(markdown),
            BlockType.PARAGRAPH
        )

    def test_mixed_unordered_list_is_paragraph(self):
        markdown = "- Apples\n Bread\n- Tea"
        self.assertEqual(
            block_to_block_type(markdown),
            BlockType.PARAGRAPH
        )

    def test_mixed_ordered_list_with_skip_is_paragraph(self):
        markdown = "1. First step\n3. Third step"
        self.assertEqual(
            block_to_block_type(markdown),
            BlockType.PARAGRAPH
        )

    def test_mixed_ordered_list_out_of_order_numbering_is_paragraph(self):
        markdown = "1. First step\n4. Second step\n3. Third step"
        self.assertEqual(
            block_to_block_type(markdown),
            BlockType.PARAGRAPH
        )

    def test_ordered_list_must_start_at_one(self):
        markdown = "2. First item\n3. Second item"
        self.assertEqual(
            block_to_block_type(markdown),
            BlockType.PARAGRAPH,
        )

    def test_unterminated_code_fence_is_paragraph(self):
        markdown = '```python\nprint("hello")'
        self.assertEqual(
            block_to_block_type(markdown),
            BlockType.PARAGRAPH
        )
    
if __name__ == "__main__":
    unittest.main()