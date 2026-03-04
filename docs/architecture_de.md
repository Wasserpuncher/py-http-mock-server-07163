# Architektur-Tiefenanalyse: py-http-mock-server

Dieses Dokument bietet einen detaillierten Überblick über die Architektur, Designprinzipien und Komponenten des Projekts `py-http-mock-server`.

## 1. Einleitung

Der `py-http-mock-server` wurde als einfacher, leichter und dennoch robuster REST API Mock-Server konzipiert. Sein primäres Ziel ist es, die Frontend-Entwicklung, Integrationstests und schnelles Prototyping zu erleichtern, indem er vorhersehbare und konfigurierbare API-Antworten bereitstellt, ohne einen Live-Backend-Dienst zu benötigen. Er nutzt Pythons eingebautes Modul `http.server` und legt den Schwerpunkt auf Einfachheit und minimale externe Abhängigkeiten.

## 2. Kern-Designprinzipien

*   **Einfachheit**: Pythons Standardbibliothek so weit wie möglich nutzen, um die Codebasis klein und leicht verständlich zu halten.
*   **Erweiterbarkeit**: Obwohl einfach, sollte das Design zukünftige Erweiterungen ermöglichen, wie z.B. das Laden externer Konfigurationen oder komplexere Routing-Regeln.
*   **Testbarkeit**: Komponenten sollten so konzipiert sein, dass sie leicht testbar sind, um die automatisierte Überprüfung der Funktionalität zu ermöglichen.
*   **Zweisprachige Unterstützung**: Alle benutzerrelevanten Dokumentationen werden sowohl in Englisch als auch in Deutsch bereitgestellt, um ein breiteres Publikum anzusprechen.
*   **Unternehmens-Ready**: Die Einhaltung bewährter Praktiken wie Typ-Hinweise, Docstrings, Unit-Tests und CI/CD gewährleistet die Eignung für professionelle Umgebungen.

## 3. Komponentenaufschlüsselung

Die Architektur des Servers besteht aus zwei Haupt-Python-Klassen: `MockServerHandler` und `MockServer`, zusammen mit einem globalen In-Memory-Datenspeicher `MOCK_DATA`.

### 3.1. `MOCK_DATA` (In-Memory Mock-Definitionen)

*   **Zweck**: Speichert die Definitionen von Mock-API-Endpunkten, einschließlich der erwarteten HTTP-Methoden, Statuscodes und Antwortkörper.
*   **Struktur**: Ein verschachteltes Dictionary, wobei:
    *   Die Schlüssel der obersten Ebene URL-Pfade sind (z.B. `/api/users`).
    *   Die Schlüssel der zweiten Ebene HTTP-Methoden sind (z.B. `"GET"`, `"POST"`).
    *   Die Werte auf der tiefsten Ebene sind Dictionaries, die `"status_code"` (Integer) und `"body"` (jeder JSON-serialisierbare Typ) enthalten.
*   **Aktueller Zustand**: Direkt in `main.py` definiert.
*   **Zukünftige Erweiterungen**: Der `initial_issue_title` schlägt vor, dies in eine externe Konfigurationsdatei (z.B. `config.json`) zu verschieben, um eine einfachere Verwaltung und dynamische Aktualisierungen ohne Codeänderungen zu ermöglichen.

### 3.2. `MockServerHandler` (Anfrage-Handler)

*   **Vererbung**: Erweitert `http.server.BaseHTTPRequestHandler`. Diese Klasse bietet die grundlegenden Funktionen zur Anfragenbearbeitung eines Standard-HTTP-Servers.
*   **Verantwortlichkeiten**:
    *   **Anfragen-Parsing**: Automatische Verarbeitung eingehender HTTP-Anfragen (Header, Pfade, Methoden).
    *   **Methoden-spezifische Verteilung**: Implementiert die Methoden `do_GET`, `do_POST`, `do_PUT`, `do_DELETE`, die vom `BaseHTTPRequestHandler` basierend auf der HTTP-Methode der eingehenden Anfrage automatisch aufgerufen werden.
    *   **Antwortgenerierung**:
        *   Ruft die entsprechende Mock-Antwort aus `MOCK_DATA` basierend auf dem Anfragenpfad und der Methode ab.
        *   Setzt HTTP-Header, einschließlich des Statuscodes und des `Content-Type`.
        *   Serialisiert den Mock-Antwortkörper (falls es sich um ein Dictionary oder eine Liste handelt) in JSON und schreibt ihn an den Client.
    *   **Fehlerbehandlung**: Gibt `404 Not Found` für undefinierte Pfade und `405 Method Not Allowed` für Pfade zurück, bei denen die angefragte Methode nicht definiert ist.
    *   **Logging**: Überschreibt `log_message`, um die Standard-Server-Logging-Ausgabe zu vereinfachen oder zu deaktivieren, wodurch die Ausgabe sauberer wird.

*   **Schlüsselmethoden**:
    *   `_set_headers(status_code: int, content_type: str)`: Hilfsfunktion zum Senden des Antwortstatus und der Header.
    *   `_serve_mock_response(method: str)`: Kernlogik zum Nachschlagen und Bereitstellen von Mock-Daten.
    *   `do_GET`, `do_POST`, `do_PUT`, `do_DELETE`: Einstiegspunkte für spezifische HTTP-Methoden. Diese Methoden lesen auch den Anfragenkörper für POST/PUT-Anfragen, obwohl dieser derzeit nicht verarbeitet, sondern nur protokolliert wird (auskommentiert). Dies bietet einen Ansatzpunkt für zukünftige Funktionen wie die Validierung des Anfragenkörpers.

### 3.3. `MockServer` (Server-Orchestrator)

*   **Vererbung**: Erweitert `socketserver.TCPServer`. `http.server.HTTPServer` selbst erbt von `TCPServer`, dies bietet also eine direkte Möglichkeit, die Serverinstanz zu verwalten.
*   **Verantwortlichkeiten**:
    *   **Server-Initialisierung**: Bindet an einen angegebenen Host und Port und ordnet den `MockServerHandler` dem Server zu.
    *   **Lebenszyklusmanagement**: Bietet `start()`- und `stop()`-Methoden für den kontrollierten Serverbetrieb.
    *   **Asynchroner Betrieb**: `start()` startet den Server in einem separaten `threading.Thread`, wodurch der Hauptanwendungs-Thread die Ausführung fortsetzen kann (entscheidend für Testumgebungen).
    *   **Adresswiederverwendung**: Setzt `allow_reuse_address = True`, um "Address already in use"-Fehler beim schnellen Neustart des Servers zu vermeiden, was in der Entwicklung und beim Testen üblich ist.

*   **Schlüsselmethoden**:
    *   `__init__(server_address: tuple[str, int], RequestHandlerClass: type[http.server.BaseHTTPRequestHandler])`: Konstruktor zur Einrichtung des Servers.
    *   `start()`: Beginnt, Anfragen in einem neuen Thread zu bedienen.
    *   `stop()`: Fährt den Server herunter und wartet, bis sein Thread beendet ist.

## 4. Workflow und Interaktion

1.  **Initialisierung**:
    *   Wenn `main.py` ausgeführt wird, wird eine `MockServer`-Instanz mit dem Standard-Host/Port und `MockServerHandler` erstellt.
    *   Wenn es über `if __name__ == "__main__":` ausgeführt wird, wird `mock_server.serve_forever()` aufgerufen, was den Haupt-Thread blockiert, bis ein `KeyboardInterrupt` (Strg+C) auftritt.
    *   Wenn es programmatisch verwendet wird (z.B. in Tests), kann `mock_server.start()` aufgerufen werden, um es in einem Hintergrund-Thread auszuführen.

2.  **Anfragenempfang**:
    *   Ein Client sendet eine HTTP-Anfrage an die Adresse des Servers.
    *   Der `MockServer` (über `TCPServer`) nimmt die Verbindung an.
    *   Für jede Anfrage wird eine Instanz von `MockServerHandler` erstellt.

3.  **Anfragenbearbeitung**:
    *   `BaseHTTPRequestHandler` (Elternklasse von `MockServerHandler`) analysiert die Anfragenzeile und die Header.
    *   Anschließend ruft es die entsprechende `do_METHOD`-Methode (z.B. `do_GET`, `do_POST`) in `MockServerHandler` auf.
    *   Innerhalb von `do_METHOD` wird `_serve_mock_response` aufgerufen.
    *   `_serve_mock_response` sucht den `self.path` und die `method` im `MOCK_DATA`-Dictionary.
    *   Wenn eine Übereinstimmung gefunden wird, wird `_set_headers` mit dem Statuscode des Mocks aufgerufen, und der `body` des Mocks wird in JSON serialisiert (falls zutreffend) und an den Client zurückgeschrieben.
    *   Wenn keine Übereinstimmung gefunden wird, wird eine 404- oder 405-Fehlerantwort generiert.

4.  **Server-Herunterfahren**:
    *   Wenn `mock_server.stop()` aufgerufen wird (oder `KeyboardInterrupt` in `serve_forever`), wird `self.shutdown()` aufgerufen, um die Anfragenbearbeitungsschleife des Servers ordnungsgemäß zu beenden.
    *   `self.server_thread.join()` stellt sicher, dass der Hintergrund-Thread beendet wird, bevor das Programm beendet wird.

## 5. Teststrategie

*   **Unit-Tests (`test_main.py`)**:
    *   Verwendet Pythons eingebautes `unittest`-Framework.
    *   Die Methode `setUpClass` startet eine Instanz des `MockServer` in einem separaten Thread auf einem dedizierten Testport (`8001`), bevor Tests ausgeführt werden.
    *   `tearDownClass` stoppt den Server, nachdem alle Tests abgeschlossen sind.
    *   Tests verwenden die `requests`-Bibliothek, um tatsächliche HTTP-Anfragen an den laufenden Mock-Server zu senden und den `status_code` und die `json()`-Antwort zu überprüfen.
    *   Umfasst erfolgreiche GET-, POST-, PUT-, DELETE-Operationen sowie Fehlerfälle wie 404 (unbekannter Pfad) und 405 (nicht unterstützte Methode).

## 6. CI/CD-Integration

*   **GitHub Actions (`.github/workflows/python-app.yml`)**:
    *   Automatisiert den Testprozess bei jedem Push und Pull Request zum `main`-Branch.
    *   Richtet mehrere Python-Versionen ein (z.B. 3.9, 3.10, 3.11), um die Kompatibilität zu gewährleisten.
    *   Installiert Abhängigkeiten aus `requirements.txt`.
    *   Führt die `unittest`-Suite aus und liefert sofortiges Feedback zu Codeänderungen.

## 7. Zukünftige Überlegungen und Verbesserungen

*   **Externe Konfiguration**: Implementierung des Ladens von `MOCK_DATA` aus einer `config.json`- oder `YAML`-Datei. Dies würde dynamische Änderungen ohne Serverneustart oder Codeänderungen ermöglichen.
*   **Dynamische Antworten**: Erlauben, dass Mock-Antworten Funktionen oder Templates sind, die Anfragedaten (z.B. Abfrageparameter, Anfragenkörper) verarbeiten können, um dynamische Antworten zu generieren.
*   **Antwortverzögerungen**: Einführung konfigurierbarer Verzögerungen für bestimmte Endpunkte, um Netzwerklatenz zu simulieren.
*   **Zustandsbehaftete Mocks**: Implementierung eines einfachen Zustandsmanagements für Mocks (z.B. inkrementelle IDs für POST-Anfragen, Verfolgung von Ressourcenaktualisierungen).
*   **Erweitertes Routing**: Unterstützung regulärer Ausdrücke für Pfade oder komplexere Routing-Logik.
*   **Middleware**: Hinzufügen von Hooks für benutzerdefinierte Middleware (z.B. Authentifizierung, Anfragenprotokollierung, Header-Modifikation).
*   **HTTPS-Unterstützung**: Option zum Bereitstellen von Mocks über HTTPS hinzufügen.
*   **Web-UI**: Eine einfache Weboberfläche zur Verwaltung von Mocks on-the-fly.

Diese Architektur bietet eine solide Grundlage für einen vielseitigen Mock-Server, der gängige API-Simulationsanforderungen erfüllen kann, während er einfach und erweiterbar bleibt.
