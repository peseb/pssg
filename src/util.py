import re
from typing import List, Tuple
from leafnode import LeafNode
from textnode import TextNode, TextType

def extract_markdown_images(text: str) -> List[Tuple[str, str]]:
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text: str) -> List[Tuple[str, str]]:
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

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


def split_nodes_delimiter(old_nodes: List[TextNode], delimiter: str, text_type: TextType) -> List[TextNode]:
    result: List[TextNode] = []
    for node in old_nodes:
        text = node.text
        while delimiter in text:
            next_delimiter = text.index(delimiter)
            is_even_delimiter_count = text.count(delimiter) % 2 == 0  
            current_text_type = TextType.Text if is_even_delimiter_count else text_type
            result.append(TextNode(text[:next_delimiter], current_text_type))
            text = text[next_delimiter + 1:]

        if len(text) > 0:
            result.append(TextNode(text, TextType.Text))

    return result
