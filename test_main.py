import unittest
import requests
import json
import time
from main import MockServer, MockServerHandler, DEFAULT_HOST, DEFAULT_PORT, MOCK_DATA

# Der Port für den Testserver, um Konflikte mit einem potenziell laufenden Hauptserver zu vermeiden
TEST_PORT = 8001 
TEST_URL = f"http://{DEFAULT_HOST}:{TEST_PORT}"

class TestMockServer(unittest.TestCase):
    """
    Testsuite für den Mock-Server.
    Startet einen Server in einem separaten Thread vor den Tests und stoppt ihn danach.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Wird einmal vor allen Tests in dieser Klasse ausgeführt.
        Startet den Mock-Server in einem separaten Thread.
        """
        print(f"\nStarte Mock-Server für Tests auf {TEST_URL}...")
        cls.mock_server = MockServer((DEFAULT_HOST, TEST_PORT), MockServerHandler)
        cls.mock_server.start() # Startet den Server im Hintergrund
        time.sleep(0.1)  # Kurze Pause, um sicherzustellen, dass der Server gestartet ist
        print("Mock-Server für Tests gestartet.")

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Wird einmal nach allen Tests in dieser Klasse ausgeführt.
        Stoppt den Mock-Server.
        """
        print(f"\nStoppe Mock-Server für Tests auf {TEST_URL}...")
        cls.mock_server.stop() # Stoppt den Server
        print("Mock-Server für Tests gestoppt.")

    def test_get_users(self) -> None:
        """
        Testet den GET-Endpunkt für /api/users.
        Erwartet einen Statuscode 200 und die vordefinierten Benutzerdaten.
        """
        response = requests.get(f"{TEST_URL}/api/users") # Sendet eine GET-Anfrage
        self.assertEqual(response.status_code, 200) # Prüft den Statuscode
        self.assertEqual(response.json(), MOCK_DATA["/api/users"]["GET"]["body"]) # Prüft den Antwortkörper

    def test_post_users(self) -> None:
        """
        Testet den POST-Endpunkt für /api/users.
        Erwartet einen Statuscode 201 und die vordefinierte Erfolgsmeldung.
        """
        new_user_data = {"name": "Charlie", "email": "charlie@example.com"}
        response = requests.post(f"{TEST_URL}/api/users", json=new_user_data) # Sendet eine POST-Anfrage mit JSON-Körper
        self.assertEqual(response.status_code, 201) # Prüft den Statuscode
        self.assertEqual(response.json(), MOCK_DATA["/api/users"]["POST"]["body"]) # Prüft den Antwortkörper

    def test_get_product_by_id(self) -> None:
        """
        Testet den GET-Endpunkt für /api/products/1.
        Erwartet einen Statuscode 200 und die vordefinierten Produktdaten.
        """
        response = requests.get(f"{TEST_URL}/api/products/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), MOCK_DATA["/api/products/1"]["GET"]["body"])

    def test_put_product_by_id(self) -> None:
        """
        Testet den PUT-Endpunkt für /api/products/1.
        Erwartet einen Statuscode 200 und die vordefinierte Erfolgsmeldung.
        """
        updated_product_data = {"name": "Laptop Pro", "price": 1500}
        response = requests.put(f"{TEST_URL}/api/products/1", json=updated_product_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), MOCK_DATA["/api/products/1"]["PUT"]["body"])

    def test_delete_product_by_id(self) -> None:
        """
        Testet den DELETE-Endpunkt für /api/products/1.
        Erwartet einen Statuscode 204 (No Content).
        """
        response = requests.delete(f"{TEST_URL}/api/products/1")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b'') # Prüft, ob der Antwortkörper leer ist

    def test_get_status(self) -> None:
        """
        Testet den GET-Endpunkt für /api/status.
        """
        response = requests.get(f"{TEST_URL}/api/status")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), MOCK_DATA["/api/status"]["GET"]["body"])

    def test_get_unknown_path(self) -> None:
        """
        Testet eine GET-Anfrage an einen unbekannten Pfad.
        Erwartet einen Statuscode 404 (Not Found).
        """
        response = requests.get(f"{TEST_URL}/api/nonexistent")
        self.assertEqual(response.status_code, 404)
        self.assertIn("not found", response.json().get("error", "").lower()) # Prüft die Fehlermeldung

    def test_unsupported_method_for_path(self) -> None:
        """
        Testet eine Anfrage mit einer nicht unterstützten Methode für einen bekannten Pfad.
        Erwartet einen Statuscode 405 (Method Not Allowed).
        """
        response = requests.post(f"{TEST_URL}/api/products/1") # POST ist nicht für /api/products/1 definiert
        self.assertEqual(response.status_code, 405)
        self.assertIn("not allowed", response.json().get("error", "").lower())

if __name__ == "__main__":
    unittest.main()
