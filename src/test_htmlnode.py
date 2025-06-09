import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        node = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node.props_to_html(), node2.props_to_html())
    
    def test_props_to_html(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode("tag", "value", [], props)
        node2 = HTMLNode("tag", "value", [], props)
        self.assertEqual(node.props_to_html(), node2.props_to_html())
    
    def test_props_to_html_different_value(self):
        props1 = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        props2 = {
            "href": "https://www.google.com",
            "target": "_blank2",
        }
        node = HTMLNode("tag", "value", [], props1)
        node2 = HTMLNode("tag", "value", [], props2)
        self.assertNotEqual(node.props_to_html(), node2.props_to_html())


if __name__ == "__main__":
    unittest.main()