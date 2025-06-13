import unittest
from util.extract_title import extract_title

class ExtractTitle(unittest.TestCase):
    def test_simple_title(self):
        title = "# This is a heading"
        res = extract_title(title)
        self.assertEqual(res, "This is a heading")

if __name__ == "__main__":
    unittest.main()