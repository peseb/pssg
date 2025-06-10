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

def split_nodes_image(old_nodes: List[TextNode]):
    result: List[TextNode] = []
    for node in old_nodes:
        matches = extract_markdown_images(node.text)
        text = node.text
        if len(matches) > 0:
            for match in matches:
                image_start_index = text.index(f"![{match[0]}]")
                text_upto_image = text[:image_start_index]

                result.append(TextNode(text_upto_image, TextType.Text))
                image_text = match[0]
                image_url = match[1]
                result.append(TextNode(image_text, TextType.Image, image_url))

                image_url_end = f"{image_url})"
                image_end_index = text.index(image_url_end) + len(image_url_end)
                text = text[image_end_index:]
            if len(text) > 0:
                result.append(TextNode(text, TextType.Text))
        else:
            result.append(node)

    return result

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
