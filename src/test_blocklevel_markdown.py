import unittest
from parentnode import ParentNode
from leafnode import LeafNode
from blocklevel_markdown import (
    BlockType, 
    markdown_to_blocks, 
    block_to_block_type, 
    text_to_children,
    markdown_to_html_node,
)

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

class TestTextToChildren(unittest.TestCase):
    """Tests for blocklevel_markdown.text_to_children()"""
    def test_text_to_textnode_all_typed(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` " 
            "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) " 
            "and a [link](https://boot.dev)"
        )
        new_nodes = text_to_children(text)
        self.assertEqual(
            ''.join(node.to_html() for node in new_nodes),
            ''.join([
                LeafNode(None, "This is ").to_html(),
                LeafNode("b", "text").to_html(),
                LeafNode(None, " with an ").to_html(),
                LeafNode("i", "italic").to_html(),
                LeafNode(None, " word and a ").to_html(),
                LeafNode("code", "code block").to_html(),
                LeafNode(None, " and an ").to_html(),
                LeafNode("img", "", {"src": "https://i.imgur.com/fJRm4Vk.jpeg", "alt": "obi wan image"}).to_html(),
                LeafNode(None, " and a ").to_html(),
                LeafNode("a", "link", {"href": "https://boot.dev"}).to_html(),
            ]),
        )

class TestBlockMarkdownToHTMLNode(unittest.TestCase):
    """Tests for blocklevel_markdown.markdown_to_html_node()"""
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading_level_2(self):
        md = "## A Heading"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h2>A Heading</h2></div>")

    def test_heading_with_inline(self):
        md = "# A **Bold** Heading"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>A <b>Bold</b> Heading</h1></div>")

    def test_quote_block(self):
        md = "> To be or not to be\n> that is the question"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>To be or not to be that is the question</blockquote></div>")

    def test_unordered_list(self):
        md = "- First\n- Second\n- Third"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li>First</li><li>Second</li><li>Third</li></ul></div>")

    def test_ordered_list_double_digits(self):
        md = "\n".join(f"{i}. Item {i}" for i in range(1, 12))
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ol><li>Item 1</li><li>Item 2</li><li>Item 3</li><li>Item 4</li><li>Item 5</li><li>Item 6</li><li>Item 7</li><li>Item 8</li><li>Item 9</li><li>Item 10</li><li>Item 11</li></ol></div>")

    def test_mixed_blocks(self):
        md = "# Title\n\nA paragraph here.\n\n- item one\n- item two"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>Title</h1><p>A paragraph here.</p><ul><li>item one</li><li>item two</li></ul></div>")

if __name__ == "__main__":
    unittest.main()