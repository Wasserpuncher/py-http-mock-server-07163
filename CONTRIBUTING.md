# Contributing to py-http-mock-server

We welcome contributions from everyone! Whether you're fixing a bug, adding a new feature, improving documentation, or just providing feedback, your input is valuable. Please take a moment to review this guide to make the contribution process as smooth as possible.

## Table of Contents
1.  [Code of Conduct](#1-code-of-conduct)
2.  [How to Contribute](#2-how-to-contribute)
    *   [Reporting Bugs](#reporting-bugs)
    *   [Suggesting Enhancements](#suggesting-enhancements)
    *   [Pull Requests](#pull-requests)
3.  [Development Setup](#3-development-setup)
4.  [Coding Guidelines](#4-coding-guidelines)
5.  [License](#5-license)

## 1. Code of Conduct

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project, you agree to abide by its terms.

## 2. How to Contribute

### Reporting Bugs

If you find a bug, please open an issue on the [GitHub Issue Tracker](https://github.com/py-http-mock-server/py-http-mock-server/issues).
Before opening a new issue, please check if a similar issue already exists. When reporting a bug, please include:

*   A clear and concise description of the bug.
*   Steps to reproduce the behavior.
*   Expected behavior.
*   Screenshots or error messages if applicable.
*   Your operating system and Python version.

### Suggesting Enhancements

We love new ideas! If you have a suggestion for a new feature or an improvement to an existing one, please open an issue on the [GitHub Issue Tracker](https://github.com/py-http-mock-server/py-http-mock-server/issues).
Describe your idea clearly, and explain why you think it would be beneficial to the project.

### Pull Requests

1.  **Fork the repository**: Click the "Fork" button on the top right of the [repository page](https://github.com/py-http-mock-server/py-http-mock-server).
2.  **Clone your forked repository**:
    ```bash
    git clone https://github.com/your-username/py-http-mock-server.git
    cd py-http-mock-server
    ```
3.  **Create a new branch**:
    ```bash
    git checkout -b feature/your-feature-name-or-bugfix/issue-number
    ```
    (e.g., `feature/add-config-file` or `bugfix/fix-404-response-123`)
4.  **Make your changes**: Implement your bug fix or feature.
5.  **Write tests**: If you're adding new functionality or fixing a bug, please add appropriate unit tests in `test_main.py` to cover your changes.
6.  **Run tests**: Ensure all existing and new tests pass:
    ```bash
    python -m unittest discover -s . -p "test_*.py"
    ```
7.  **Format your code**: We use `black` for code formatting. Please ensure your code is formatted correctly.
    ```bash
    pip install black
    black .
    ```
8.  **Commit your changes**: Write clear and concise commit messages.
    ```bash
    git add .
    git commit -m "feat: Add support for config file parsing" # or "fix: Correct 404 response for unknown paths"
    ```
9.  **Push to your fork**:
    ```bash
    git push origin feature/your-feature-name
    ```
10. **Open a Pull Request**: Go to the original `py-http-mock-server` repository on GitHub and you'll see a banner suggesting you open a pull request. Fill out the PR template with a clear description of your changes, referencing any related issues.

## 3. Development Setup

Follow the [Installation](#installation) steps in `README.md` to set up your local development environment.

## 4. Coding Guidelines

*   **Python Version**: Aim for compatibility with Python 3.9+.
*   **Type Hinting**: Use type hints for all function arguments and return values.
*   **Docstrings**: All classes and methods should have clear docstrings explaining their purpose, arguments, and return values (English).
*   **Variable Names**: Use descriptive English variable names.
*   **Inline Comments**: Inline comments should be in German, explaining complex logic or specific implementation details for beginners.
*   **Black**: Format your code with `black`.
*   **Unit Tests**: All new features and bug fixes should be accompanied by relevant unit tests.

## 5. License

By contributing, you agree that your contributions will be licensed under the MIT License.
