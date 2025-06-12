from typing import List
from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag: str | None, children: List[HTMLNode] | None, props: dict[str, str] | None = None) -> None:
        super().__init__(tag, None, children, props)
    
    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("ParentNode must have tag")
        if self.children is None:
            raise ValueError("ParentNode must have children")
        
        child_html = ""
        for child in self.children:
            child_html += child.to_html()
        
        return f"<{self.tag}>{child_html}</{self.tag}>"