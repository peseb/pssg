import unittest
from enums.blocktype import BlockType
from util.block_to_blocktype import block_to_blocktype

class BlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        paragraph = "blablabla"
        blocktype = block_to_blocktype(paragraph)
        self.assertEqual(blocktype, BlockType.Paragraph)
    
    def test_heading(self):
        heading_blocks = ["### this is a heading", "# this is a heading", "###### this is a heading"]
        for block in heading_blocks:
            blocktype = block_to_blocktype(block)
            self.assertEqual(blocktype, BlockType.Heading)
        
        not_headings = ["#Not a heading", "Not a heading", "######not a heading", "####### not a heading"]
        for block in not_headings:
            blocktype = block_to_blocktype(block)
            self.assertNotEqual(blocktype, BlockType.Heading)
        
    def test_codeblock(self):
        heading_blocks = ["``` this is code```", "```this is a heading   ```", "```code```"]
        for block in heading_blocks:
            blocktype = block_to_blocktype(block)
            self.assertEqual(blocktype, BlockType.Code)
        
        not_headings = ["```Not code", "Not a code```", "``Not code```"]
        for block in not_headings:
            blocktype = block_to_blocktype(block)
            self.assertNotEqual(blocktype, BlockType.Code)
    
    def test_quote(self):
        heading_blocks = ["> Simple quote", "> Quote\n> Quote"]
        for block in heading_blocks:
            blocktype = block_to_blocktype(block)
            self.assertEqual(blocktype, BlockType.Quote)
        
        not_headings = ["Not quote", "> Quote\nNot quote"]
        for block in not_headings:
            blocktype = block_to_blocktype(block)
            self.assertNotEqual(blocktype, BlockType.Quote)
    
    def test_unordered_lists(self):
        heading_blocks = ["- Simple listitem", "- Item1\n- Item 2"]
        for block in heading_blocks:
            blocktype = block_to_blocktype(block)
            self.assertEqual(blocktype, BlockType.UnorderedList)
        
        not_headings = ["-Not item", "- Item 1\n-Not item 2"]
        for block in not_headings:
            blocktype = block_to_blocktype(block)
            self.assertNotEqual(blocktype, BlockType.UnorderedList)
    
    def test_ordered_lists(self):
        heading_blocks = ["1. Simple listitem", "1. Item1\n2. Item 2"]
        for block in heading_blocks:
            blocktype = block_to_blocktype(block)
            self.assertEqual(blocktype, BlockType.OrderedList)
        
        not_headings = ["1Not item", "1.Not item", "1. Item 1\n2.Not item 2", "1. Item 1\n3. Item 3\n2. Item 2" ]
        for block in not_headings:
            blocktype = block_to_blocktype(block)
            self.assertNotEqual(blocktype, BlockType.OrderedList)

