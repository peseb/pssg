import unittest

from textnode import TextNode, TextType
from util import text_node_to_html_node


class TextTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.Text)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    


if __name__ == "__main__":
    unittest.main()