import unittest
from unittest.mock import patch
from vtpass.main import VtPassPythonSDK

class TestVtPassPythonSDK(unittest.TestCase):
    def setUp(self):
        self.sdk = VtPassPythonSDK()

    @patch("requests.get")
    def test_get_credit_wallet_balance_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"contents": {"balance": 100}}
        balance = self.sdk.get_credit_wallet_balance("https://api.vtpass.com")
        self.assertEqual(balance, 100)

    @patch("requests.get")
    def test_get_credit_wallet_balance_error(self, mock_get):
        mock_get.return_value.status_code = 500
        mock_get.return_value.text = "Internal Server Error"
        error = self.sdk.get_credit_wallet_balance("https://api.vtpass.com")
        self.assertEqual(error, "HTTP error occurred: 500 - Internal Server Error")

    @patch("requests.get")
    def test_get_available_service_categories_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"content": [{"id": 1, "name": "Category 1"}, {"id": 2, "name": "Category 2"}]}
        categories = self.sdk.get_available_service_categories("https://api.vtpass.com")
        self.assertEqual(categories, [{"id": 1, "name": "Category 1"}, {"id": 2, "name": "Category 2"}])

    # Add more test cases for other methods...

if __name__ == "__main__":
    unittest.main()import unittest
from unittest.mock import patch
from vtpass.main import VtPassPythonSDK

class TestVtPassPythonSDK(unittest.TestCase):

    def setUp(self):
        self.sdk = VtPassPythonSDK()

    def test_verify_keys_added(self):
        with patch('vtpass.main.sys') as mock_sys:
            self.sdk.verify_keys_added()
            mock_sys.exit.assert_called_with(1)

    def test_get_request_headers(self):
        headers = self.sdk.get_request_headers()
        self.assertEqual(headers['api-key'], self.sdk.api_key)
        self.assertEqual(headers['public-key'], self.sdk.public_key)
        self.assertEqual(headers['Accept'], 'application/json')
        self.assertEqual(headers['Content-Type'], 'application/json')

    def test_post_request_headers(self):
        headers = self.sdk.post_request_headers()
        self.assertEqual(headers['api-key'], self.sdk.api_key)
        self.assertEqual(headers['secret-key'], self.sdk.secret_key)
        self.assertEqual(headers['Accept'], 'application/json')
        self.assertEqual(headers['Content-Type'], 'application/json')

    # Add more test cases for other methods...

if __name__ == '__main__':
    unittest.main()import unittest
from unittest.mock import patch
from vtpass.main import VtPassPythonSDK

class TestVtPassPythonSDK(unittest.TestCase):

    @patch('vtpass.main.requests.get')
    def test_get_credit_wallet_balance_success(self, mock_get):
        sdk = VtPassPythonSDK()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"contents": {"balance": 100}}
        result = sdk.get_credit_wallet_balance("https://api.vtpass.com")
        self.assertEqual(result, 100)

    @patch('vtpass.main.requests.get')
    def test_get_credit_wallet_balance_http_error(self, mock_get):
        sdk = VtPassPythonSDK()
        mock_get.return_value.status_code = 404
        mock_get.return_value.text = "Not Found"
        result = sdk.get_credit_wallet_balance("https://api.vtpass.com")
        self.assertEqual(result, "HTTP error occurred: 404 - Not Found")

    @patch('vtpass.main.requests.get')
    def test_get_credit_wallet_balance_exception(self, mock_get):
        sdk = VtPassPythonSDK()
        mock_get.side_effect = Exception("An error occurred")
        result = sdk.get_credit_wallet_balance("https://api.vtpass.com")
        self.assertEqual(result, "An error occurred")

    # Add more test cases for other methods...

if __name__ == '__main__':
    unittest.main()