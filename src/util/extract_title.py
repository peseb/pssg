from htmlnode import HTMLNode
from util.markdown_to_html_node import markdown_to_html_node

def find_heading(node: HTMLNode) -> str:
    if node.tag == "h1" and node.children and node.children[0].value:
        return node.children[0].value
    
    if node.children is None:
        return ""

    heading = ""
    for c in node.children:
        heading = find_heading(c)
        if heading:
            return heading
    
    return heading


def extract_title(markdown: str):
    node = markdown_to_html_node(markdown)
    heading = find_heading(node)
    if heading:
        return heading.removeprefix("# ")
    
    raise Exception("No header found")
         