import http.server
import socketserver
import json
import threading
from typing import Dict, Any, Union

# Definieren Sie den Standard-Host und Port für den Mock-Server
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000

# In-memory-Speicher für Mock-Daten.
# Dies kann später durch eine Konfigurationsdatei oder Datenbank ersetzt werden.
# Der Schlüssel ist der Pfad, der Wert ist ein Dictionary von HTTP-Methoden zu deren Antworten.
# Jede Antwort ist ein Dictionary mit 'status_code' und 'body'.
MOCK_DATA: Dict[str, Dict[str, Dict[str, Any]]] = {
    "/api/users": {
        "GET": {
            "status_code": 200,
            "body": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
        },
        "POST": {
            "status_code": 201,
            "body": {"message": "User created successfully"}
        }
    },
    "/api/products/1": {
        "GET": {
            "status_code": 200,
            "body": {"id": 1, "name": "Laptop", "price": 1200}
        },
        "PUT": {
            "status_code": 200,
            "body": {"message": "Product updated successfully"}
        },
        "DELETE": {
            "status_code": 204,
            "body": ""
        }
    },
    "/api/status": {
        "GET": {
            "status_code": 200,
            "body": {"status": "ok", "server": "py-http-mock-server"}
        }
    }
}

class MockServerHandler(http.server.BaseHTTPRequestHandler):
    """
    Ein benutzerdefinierter Request-Handler für den Mock-Server.
    Er verarbeitet eingehende HTTP-Anfragen und liefert vordefinierte Mock-Antworten.
    """

    def _set_headers(self, status_code: int = 200, content_type: str = "application/json") -> None:
        """
        Setzt die HTTP-Antwort-Header.
        :param status_code: Der HTTP-Statuscode, der gesendet werden soll.
        :param content_type: Der Content-Type des Antwortkörpers.
        """
        self.send_response(status_code)  # Sendet den HTTP-Statuscode
        self.send_header("Content-type", content_type)  # Setzt den Content-Type Header
        self.end_headers()  # Beendet die Header-Sektion

    def _serve_mock_response(self, method: str) -> None:
        """
        Dient die Mock-Antwort basierend auf dem angefragten Pfad und der Methode.
        Wenn keine Mock-Daten gefunden werden, wird ein 404 Not Found zurückgegeben.
        :param method: Die HTTP-Methode der Anfrage (z.B. "GET", "POST").
        """
        path = self.path  # Holt den angefragten Pfad
        
        # Überprüft, ob der Pfad in den Mock-Daten existiert
        if path in MOCK_DATA:
            # Überprüft, ob die HTTP-Methode für diesen Pfad definiert ist
            if method in MOCK_DATA[path]:
                response_data = MOCK_DATA[path][method]  # Holt die vordefinierte Antwort
                status_code = response_data.get("status_code", 200)  # Holt den Statuscode, Standard ist 200
                body = response_data.get("body", {})  # Holt den Antwortkörper, Standard ist ein leeres Dictionary
                
                self._set_headers(status_code)  # Setzt die Header mit dem Statuscode
                
                # Wenn der Körper ein Dictionary oder eine Liste ist, wird er als JSON gesendet
                if isinstance(body, (dict, list)):
                    self.wfile.write(json.dumps(body).encode("utf-8"))  # Schreibt den JSON-kodierten Körper
                else:
                    self.wfile.write(str(body).encode("utf-8"))  # Schreibt den Körper als String
            else:
                # Methode nicht gefunden für den Pfad
                self._set_headers(405)  # Method Not Allowed
                error_body = {"error": f"Method {method} not allowed for path {path}"}
                self.wfile.write(json.dumps(error_body).encode("utf-8"))
        else:
            # Pfad nicht gefunden
            self._set_headers(404)  # Not Found
            error_body = {"error": f"Path {path} not found"}
            self.wfile.write(json.dumps(error_body).encode("utf-8"))

    def do_GET(self) -> None:
        """Behandelt GET-Anfragen."""
        self._serve_mock_response("GET")

    def do_POST(self) -> None:
        """
        Behandelt POST-Anfragen.
        Für POST-Anfragen könnte man den Request-Körper lesen, um ihn zu loggen oder zu verarbeiten.
        Aktuell ignorieren wir den Request-Körper und senden nur die vordefinierte Antwort.
        """
        content_length = int(self.headers.get('Content-Length', 0)) # Holt die Länge des Request-Körpers
        post_body = self.rfile.read(content_length).decode('utf-8') # Liest den Request-Körper
        # Optional: Loggen des empfangenen POST-Körpers
        # print(f"Received POST body for {self.path}: {post_body}") 
        self._serve_mock_response("POST")

    def do_PUT(self) -> None:
        """Behandelt PUT-Anfragen."""
        content_length = int(self.headers.get('Content-Length', 0))
        put_body = self.rfile.read(content_length).decode('utf-8')
        # print(f"Received PUT body for {self.path}: {put_body}")
        self._serve_mock_response("PUT")

    def do_DELETE(self) -> None:
        """Behandelt DELETE-Anfragen."""
        self._serve_mock_response("DELETE")

    def log_message(self, format: str, *args: Any) -> None:
        """
        Überschreibt die Standard-Log-Nachrichten, um sie zu vereinfachen oder anzupassen.
        Deaktiviert standardmäßig die Ausgabe von Request-Informationen an stdout/stderr.
        Entfernen Sie die 'pass'-Anweisung, um das Logging zu aktivieren.
        """
        # pass  # Deaktiviert das Logging der Request-Nachrichten
        super().log_message(format, *args) # Standard-Logging beibehalten


class MockServer(socketserver.TCPServer):
    """
    Ein einfacher HTTP-Server, der den MockServerHandler verwendet.
    Er kapselt die Funktionalität des http.server.HTTPServer.
    """
    
    # Erlaubt die Wiederverwendung der Adresse, um "Address already in use" Fehler zu vermeiden
    allow_reuse_address = True

    def __init__(self, server_address: tuple[str, int], RequestHandlerClass: type[http.server.BaseHTTPRequestHandler]):
        """
        Initialisiert den MockServer.
        :param server_address: Ein Tupel (Host, Port) für den Server.
        :param RequestHandlerClass: Die Klasse, die Anfragen verarbeitet (z.B. MockServerHandler).
        """
        super().__init__(server_address, RequestHandlerClass)
        self.host = server_address[0]  # Speichert den Hostnamen
        self.port = server_address[1]  # Speichert den Port
        print(f"Mock-Server gestartet auf http://{self.host}:{self.port}") # Ausgabe beim Start

    def start(self) -> None:
        """
        Startet den Mock-Server in einem neuen Thread, um nicht den Haupt-Thread zu blockieren.
        Dies ist nützlich für Tests oder wenn der Server im Hintergrund laufen soll.
        """
        # Erstellt einen neuen Thread, der die Server-Schleife ausführt
        self.server_thread = threading.Thread(target=self.serve_forever)
        self.server_thread.daemon = True  # Macht den Thread zu einem Daemon, damit er beendet wird, wenn das Hauptprogramm endet
        self.server_thread.start()  # Startet den Thread
        print(f"Server-Thread gestartet für http://{self.host}:{self.port}")

    def stop(self) -> None:
        """
        Stoppt den Mock-Server.
        """
        print(f"Mock-Server wird gestoppt auf http://{self.host}:{self.port}")
        self.shutdown()  # Beendet die serve_forever Schleife
        self.server_thread.join()  # Wartet, bis der Server-Thread beendet ist
        print("Mock-Server gestoppt.")

if __name__ == "__main__":
    # Erstellt eine Instanz des MockServers mit dem Standard-Host und Port
    mock_server = MockServer((DEFAULT_HOST, DEFAULT_PORT), MockServerHandler);
    try:
        # Startet den Server, der unendlich lange läuft, bis er unterbrochen wird
        mock_server.serve_forever()
    except KeyboardInterrupt:
        # Fängt KeyboardInterrupt (Strg+C) ab, um den Server elegant zu beenden
        print("\n^C empfangen, Server wird heruntergefahren.")
    finally:
        # Stellt sicher, dass der Server ordnungsgemäß heruntergefahren wird
        mock_server.server_close()
        print("Server heruntergefahren.")
