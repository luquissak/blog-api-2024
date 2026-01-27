import unittest
from unittest.mock import MagicMock, patch

class TestRagGcpAgentBqFullBlog(unittest.TestCase):

    @patch('langchain_google_community.bq_storage_vectorstores.bigquery.BigQueryVectorStore')  # Ensure 'test.store' is the correct import path and has the 'store' attribute
    def test_add_texts(self, mock_store):
        # Sample data
        all_texts = ["Apples and oranges", "Cars and airplanes", "Pineapple", "Train", "Banana"]
        metadatas = [{"len": len(t)} for t in all_texts]

        # Mock the add_texts method
        mock_store.add_texts = MagicMock()

        # Call the method to add texts
        mock_store.add_texts(all_texts, metadatas=metadatas)

        # Assert that add_texts was called with the correct arguments
        mock_store.add_texts.assert_called_once_with(all_texts, metadatas=metadatas)

if __name__ == '__main__':
    unittest.main()