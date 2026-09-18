import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_not_eq(self):
        node = TextNode("a link", TextType.LINK, None)
        node2 = TextNode("a link", TextType.LINK, 'www.google.com')
        self.assertNotEqual(node, node2)

    def test_text_type(self):
        node = TextNode('asdf', TextType.TEXT)
        node2 = TextNode('asdf', TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_to_html(self):
        node = TextNode('Here is google link', TextType.LINK, url='www.google.com')
        html_node = text_node_to_html_node(node)
        self.assertEqual(
            html_node.to_html(),
            '<a href="www.google.com">Here is google link</a>'
        )


if __name__ == "__main__":
    unittest.main()