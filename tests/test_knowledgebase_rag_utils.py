import unittest
import knowledgebase_rag.utils as utils

class TestKnowledgeRAGUtils(unittest.TestCase):

    def test_is_valid_url_valid(self):
        # Test with a valid URL, check if return type is string
        url = utils.is_valid_url("https://waterservices.usgs.gov/docs/")
        self.assertIsInstance(url, str)

        # Test with a valid URL, check if the returned URL ends with a "/"
        url = utils.is_valid_url("https://waterservices.usgs.gov/docs")
        self.assertTrue(url.endswith("/"))

    def test_is_valid_url_invalid(self):
        # Test with an invalid URL, check if ValueError is raised
        with self.assertRaises(ValueError):
            utils.is_valid_url("waterservices.usgs.gov/docs/")
        # Test with an invalid URL, check if ValueError is raised
        with self.assertRaises(ValueError):
            utils.is_valid_url("https://waterservices.usgs.gov/docs/'; DROP TABLE users;")
        # Test with None, check if ValueError is raised
        with self.assertRaises(ValueError):
            utils.is_valid_url(None)

    def test_find_pages_from_base_valid(self):
        # Test with USGS URL, check if return type is list
        links = utils.find_pages_from_base("https://waterservices.usgs.gov/docs/")
        self.assertIsInstance(links, list)
        # Test with USGS URL, check if the length of the list is greater than 0
        self.assertGreater(len(links), 0)
        
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