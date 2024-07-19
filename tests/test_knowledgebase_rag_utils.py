import unittest
from unittest.mock import patch
from unstructured.documents.elements import Element
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

    @patch('knowledgebase_rag.utils.OpenAIEmbeddingEncoder')
    def test_unstructured_page_processing(self, mock_encoder):

        # Setup the mock object for OpenAI Embedding Encoder
        mock_instance = mock_encoder.return_value
        mock_instance.embed_documents.return_value = [Element()] * 1536

        # Test with a valid URL, check if return type is list
        embeddings = utils.unstructured_page_processing("https://waterservices.usgs.gov/docs/")
        self.assertIsInstance(embeddings, list)
        # Test with a valid URL, check if the length of the list is greater than 0
        self.assertEqual(len(embeddings), 1536)

    @patch('knowledgebase_rag.utils.Pinecone')
    def test_update_embeddings_in_pinecone(self, mock_pinecone):

        # Setup the mock object for Pinecone
        mock_instance = mock_pinecone.return_value
        mock_instance.delete.return_value = {}
        mock_instance.upsert_embeddings.return_value = {'upserted_count': 1}
        mock_instance.delete.return_value = {}

        # Set up test harness
        elem = Element()
        elem.embeddings = [0] * 1536
        elem.text = "This is an example text."
        elem.metadata.url = "https://example.com"

        # Test with a list of Elements, check if the function returns None
        embeddings = [elem]
        self.assertIsNone(utils.update_embeddings_in_pinecone(embeddings))
        



if __name__ == '__main__':
    unittest.main()