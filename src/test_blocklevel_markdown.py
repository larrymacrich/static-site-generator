import unittest
from blocklevel_markdown import markdown_to_blocks

class test_extract_markdown_images(unittest.TestCase):
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

    
if __name__ == "__main__":
    unittest.main()