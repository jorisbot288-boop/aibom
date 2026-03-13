# Contributing to AIBOM

First, thank you for considering contributing to AIBOM. Your help is valuable in keeping this a useful and up-to-date tool for the community. As AI frameworks evolve, community contributions are the best way to ensure AIBOM remains a relevant compliance tool.

This document provides guidelines for contributing to the project.

## Running the Project Locally

To get started, set up a local development environment:

1.  Clone the repository:
    ```sh
    git clone https://github.com/jorisbot288-boop/aibom.git
    cd aibom
    ```

2.  Install the project in editable mode:
    ```sh
    pip install -e .
    ```

3.  Run a scan on a project:
    ```sh
    aibom scan /path/to/your/project
    ```

## Adding Support for a New AI Framework

The core scanning logic is located in `aibom/scanner.py`. To add support for a new framework, you will likely need to modify the functions in this file to detect new dependency patterns or file types associated with that framework.

Please follow the existing structure and add comments to explain the new detection logic.

## Pull Request Guidelines

To help us review and merge your changes quickly, please follow these guidelines:

-   **Small, focused PRs:** Submit one pull request per feature or bug fix.
-   **Clear descriptions:** Provide a clear description of the problem and your solution in the pull request. Include any relevant issue numbers.
-   **One feature per PR:** Do not bundle multiple unrelated changes into a single pull request.

## Reporting Issues

If you encounter a bug or have a suggestion, please open an issue on GitHub. Include the following information:

-   A clear and descriptive title.
-   The version of AIBOM you are using.
-   Steps to reproduce the issue.
-   Any relevant error messages or logs.

## Code Style

This project uses standard Python. While there are no strict linting or formatting rules, please try to follow the existing code style for consistency. The main goal is readability and maintainability.
