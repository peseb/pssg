from enum import Enum


class TextType(Enum):
    Text = "text"
    Bold = "bold"
    Italic = "italic"
    Code = "code"
    Link = "link"
    Image = "image"