from leafnode import LeafNode
from textnode import TextNode, TextType


def text_node_to_html_node(textnode: TextNode) -> LeafNode:
    match textnode.text_type:
        case TextType.Text:
            return LeafNode(None, textnode.text)
        case TextType.Bold:
            return LeafNode("b", textnode.text)
        case TextType.Italic:
            return LeafNode("i", textnode.text)
        case TextType.Link:
            return LeafNode("a", textnode.text)
        case TextType.Image:
            src = textnode.url if textnode.url != None else ""
            return LeafNode("img", "", {"alt": textnode.text, "src": src})
        case _: pass
    
    raise Exception("Invalid TextType")

