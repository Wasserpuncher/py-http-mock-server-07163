# py-http-mock-server

[![Build Status](https://github.com/your-username/py-http-mock-server/workflows/Python%20application/badge.svg)](https://github.com/your-username/py-http-mock-server/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Contributors](https://img.shields.io/github/contributors/your-username/py-http-mock-server)](https://github.com/your-username/py-http-mock-server/graphs/contributors)

Ein leichter und unternehmenstauglicher REST API Mock-Server, der mit Pythons Standardmodul `http.server` erstellt wurde. Dieses Projekt bietet eine einfache, aber leistungsstarke Möglichkeit, API-Antworten für die lokale Entwicklung, Tests und schnelles Prototyping zu simulieren, wodurch Abhängigkeiten von Backend-Diensten reduziert werden.

## Inhaltsverzeichnis
- [Funktionen](#funktionen)
- [Installation](#installation)
- [Verwendung](#verwendung)
- [Struktur der Mock-Daten](#struktur-der-mock-daten)
- [Mitwirken](#mitwirken)
- [Lizenz](#lizenz)
- [Dokumentation](#dokumentation)

## Funktionen
*   **Einfache Einrichtung**: Schneller Start mit minimaler Konfiguration.
*   **Leichtgewichtig**: Basiert auf der Python-Standardbibliothek, keine schwerfälligen Frameworks.
*   **Anpassbare Antworten**: Definieren Sie Mock-Antworten (Statuscodes, Körper) für verschiedene HTTP-Methoden und Pfade.
*   **Zweisprachige Dokumentation**: Umfassende Dokumentation in Englisch und Deutsch verfügbar.
*   **Unit-Tests**: Die Kernlogik ist durch Unit-Tests abgedeckt.
*   **CI/CD-Ready**: Enthält einen GitHub Actions Workflow für automatisierte Tests.

## Installation

1.  **Repository klonen**:
    ```bash
    git clone https://github.com/py-http-mock-server/py-http-mock-server.git
    cd py-http-mock-server
    ```

2.  **Virtuelle Umgebung erstellen** (empfohlen):
    ```bash
    python -m venv venv
    source venv/bin/activate # Unter Windows verwenden Sie `venv\Scripts\activate`
    ```

3.  **Abhängigkeiten installieren**:
    ```bash
    pip install -r requirements.txt
    ```

## Verwendung

Um den Mock-Server zu starten, führen Sie einfach das Skript `main.py` aus:

```bash
python main.py
```

Standardmäßig startet der Server auf `http://127.0.0.1:8000`.

Sie können dann Anfragen an die definierten Mock-Endpunkte senden.

**Beispielanfragen (mit `curl`):**

*   **GET /api/users**:
    ```bash
    curl http://127.0.0.1:8000/api/users
    ```
    Erwartete Ausgabe: `[{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]`

*   **POST /api/users**:
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"name": "Charlie", "email": "charlie@example.com"}' http://127.0.0.1:8000/api/users
    ```
    Erwartete Ausgabe: `{"message": "User created successfully"}`

*   **GET /api/products/1**:
    ```bash
    curl http://127.0.0.1:8000/api/products/1
    ```
    Erwartete Ausgabe: `{"id": 1, "name": "Laptop", "price": 1200}`

*   **PUT /api/products/1**:
    ```bash
    curl -X PUT -H "Content-Type: application/json" -d '{"name": "Laptop Pro", "price": 1500}' http://127.0.0.1:8000/api/products/1
    ```
    Erwartete Ausgabe: `{"message": "Product updated successfully"}`

*   **DELETE /api/products/1**:
    ```bash
    curl -X DELETE http://127.0.0.1:8000/api/products/1
    ```
    Erwartete Ausgabe: (Kein Inhalt, Statuscode 204)

## Struktur der Mock-Daten

Die Mock-Antworten sind derzeit im `MOCK_DATA`-Dictionary in `main.py` im Arbeitsspeicher definiert. Jeder Eintrag ordnet einen URL-Pfad einem Dictionary von HTTP-Methoden zu, das wiederum einem Antwortobjekt mit `status_code` und `body` zugeordnet ist.

Beispiel:
```python
MOCK_DATA = {
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
    # ... weitere Pfade
}
```

**Zukünftige Erweiterung**: Die Unterstützung für das Laden von Mock-Daten aus externen Konfigurationsdateien (z.B. `config.json` oder `YAML`) ist geplant.

## Mitwirken

Wir freuen uns über Beiträge! Bitte lesen Sie unsere [CONTRIBUTING.md](CONTRIBUTING.md) für Richtlinien zum Einstieg.

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert. Details finden Sie in der Datei [LICENSE](LICENSE).

## Dokumentation

*   [Architecture Deep Dive (English)](docs/architecture_en.md)
*   [Architektur-Tiefenanalyse (Deutsch)](docs/architecture_de.md)
