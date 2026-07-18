import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"id": "test", "class": "test"})
        result = " id=\"test\" class=\"test\""        
        self.assertEqual(node.props_to_html(), result)
    
if __name__ == "__main__":
    unittest.main()