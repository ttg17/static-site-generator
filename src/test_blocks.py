import unittest

from blocks import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
    markdown_to_html_node,
)


class TestBlock(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_heading(self):
        block = '# This is a heading'
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.HEADING
        )

    def test_paragraph(self):
        block = 'This is a paragraph of text. It has some **bold** and _italic_ words inside of it.'
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.PARAGRAPH
        )

    def test_unordered_list(self):
        block = """
- This is the first list item in a list block
- This is a list item
- This is another list item
"""
        block_type = block_to_block_type(block.strip())
        self.assertEqual(
            block_type,
            BlockType.UNORDERED_LIST
        )

    def test_ordered_list(self):
        block = """
1. This is the first list item in a list block
2. This is a list item
3. This is another list item
"""
        block_type = block_to_block_type(block.strip())
        self.assertEqual(
            block_type,
            BlockType.ORDERED_LIST
        )

    def test_markdown_to_html_node(self):
        markdown = (
            "A **bold** paragraph\ncontinued\n\n"
            "## Heading\n\n"
            "> quoted\n> text\n\n"
            "- first\n- _second_\n\n"
            "1. one\n2. two\n\n"
            "```\n**literal**\n```"
        )
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(
            html_node.to_html(),
            "<div><p>A <b>bold</b> paragraph continued</p>"
            "<h2>Heading</h2>"
            "<blockquote>quoted\ntext</blockquote>"
            "<ul><li>first</li><li><i>second</i></li></ul>"
            "<ol><li>one</li><li>two</li></ol>"
            "<pre><code>**literal**\n</code></pre></div>",
        )

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


