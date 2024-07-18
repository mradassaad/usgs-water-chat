import unittest
import knowledgebase_rag.utils as utils

class TestKnowledgeRAGUtils(unittest.TestCase):
    def test_find_pages_from_base_valid(self):
        # Test with a valid URL
        links = utils.find_pages_from_base("https://waterservices.usgs.gov/docs/")
        self.assertIsInstance(links, list)
        
    def test_find_pages_from_base_invalid(self):
        # Test with an invalid URL
        with self.assertRaises(ValueError):
            utils.find_pages_from_base("waterservices.usgs.gov/docs/")
        # Test with a URL that contains potential injection attack
        with self.assertRaises(ValueError):
            utils.find_pages_from_base("https://waterservices.usgs.gov/docs/'; DROP TABLE users;")

        with self.assertRaises(ValueError):
            utils.find_pages_from_base(None)


if __name__ == '__main__':
    unittest.main()