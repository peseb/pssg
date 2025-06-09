from typing import List, Optional, Self

class HTMLNode():
    def __init__(self, tag: Optional[str] = None, value: Optional[str] = None, children: Optional[List[Self]] = None, props: Optional[dict[str, str]] = None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError()
    
    def props_to_html(self) -> str:
        if self.props is None: return ""
        return " " + " ".join(map(lambda x: f"{x}={self.props[x]}", self.props))
    
    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"