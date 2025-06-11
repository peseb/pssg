import unittest

from textnode import TextNode, TextType
from util.util import extract_markdown_images, extract_markdown_links, markdown_to_blocks, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_node_to_html_node, text_to_textnodes


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

    def test_text_to_textnodes(self):
        nodes = text_to_textnodes("This is **text** with an _italic_ word and a ```code block``` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertListEqual(
            [
                TextNode("This is ", TextType.Text),
                TextNode("text", TextType.Bold),
                TextNode(" with an ", TextType.Text),
                TextNode("italic", TextType.Italic),
                TextNode(" word and a ", TextType.Text),
                TextNode("code block", TextType.Code),
                TextNode(" and an ", TextType.Text),
                TextNode("obi wan image", TextType.Image, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.Text),
                TextNode("link", TextType.Link, "https://boot.dev"),
            ],
            nodes,
        )
    
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



if __name__ == "__main__":
    unittest.main()