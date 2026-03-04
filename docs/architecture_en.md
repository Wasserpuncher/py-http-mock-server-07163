# Architecture Deep Dive: py-http-mock-server

This document provides a detailed overview of the architecture, design principles, and components of the `py-http-mock-server` project.

## 1. Introduction

The `py-http-mock-server` is designed to be a simple, lightweight, yet robust REST API mock server. Its primary goal is to facilitate frontend development, integration testing, and rapid prototyping by providing predictable and configurable API responses without requiring a live backend service. It leverages Python's built-in `http.server` module, emphasizing simplicity and minimal external dependencies.

## 2. Core Design Principles

*   **Simplicity**: Utilize Python's standard library as much as possible to keep the codebase small and easy to understand.
*   **Extensibility**: While simple, the design should allow for future enhancements, such as external configuration loading or more complex routing rules.
*   **Testability**: Components should be designed to be easily testable, enabling automated verification of functionality.
*   **Bilingual Support**: All user-facing documentation is provided in both English and German to cater to a broader audience.
*   **Enterprise-Ready**: Adherence to best practices like type hinting, docstrings, unit tests, and CI/CD ensures suitability for professional environments.

## 3. Component Breakdown

The server's architecture is composed of two main Python classes: `MockServerHandler` and `MockServer`, along with a global in-memory data store `MOCK_DATA`.

### 3.1. `MOCK_DATA` (In-memory Mock Definitions)

*   **Purpose**: Stores the definitions of mock API endpoints, including the expected HTTP methods, status codes, and response bodies.
*   **Structure**: A nested dictionary where:
    *   The top-level keys are URL paths (e.g., `/api/users`).
    *   The second-level keys are HTTP methods (e.g., `"GET"`, `"POST"`).
    *   The values at the deepest level are dictionaries containing `"status_code"` (integer) and `"body"` (any JSON-serializable type).
*   **Current State**: Defined directly within `main.py`.
*   **Future Enhancements**: The `initial_issue_title` suggests moving this to an external configuration file (e.g., `config.json`) for easier management and dynamic updates without code changes.

### 3.2. `MockServerHandler` (Request Handler)

*   **Inheritance**: Extends `http.server.BaseHTTPRequestHandler`. This class provides the fundamental request handling capabilities of a standard HTTP server.
*   **Responsibilities**:
    *   **Request Parsing**: Automatically handles parsing of incoming HTTP requests (headers, paths, methods).
    *   **Method-Specific Dispatch**: Implements `do_GET`, `do_POST`, `do_PUT`, `do_DELETE` methods, which are called automatically by `BaseHTTPRequestHandler` based on the incoming request's HTTP method.
    *   **Response Generation**:
        *   Retrieves the appropriate mock response from `MOCK_DATA` based on the request path and method.
        *   Sets HTTP headers, including the status code and `Content-Type`.
        *   Serializes the mock response body (if it's a dict or list) to JSON and writes it to the client.
    *   **Error Handling**: Returns `404 Not Found` for undefined paths and `405 Method Not Allowed` for paths where the requested method is not defined.
    *   **Logging**: Overrides `log_message` to simplify or disable default server logging, making output cleaner.

*   **Key Methods**:
    *   `_set_headers(status_code: int, content_type: str)`: Helper to send response status and headers.
    *   `_serve_mock_response(method: str)`: Core logic for looking up and serving mock data.
    *   `do_GET`, `do_POST`, `do_PUT`, `do_DELETE`: Entry points for specific HTTP methods. These methods also read the request body for POST/PUT requests, though it's currently not processed, only logged (commented out). This provides a hook for future features like request body validation.

### 3.3. `MockServer` (Server Orchestrator)

*   **Inheritance**: Extends `socketserver.TCPServer`. `http.server.HTTPServer` itself inherits from `TCPServer`, so this provides a direct way to manage the server instance.
*   **Responsibilities**:
    *   **Server Initialization**: Binds to a specified host and port, and associates the `MockServerHandler` with the server.
    *   **Lifecycle Management**: Provides `start()` and `stop()` methods for controlled server operation.
    *   **Asynchronous Operation**: `start()` launches the server in a separate `threading.Thread`, allowing the main application thread to continue execution (crucial for testing environments).
    *   **Address Reuse**: Sets `allow_reuse_address = True` to prevent "Address already in use" errors when restarting the server quickly, common in development and testing.

*   **Key Methods**:
    *   `__init__(server_address: tuple[str, int], RequestHandlerClass: type[http.server.BaseHTTPRequestHandler])`: Constructor to set up the server.
    *   `start()`: Begins serving requests in a new thread.
    *   `stop()`: Shuts down the server and waits for its thread to terminate.

## 4. Workflow and Interaction

1.  **Initialization**:
    *   When `main.py` is executed, a `MockServer` instance is created with the default host/port and `MockServerHandler`.
    *   If run via `if __name__ == "__main__":`, `mock_server.serve_forever()` is called, blocking the main thread until a `KeyboardInterrupt` (Ctrl+C) occurs.
    *   If used programmatically (e.g., in tests), `mock_server.start()` can be called to run it in a background thread.

2.  **Request Reception**:
    *   A client sends an HTTP request to the server's address.
    *   The `MockServer` (via `TCPServer`) accepts the connection.
    *   For each request, an instance of `MockServerHandler` is created.

3.  **Request Handling**:
    *   `BaseHTTPRequestHandler` (parent of `MockServerHandler`) parses the request line and headers.
    *   It then calls the appropriate `do_METHOD` method (e.g., `do_GET`, `do_POST`) in `MockServerHandler`.
    *   Inside `do_METHOD`, `_serve_mock_response` is called.
    *   `_serve_mock_response` looks up the `self.path` and `method` in the `MOCK_DATA` dictionary.
    *   If a match is found, `_set_headers` is called with the mock's status code, and the mock's `body` is serialized to JSON (if applicable) and written back to the client.
    *   If no match, a 404 or 405 error response is generated.

4.  **Server Shutdown**:
    *   When `mock_server.stop()` is called (or `KeyboardInterrupt` in `serve_forever`), `self.shutdown()` is invoked to gracefully stop the server's request-handling loop.
    *   `self.server_thread.join()` ensures the background thread completes before the program exits.

## 5. Testing Strategy

*   **Unit Tests (`test_main.py`)**:
    *   Uses Python's built-in `unittest` framework.
    *   The `setUpClass` method starts an instance of `MockServer` in a separate thread on a dedicated test port (`8001`) before any tests run.
    *   `tearDownClass` stops the server after all tests are completed.
    *   Tests use the `requests` library to send actual HTTP requests to the running mock server and assert on the `status_code` and `json()` response.
    *   Covers successful GET, POST, PUT, DELETE operations, as well as error cases like 404 (unknown path) and 405 (unsupported method).

## 6. CI/CD Integration

*   **GitHub Actions (`.github/workflows/python-app.yml`)**:
    *   Automates the testing process on every push and pull request to the `main` branch.
    *   Sets up multiple Python versions (e.g., 3.9, 3.10, 3.11) to ensure compatibility.
    *   Installs dependencies from `requirements.txt`.
    *   Runs the `unittest` suite, providing immediate feedback on code changes.

## 7. Future Considerations and Enhancements

*   **External Configuration**: Implement loading `MOCK_DATA` from a `config.json` or `YAML` file. This would allow dynamic changes without restarting the server or modifying code.
*   **Dynamic Responses**: Allow mock responses to be functions or templates that can process request data (e.g., query parameters, request body) to generate dynamic responses.
*   **Response Delays**: Introduce configurable delays for specific endpoints to simulate network latency.
*   **Stateful Mocks**: Implement simple state management for mocks (e.g., incrementing IDs for POST requests, tracking resource updates).
*   **Advanced Routing**: Support regular expressions for paths, or more complex routing logic.
*   **Middleware**: Add hooks for custom middleware (e.g., authentication, request logging, header modification).
*   **HTTPS Support**: Add an option to serve mocks over HTTPS.
*   **Web UI**: A simple web interface for managing mocks on the fly.

This architecture provides a solid foundation for a versatile mock server, capable of handling common API simulation needs while remaining simple and extensible.
