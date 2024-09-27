from tests.base.base_test_case import BaseTestCase

class TestRoute(BaseTestCase):
    def assertStatusCode(self, response, expected_status_code):
        """Ensures that the response status code is as expected."""
        self.assertEqual(response.status_code, expected_status_code)

    def assertMessage(self, response, expected_message):
        """Ensures that the response message is as expected."""
        data = response.json

        self.assertIn('message', data)

        self.assertEqual(data['message'], expected_message)

    def POSTRequest(self, route, token=None, data=None):
        """Makes a POST request with or without authentication."""
        headers = {'Authorization': f'Bearer {token}'} if token else {}

        return self.client.post(route, json=data, headers=headers)

    def GETRequest(self, route, token=None):
        """Makes a GET request with or without authentication."""
        headers = {'Authorization': f'Bearer {token}'} if token else {}

        return self.client.get(route, headers=headers)

    def PUTRequest(self, route, token=None, data=None):
        """Makes a PUT request with or without authentication."""
        headers = {'Authorization': f'Bearer {token}'} if token else {}

        return self.client.put(route, json=data, headers=headers)

    def PATCHRequest(self, route, token=None, data=None):
        """Makes a PATCH request with or without authentication."""
        headers = {'Authorization': f'Bearer {token}'} if token else {}

        return self.client.patch(route, json=data, headers=headers)

    def DELETERequest(self, route, token=None):
        """Makes a DELETE request with or without authentication."""
        headers = {'Authorization': f'Bearer {token}'} if token else {}
        
        return self.client.delete(route, headers=headers)
