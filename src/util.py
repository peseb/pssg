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

def split_nodes_link(old_nodes: List[TextNode]):
    result: List[TextNode] = []
    for node in old_nodes:
        matches = extract_markdown_links(node.text)
        nodes = get_nodes(node, matches, TextType.Link)
        result.extend(nodes)

    return result

def split_nodes_image(old_nodes: List[TextNode]):
    result: List[TextNode] = []
    for node in old_nodes:
        matches = extract_markdown_images(node.text)
        nodes = get_nodes(node, matches, TextType.Image)
        result.extend(nodes)

    return result

def get_nodes(node: TextNode, matches: List[Tuple[str, str]], text_type: TextType):
    text = node.text
    result: List[TextNode] = []
    prefix = "!" if text_type is TextType.Image else ""
    if len(matches) > 0:
        for match in matches:
            image_start_index = text.index(f"{prefix}[{match[0]}]")
            text_upto_image = text[:image_start_index]

            result.append(TextNode(text_upto_image, TextType.Text))
            image_text = match[0]
            image_url = match[1]
            result.append(TextNode(image_text, text_type, image_url))

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
        if delimiter not in text:
            result.append(node)
        else:
            while delimiter in text:
                next_delimiter = text.index(delimiter)
                is_even_delimiter_count = text.count(delimiter) % 2 == 0  
                current_text_type = TextType.Text if is_even_delimiter_count else text_type
                result.append(TextNode(text[:next_delimiter], current_text_type))
                text = text[next_delimiter + len(delimiter):]

            if len(text) > 0:
                result.append(TextNode(text, TextType.Text))

    return result

def text_to_textnodes(text: str) -> List[TextNode]:
    old_nodes: List[TextNode] = []
    new_nodes: List[TextNode] = [TextNode(text, TextType.Text)]
    while len(old_nodes) != len(new_nodes):
        old_nodes = new_nodes.copy()
        generated_nodes: List[TextNode] = []
        generated_nodes = split_nodes_image(old_nodes)
        generated_nodes = split_nodes_link(generated_nodes)
        generated_nodes = split_nodes_delimiter(generated_nodes, "_", TextType.Italic)
        generated_nodes = split_nodes_delimiter(generated_nodes, "**", TextType.Bold)
        generated_nodes = split_nodes_delimiter(generated_nodes, "`", TextType.Code)

        new_nodes = (generated_nodes).copy()
        print("Old nodes: ", len(old_nodes))
        print("New nodes: ", len(new_nodes))


    return new_nodes



