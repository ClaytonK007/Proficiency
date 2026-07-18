import unittest
from fastapi.testclient import TestClient

import api


class SouthAfricanIdValidationTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(api.app)

    def test_mismatched_dob_and_id_number_is_rejected(self):
        response = self.client.post(
            "/submit",
            data={
                "name": "Test",
                "surname": "User",
                "idNo": "9912311234567",
                "dob": "2000-01-01",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("match", response.text.lower())


if __name__ == "__main__":
    unittest.main()
