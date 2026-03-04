# py-http-mock-server

[![Build Status](https://github.com/your-username/py-http-mock-server/workflows/Python%20application/badge.svg)](https://github.com/your-username/py-http-mock-server/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Contributors](https://img.shields.io/github/contributors/your-username/py-http-mock-server)](https://github.com/your-username/py-http-mock-server/graphs/contributors)

A lightweight and enterprise-ready REST API Mock Server built with Python's standard `http.server` module. This project provides a simple yet powerful way to simulate API responses for local development, testing, and rapid prototyping, reducing dependencies on backend services.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Mock Data Structure](#mock-data-structure)
- [Contributing](#contributing)
- [License](#license)
- [Documentation](#documentation)

## Features
*   **Simple Setup**: Get started quickly with minimal configuration.
*   **Lightweight**: Built on Python's standard library, no heavy frameworks.
*   **Customizable Responses**: Define mock responses (status codes, bodies) for different HTTP methods and paths.
*   **Bilingual Documentation**: Comprehensive documentation available in both English and German.
*   **Unit Tested**: Core logic is covered by unit tests.
*   **CI/CD Ready**: Includes a GitHub Actions workflow for automated testing.

## Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/py-http-mock-server/py-http-mock-server.git
    cd py-http-mock-server
    ```

2.  **Create a virtual environment** (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To start the mock server, simply run the `main.py` script:

```bash
python main.py
```

By default, the server will start on `http://127.0.0.1:8000`.

You can then send requests to the defined mock endpoints.

**Example requests (using `curl`):**

*   **GET /api/users**:
    ```bash
    curl http://127.0.0.1:8000/api/users
    ```
    Expected output: `[{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]`

*   **POST /api/users**:
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"name": "Charlie", "email": "charlie@example.com"}' http://127.0.0.1:8000/api/users
    ```
    Expected output: `{"message": "User created successfully"}`

*   **GET /api/products/1**:
    ```bash
    curl http://127.0.0.1:8000/api/products/1
    ```
    Expected output: `{"id": 1, "name": "Laptop", "price": 1200}`

*   **PUT /api/products/1**:
    ```bash
    curl -X PUT -H "Content-Type: application/json" -d '{"name": "Laptop Pro", "price": 1500}' http://127.0.0.1:8000/api/products/1
    ```
    Expected output: `{"message": "Product updated successfully"}`

*   **DELETE /api/products/1**:
    ```bash
    curl -X DELETE http://127.0.0.1:8000/api/products/1
    ```
    Expected output: (No content, 204 status code)

## Mock Data Structure

The mock responses are currently defined in-memory within `main.py` in the `MOCK_DATA` dictionary. Each entry maps a URL path to a dictionary of HTTP methods, which then maps to a response object containing `status_code` and `body`.

Example:
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
    # ... more paths
}
```

**Future Enhancement**: Support for loading mock data from external configuration files (e.g., `config.json` or `YAML`) is planned.

## Contributing

We welcome contributions! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to get started.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Documentation

*   [Architecture Deep Dive (English)](docs/architecture_en.md)
*   [Architektur-Tiefenanalyse (Deutsch)](docs/architecture_de.md)
