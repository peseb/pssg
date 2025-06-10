import unittest

from textnode import TextNode, TextType
from util import extract_markdown_images, extract_markdown_links, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_node_to_html_node


class TextTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.Text)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.Text)
        new_nodes = split_nodes_delimiter([node], "`", TextType.Code)
        self.assertEqual(len(new_nodes), 3)

        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.Text)

        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.Code)

        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.Text)
    
    def test_split_nodes_delimiter_italic(self):
        node = TextNode("This is text with a _italic block_ word", TextType.Text)
        new_nodes = split_nodes_delimiter([node], "_", TextType.Italic)
        self.assertEqual(len(new_nodes), 3)

        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.Text)

        self.assertEqual(new_nodes[1].text, "italic block")
        self.assertEqual(new_nodes[1].text_type, TextType.Italic)

        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.Text)

    def test_split_nodes_delimiter_two_bold(self):
        node = TextNode("This is text with a *bold* block *word*", TextType.Text)
        new_nodes = split_nodes_delimiter([node], "*", TextType.Bold)
        self.assertEqual(len(new_nodes), 4)

        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.Text)

        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.Bold)

        self.assertEqual(new_nodes[2].text, " block ")
        self.assertEqual(new_nodes[2].text_type, TextType.Text)

        self.assertEqual(new_nodes[3].text, "word")
        self.assertEqual(new_nodes[3].text_type, TextType.Bold)
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.Text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.Text),
                TextNode("image", TextType.Image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.Text),
                TextNode(
                    "second image", TextType.Image, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_images_no_images(self):
        node = TextNode(
            "This is text with no images",
            TextType.Text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with no images", TextType.Text),
            ],
            new_nodes,
        )
    
    def test_split_links(self):
        node = TextNode(
                "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
                TextType.Text,
            )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.Text),
                TextNode("to boot dev", TextType.Link, "https://www.boot.dev"),
                TextNode(" and ", TextType.Text),
                TextNode(
                    "to youtube", TextType.Link, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )
    
    def test_split_links_no_link(self):
        node = TextNode(
                "This is text with no links!",
                TextType.Text,
            )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode(
                "This is text with no links!",
                TextType.Text,
            )
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()